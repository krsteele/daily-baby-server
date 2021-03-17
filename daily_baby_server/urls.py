"""daily_baby_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import include
from rest_framework import routers
from django.urls import path

from dailybabyapi.views import register_user, login_user
from dailybabyapi.views import Profile
from dailybabyapi.views.daysOfWeek import DaysOfWeek
from dailybabyapi.views.relationships import RelationshipView
from dailybabyapi.views.baby import BabyView
from dailybabyapi.views.user import Users


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'profile', Profile, 'profile')
router.register(r'daysOfWeek', DaysOfWeek, 'daysOfWeek')
router.register(r'relationships', RelationshipView, 'relationship')
router.register(r'babies', BabyView, 'baby')
router.register(r'users', Users, 'user')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),

]

