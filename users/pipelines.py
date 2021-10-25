from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from users.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', '/method/users.get', None, urlencode(
        OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'personal', 'photo_100')), access_token=response['access_token'], v=5.131)), None))

    resp= requests.get(api_url)
    if resp.status_code !=200:
        return

    data = resp.json()['response'][0]

    if data['sex']:
        if data['sex'] == 2:
            user.userprofile.gender = UserProfile.MALE
        elif data['sex'] == 1:
            user.userprofile.gender = UserProfile.FEMALE
        else:
            pass

    if data['about']:
        user.userprofile.about = data['about']


    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

    age = timezone.now().date().year-bdate.year
    user.age = age
    # 100 для првоерки
    # if age < 100:
    if age <18:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')



    if data['personal']['langs']:
        print(data['personal']['langs'])
        user.userprofile.language = ''
        for language in data['personal']['langs']:
            user.userprofile.language += f'{language}\n'

    if data['photo_100']:
        user.userprofile.photo = data['photo_100']

    user.save()