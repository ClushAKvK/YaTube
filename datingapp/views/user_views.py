from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse

from rest_framework.authtoken.models import Token

import json
from io import BytesIO
from itertools import chain

from ExtUser.models import ExtUser


@csrf_exempt
def profile(request, attribute=''):
    if request.method == 'POST':
        try:
            json_acceptable_string = request.body.decode('utf-8').replace("'", "\"")
            data = json.loads(json_acceptable_string)

            token = request.META['HTTP_TOKEN']
            user = Token.objects.get(pk=token).user
            gender_choices = ['Man', 'Woman']
            orientation_choices = ['Straight', 'Gay']
            if attribute == 'details':
                if data['gender'] not in gender_choices or data['orientation'] not in orientation_choices:
                    return HttpResponseBadRequest()
                else:
                    string_to_exec = 'user.profile.language = "' + data['language'] + '";' +\
                                'user.profile.badge = "' + data['badge'] + '"; user.profile.save();' +\
                                'user.gender = "' + data['gender'][0] + '";' +\
                                'user.orientation = "' + data['orientation'][0] + '"; user.save()'
            elif attribute == 'location':
                string_to_exec = 'user.location="'+data[attribute] +\
                                 '"; user.birthday="'+data['birthday'] + '";user.save()'
            else:
                string_to_exec = 'user.profile.' + attribute + ' = "' + data[attribute] + '"; user.profile.save()'

            exec(string_to_exec)

            return HttpResponse('Good response.')
        except Token.DoesNotExist:
            return HttpResponseBadRequest('Token does not exist.')
        except Exception as e:
            return HttpResponseBadRequest('Something went wrong.')
    return HttpResponseBadRequest('Only POST request.')


@csrf_exempt
def profile_photo(request):
    try:
        if request.method == 'POST':
            token = request.META['HTTP_TOKEN']
            user = Token.objects.get(pk=token).user

            image = BytesIO(request.body)
            user.profile.photo.save(
                user.username + "\'" + ' photo.jpg',
                File(image)
            )

            return JsonResponse(
                {
                    'photo_url': ('http://' + request.get_host() + user.profile.photo.url)
                }
            )
        return HttpResponseBadRequest('Only POST request.')
    except Token.DoesNotExist:
        return HttpResponseBadRequest('Token does not exist.')
    except Exception as e:
        return HttpResponseBadRequest('Something went wrong.')


@csrf_exempt
def get_users(request):
    try:
        token = request.META['HTTP_TOKEN']
        user_req = Token.objects.get(pk=token).user
        all_users = ExtUser.objects.exclude(username=user_req.username)
        all_users_ver2 = []
        for user in all_users:
            all_users_ver2.append(
                {
                    'username': user.username,
                    'photo': 'http://' + request.get_host() + user.profile.photo.url,
                    'age': str(user.birthday),
                    'location': user.location

                }
            )

        return JsonResponse(
            {
                'users': all_users_ver2
            }
        )
    except Token.DoesNotExist:
        return HttpResponseBadRequest('Token does not exist')

    except Exception as e:
        return HttpResponseBadRequest('Something went wrong.')


@csrf_exempt
def get_req_user(request):
    if request.method == 'GET':
        req_user = ExtUser.objects.get(username=request.GET.get('reqUser'))

        token = request.META['HTTP_TOKEN']
        user = Token.objects.get(pk=token).user

        user.create_visit(req_user)

        if req_user.gender == 'M':
            gender = 'Man'
        else:
            gender = 'Woman'
        if req_user.orientation == 'S':
            orientation = 'Straight'
        else:
            orientation = 'Gay'

        return JsonResponse(
            {
                'id': req_user.id,
                'username': req_user.username,
                'email': req_user.email,
                'location': req_user.location,
                'orientation': orientation,
                'gender': gender,
                'birthday': req_user.birthday,
                'photo_url': ('http://' + request.get_host() + req_user.profile.photo.url),
                'summary': req_user.profile.summary,
                'language': req_user.profile.language,
                'base': req_user.profile.base,
                'life': req_user.profile.life,
                'good': req_user.profile.good,
                'favorite': req_user.profile.favorite,
                'badge': req_user.profile.badge,
                'like': user.get_like_on_user(req_user)
            }
        )

    return HttpResponseBadRequest('Something went wrong.')


@csrf_exempt
def likes_friendship(request, kind=''):
    try:
        req_username = request.GET.get('reqUser', False)
        req_user = ''
        if req_username:
            req_user = ExtUser.objects.get(username=req_username)

        token = request.META['HTTP_TOKEN']
        user = Token.objects.get(pk=token).user

        if kind == 'create':
            user.create_friendship(req_user)
            return HttpResponse('Like created.')

        elif kind == 'delete':
            if user.delete_friendship(req_user) is True:
                return HttpResponse('Like deleted.')

        elif kind == 'getMutually':
            likes1, likes2 = user.get_friends()
            likes = list(chain(likes1, likes2))
            all_likes = []

            for like in likes:
                if like.friend != user:
                    all_likes.append(
                        {
                            'username': like.friend.username,
                            'photo': 'http://' + request.get_host() + like.friend.profile.photo.url,
                            'age': str(like.friend.birthday),
                            'location': like.friend.location,
                            'date': str(like.created.date())
                        }
                    )
                else:
                    all_likes.append(
                        {
                            'username': like.creator.username,
                            'photo': 'http://' + request.get_host() + like.creator.profile.photo.url,
                            'age': str(like.creator.birthday),
                            'location': like.creator.location,
                            'date': str(like.created.date())
                        }
                    )

            return JsonResponse(
                {
                    'ownLikes': all_likes
                }
            )

        elif kind == 'getSentLikes':
            likes1, likes2 = user.get_sent_requests_for_friendship()

            sent_likes = list(chain(likes1, likes2))
            likes = []

            for sent in sent_likes:
                if sent.friend != user:
                    likes.append(
                        {
                            'username': sent.friend.username,
                            'photo': 'http://' + request.get_host() + sent.friend.profile.photo.url,
                            'age': str(sent.friend.birthday),
                            'location': sent.friend.location,
                            'date': str(sent.created.date())
                        }
                    )
                else:
                    likes.append(
                        {
                            'username': sent.creator.username,
                            'photo': 'http://' + request.get_host() + sent.creator.profile.photo.url,
                            'age': str(sent.creator.birthday),
                            'location': sent.creator.location,
                            'date': str(sent.created.date())
                        }
                    )

            return JsonResponse(
                {
                    'ownLikes': likes
                }
            )

        elif kind == 'getOwnLikes':
            own_likes = user.get_requests_for_friendships()
            likes = []
            for like in own_likes:
                likes.append(
                    {
                        'username': like.creator.username,
                        'photo': 'http://' + request.get_host() + like.creator.profile.photo.url,
                        'age': str(like.creator.birthday),
                        'location': like.creator.location,
                        'date': str(like.created.date())
                    }
                )
            return JsonResponse(
                {
                    'ownLikes': likes
                }
            )
    except Token.DoesNotExist:
        return HttpResponseBadRequest('Token does not exist.')

    except Exception as e:
        return HttpResponseBadRequest('Something went wrong.')


@csrf_exempt
def get_visitors(request, kind=''):
    try:
        token = request.META['HTTP_TOKEN']
        user = Token.objects.get(pk=token).user

        if kind == 'my':
            visitors = []
            for visitor in user.get_my_visitors():
                visitors.append(
                    {
                        'username': visitor.visitor.username,
                        'photo': 'http://' + request.get_host() + visitor.visitor.profile.photo.url,
                        'age': str(visitor.visitor.birthday),
                        'location': visitor.visitor.location,
                        'date': str(visitor.visitDate)
                    }
                )

            return JsonResponse(
                {
                    'visitors': visitors
                }
            )
        elif kind == 'own':
            visitors = []

            for visitor in user.get_my_visitors():
                visitors.append(
                    {
                        'username': visitor.reqUser.username,
                        'photo': 'http://' + request.get_host() + visitor.reqUser.profile.photo.url,
                        'age': str(visitor.reqUser.birthday),
                        'location': visitor.reqUser.location,
                        'date': str(visitor.visitDate)
                    }
                )

            return JsonResponse(
                {
                    'visitors': visitors
                }
            )

        return HttpResponseBadRequest('Cant work with this url.')
    except Token.DoesNotExist:
        return HttpResponseBadRequest('Token does not exist.')


@csrf_exempt
def refresh_token(request):
    try:
        token = request.META['HTTP_TOKEN']
        user = Token.objects.get(pk=token).user
        user.refresh_token()
        new_token = Token.objects.get(user=user).key

        return JsonResponse(
            {
                'new_token': new_token
            }
        )
    except Token.DoesNotExist:
        return HttpResponseBadRequest('Token does not exist.')
