from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from dailybabyapi.models import DailyUser


class Users(ViewSet):
    
    def update(self, request, pk=None):
        dailyUser = DailyUser.objects.get(user=request.auth.user)
        dailyUser.user.first_name = request.data["firstName"]
        dailyUser.user.last_name = request.data["lastName"]
        dailyUser.user.email = request.data["email"]
        #password??? other fields???
        dailyUser.text_time = request.data["textTime"]
        dailyUser.phone_number = request.data["phone"]
        dailyUser.profile_image = request.data["profileImage"]

        dailyUser.user.save()
        dailyUser.save()

        # I'll have seven checkboxes with the days of the week. How do I make sure that 
        # if they uncheck a box, that the DailyUserDays join table instance is deleted? 
        # I can iterate through the list and create an instance for days of the week that 
        # checked, but how do I make sure to find and delete the others?

        return Response({}, status=status.HTTP_204_NO_CONTENT)
        




# class DailyUserSerializer(serializers.ModelSerializer):
#     """JSON serializer for user"""
#     class Meta:
#         model=DailyUser
#         fields=('id', 'user', 'text_time', 'phone_number', 'profile_image')
#         depth=1