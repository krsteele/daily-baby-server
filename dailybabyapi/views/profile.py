from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dailybabyapi.models import DailyUser
from dailybabyapi.models import DailyUserDay
from dailybabyapi.models import DayOfWeek


class Profile(ViewSet):
    """User can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info
        """
        dailyuser = DailyUser.objects.get(user=request.auth.user)
        dailyuser_days = DailyUserDay.objects.filter(user=dailyuser)

        dailyuser_days = DailyUserDaysSerializer(
            dailyuser_days, many=True, context={'request': request})
        dailyuser = DailyUserSerializer(
            dailyuser, many=False, context={'request': request})

        # Manually construct the JSON structure you want in the response
        profile = {}
        profile["dailyuser"] = dailyuser.data
        profile["dailyuser_days"] = dailyuser_days.data

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