import math

from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.shortcuts import render
import get_subsctibers.VK_API as vk
import requests

from get_subsctibers.models import Subscriber, SubscriberSubscriber

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
    vk_response = requests.get(query)

    if vk_response.status_code == 200 and 'response' in vk_response.json():
        result = vk_response.json()['response']['items']
        count = math.ceil(vk_response.json()['response']['count'] / COUNT)


    prev_offset = offset - COUNT
    next_offset = offset + COUNT
    pages = [i * COUNT for i in range(count)]

    check_user = Subscriber.objects.filter(user_id=user['id'])

    if not check_user:
        main_user = Subscriber()
        main_user.user_id = user['id']
        main_user.name = user['first_name']
        main_user.surname = user['last_name']
        main_user.save()

    for item in result:
        check_user = Subscriber.objects.filter(user_id=item['id'])
        if not check_user:
            sub_user = Subscriber()
            sub_user.user_id = item['id']
            sub_user.name = item['first_name']
            sub_user.surname = item['last_name']
            sub_user.save()
        check_user = SubscriberSubscriber.objects.filter(user_owner=user['id'], user_subsciber=item['id'])
        if not check_user:
            subscribe = SubscriberSubscriber()
            subscribe.user_owner = Subscriber.objects.filter(user_id=user['id'])[0]
            subscribe.user_subsciber = Subscriber.objects.filter(user_id=item['id'])[0]
            subscribe.save()

    return render(request, 'index.html', {
        'result': result,
        'user': user,
        'prev_offset': prev_offset,
        'next_offset': next_offset,
        'pages': pages,
        'count': COUNT
    })


class SubscribeDetailView(DetailView):
    model = Subscriber
    template_name = "archive_detail.html"

    def get(self, request, *args, **kwargs):
        user = Subscriber.objects.filter(user_id=kwargs['id'])[0]
        subscribers = SubscriberSubscriber.objects.filter(user_owner=user)

        context = {
            'user': user,
            'subscribers': subscribers
        }
        return render(request, 'archive_detail.html', context)


class SubscriberListView(ListView):
    model = Subscriber
    paginate_by = 20
    template_name = "archive.html"
