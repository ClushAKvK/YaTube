from ExtUser.models import ExtUser
from django.contrib import auth
from django.http import JsonResponse,HttpResponseBadRequest, HttpResponse
import json
from PIL import Image
import sys
from django.views.decorators.csrf import csrf_exempt
from ExtUser.models import ExtUser
from ExtUserFriedship.models import Friendship
from ExtUserCorrespondence.models import ExtUserMessage
from ExtUserCorrespondence.models import ExtUserDialog
from datetime import datetime
from rest_framework.authtoken.models import Token
from Visitor.models import Visitor


def test_view(request):
    try:
        admin = ExtUser.objects.get(username='admin')
        test4 = ExtUser.objects.get(username='Valeria')

        return HttpResponse('ok')
    except:
        print(sys.exc_info())
        return HttpResponseBadRequest()
