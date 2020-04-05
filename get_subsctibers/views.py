import math

from django.http import HttpResponse
from django.shortcuts import render
import get_subsctibers.VK_API as vk
import requests

COUNT = 20


def index(request, user_id=vk.DEFAULT_ID, offset=0):
    user = None
    result = {}
    count = 1

    user_params = "user_ids={0}&name_case=Nom&&fields={1}".format(user_id, "photo_100")
    user_query = "https://api.vk.com/method/{0}?{1}&access_token={2}&v={3}".format("users.get", user_params, vk.TOKEN,
                                                                                   vk.VERSION)
    user_response = requests.get(user_query)

    if user_response.status_code == 200:
        user = user_response.json()['response'][0]
    user_id = user['id']

    params = "user_id={0}&count={1}&offset={2}&fields={3}".format(user_id, COUNT,
                                                                  offset, "photo_50")
    query = "https://api.vk.com/method/{0}?{1}&access_token={2}&v={3}".format("users.getFollowers", params, vk.TOKEN,
                                                                              vk.VERSION)
    print(query)
    vk_response = requests.get(query)

    if vk_response.status_code == 200:
        result = vk_response.json()['response']['items']
        count = math.ceil(vk_response.json()['response']['count'] / COUNT)

    prev_offset = offset - COUNT
    next_offset = offset + COUNT
    pages = [i * COUNT for i in range(count)]

    return render(request, 'index.html', {
        'result': result,
        'user': user,
        'prev_offset': prev_offset,
        'next_offset': next_offset,
        'pages': pages,
        'count': COUNT
    })
