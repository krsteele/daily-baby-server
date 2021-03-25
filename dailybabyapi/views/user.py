from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from dailybabyapi.models import DailyUser


class Users(ViewSet):
    
    def update(self, request, pk=None):
        """Handle PUT operations

            Returns:
                Response -- 204_NO_CONTENT
        """

        dailyUser = DailyUser.objects.get(user=request.auth.user)
        dailyUser.user.first_name = request.data["firstName"]
        dailyUser.user.last_name = request.data["lastName"]
        dailyUser.user.email = request.data["email"]

        dailyUser.text_time = request.data["textTime"]
        dailyUser.phone_number = request.data["phone"]
        dailyUser.profile_image = request.data["profileImage"]
        dailyUser.monday = request.data["monday"]
        dailyUser.tuesday = request.data["tuesday"]
        dailyUser.wednesday = request.data["wednesday"]
        dailyUser.thursday = request.data["thursday"]
        dailyUser.friday = request.data["friday"]
        dailyUser.saturday = request.data["saturday"]
        dailyUser.sunday = request.data["sunday"]

        dailyUser.user.save()
        dailyUser.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        print("request", request.data)
        dailyuser = DailyUser.objects.get(user=request.auth.user)
        
        for key in request.data:
            setattr(dailyuser, key, request.data[key])

        dailyuser.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
        