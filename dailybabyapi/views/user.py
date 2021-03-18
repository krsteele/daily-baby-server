from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from dailybabyapi.models import DailyUser
from dailybabyapi.models import DailyUserDay
from dailybabyapi.models import DayOfWeek


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
        #password??? other fields???
        dailyUser.text_time = request.data["textTime"]
        dailyUser.phone_number = request.data["phone"]
        dailyUser.profile_image = request.data["profileImage"]

        dailyUser.user.save()
        dailyUser.save()

        DailyUserDay.objects.filter(user=dailyUser).delete()

        listOfDays = request.data["daysOfWeek"]
        
        for day in listOfDays:
            chosenDay = DayOfWeek.objects.get(pk=day)
            userDay = DailyUserDay()
            userDay.day = chosenDay
            userDay.user = dailyUser
            userDay.save()

 
        return Response({}, status=status.HTTP_204_NO_CONTENT)
        




# class DailyUserSerializer(serializers.ModelSerializer):
#     """JSON serializer for user"""
#     class Meta:
#         model=DailyUser
#         fields=('id', 'user', 'text_time', 'phone_number', 'profile_image')
#         depth=1