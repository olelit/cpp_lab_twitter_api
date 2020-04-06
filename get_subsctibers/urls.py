"""cpp_twitter_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from get_subsctibers import views
from get_subsctibers.views import SubscriberListView, SubscribeDetailView

urlpatterns = [
    path('user/', views.index),
    path('user/<str:user_id>/<int:offset>/', views.index, name="list"),
    path('user/<str:user_id>/', views.index, name="list"),
    path('archive/', SubscriberListView.as_view(), name='archive'),
    path('archive/<id>', SubscribeDetailView.as_view(), name='archive_detail')
]
