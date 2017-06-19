from django.contrib import auth
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token

import json
from io import BytesIO
from urllib.request import urlopen, urlparse

from ExtUser.models import ExtUser


def check_json_data(json_data):
    json_data_keys = json_data.keys()
    if 'location' not in json_data_keys:
        json_data['location'] = ''
    if 'birthday' not in json_data_keys:
        json_data['birthday'] = '1900-01-01'
    return json_data


@csrf_exempt
def facebook(request):
    if request.method == 'POST':
        json_acceptable_string = request.body.decode('utf-8').replace("'", "\"")
        json_data = json.loads(json_acceptable_string)
        try:
            fd = urlopen(json_data['photo_url'])
            image_name = urlparse(json_data['photo_url']).path.split('/')[-1]
            image_file = BytesIO(fd.read())

            try:
                user = ExtUser.objects.get(username=json_data['username'])
                Token.objects.get(user=user)
                return JsonResponse({
                        'message': 'User and token already exist.'
                    })
            except ExtUser.DoesNotExist:
                json_data = check_json_data(json_data)
                new_user = ExtUser.objects.create_user(
                    username=json_data['username'],
                    email=json_data['email'],
                    location=json_data['location'],
                    orientation='S',
                    gender=json_data['gender'][0].upper(),
                    birthday=json_data['birthday'],
                    password=json_data['password'],
                )
                new_user.photo.save(image_name, File(image_file))
                new_user.save()
                token = Token.objects.create(user=new_user)

                if new_user:
                    return JsonResponse({
                            'message': 'User is created. Sign in please.',
                            'token': token.key
                        })

        except Exception as e:
            return HttpResponseBadRequest('Something went wrong.')
    return HttpResponseBadRequest('Only POST request.')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8').replace("'", "\""))
            identificator = json_data['identificator']
            password = json_data['password']
            if '@' in identificator:
                identificator = ExtUser.objects.get(email=identificator).username
            try:
                user = auth.authenticate(username=identificator, password=password)
            except Exception as e:
                return HttpResponseBadRequest('Some errors with login.')

            if user:
                gender = 'Man' if user.gender == 'M' else 'Woman'

                if user.orientation == 'S':
                    orientation = 'Straight'
                else:
                    orientation = 'Gay'

                response_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'location': user.location,
                    'orientation': orientation,
                    'gender': gender,
                    'birthday': user.birthday,
                    'photo_url': ('http://' + request.get_host() + user.profile.photo.url),
                    'summary': user.profile.summary,
                    'language': user.profile.language,
                    'base': user.profile.base,
                    'life': user.profile.life,
                    'good': user.profile.good,
                    'favorite': user.profile.favorite,
                    'badge': user.profile.badge,
                    'token': Token.objects.get(user=user).key
                }

                return JsonResponse(response_data)
        except Token.DoesNotExist:
            return HttpResponseBadRequest('Token does not exist.')

    return HttpResponseBadRequest('Only POST request.')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8').replace("'", "\""))
        try:
            new_user = ExtUser.objects.create_user(
                username=json_data['username'],
                email=json_data['email'],
                location=json_data['location'],
                orientation=json_data['orientation'][0],
                gender=json_data['gender'][0],
                birthday=json_data['birthday'],
                password=json_data['password']
            )
            new_user.save()
            token = Token.objects.create(user=new_user)

            if new_user:
                return JsonResponse(
                    {
                        'message': 'User is created. Sign in please.',
                        'token': token.key
                    }
                )
        except Exception as e:
            return HttpResponseBadRequest('Errors with creating user.')

    return HttpResponseBadRequest('Only POST request.')
