from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dailybabyapi.models.baby import Baby
from dailybabyapi.models import DailyUser
from dailybabyapi.models import DailyUserDay
from dailybabyapi.models import DayOfWeek
from dailybabyapi.models import UserBaby


class Profile(ViewSet):
    """User can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info
        """
        dailyuser = DailyUser.objects.get(user=request.auth.user)
        dailyuser_days = DailyUserDay.objects.filter(user=dailyuser)
        userbabies = UserBaby.objects.filter(user=dailyuser)

        dailyuser_days = DailyUserDaysSerializer(
            dailyuser_days, many=True, context={'request': request})
        userbabies = UserBabySerializer(
            userbabies, many=True, context={'request': request})
        dailyuser = DailyUserSerializer(
            dailyuser, many=False, context={'request': request})

        # Manually construct the JSON structure you want in the response
        profile = {}
        profile["dailyuser"] = dailyuser.data
        profile["dailyuser_days"] = dailyuser_days.data
        profile["userbabies"] = userbabies.data

        return Response(profile)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for dailyuser's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class DailyUserSerializer(serializers.ModelSerializer):
    """JSON serializer for dailyuser"""
    user = UserSerializer(many=False)

    class Meta:
        model = DailyUser
        fields = ('user', 'text_time', 'phone_number', 'profile_image')


class DaysOfWeekSerializer(serializers.ModelSerializer):
    """JSON serializer for daysOfWeek"""
    class Meta:
        model = DayOfWeek
        fields = ('day',)


class DailyUserDaysSerializer(serializers.ModelSerializer):
    """JSON serializer for dailyUserDays"""
    day = DaysOfWeekSerializer(many=False)

    class Meta:
        model = DailyUserDay
        fields = ('day',)

class BabySerializer(serializers.ModelSerializer):
    """JSON serializer for baby"""
    class Meta:
        model = Baby
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'nickname', 'profile_image')

class UserBabySerializer(serializers.ModelSerializer):
    """JSON serializer for userBabies"""
    baby = BabySerializer(many=False)

    class Meta:
        model = UserBaby
        fields = ('id', 'baby')