"""View module for handling requests about babies"""

from dailybabyapi.models.relationship import Relationship
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from django.contrib.auth.models import User
from dailybabyapi.models import DailyUser, user_baby
from dailybabyapi.models import Baby
from dailybabyapi.models import UserBaby

from datetime import date


class BabyView(ViewSet):
    """Daily Baby babies"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized baby instance
        """

        daily_user = DailyUser.objects.get(user=request.auth.user)

        baby = Baby()
        baby.first_name = request.data["firstName"]
        baby.middle_name = request.data["middleName"]
        baby.last_name = request.data["lastName"]
        baby.nickname = request.data["nickname"]
        baby.birth_date = request.data["birthdate"]
        baby.profile_image = request.data["profileImage"]
        baby.save()

        userBabyinstance = UserBaby()
        userBabyinstance.user = daily_user
        userBabyinstance.baby = baby
        userBabyinstance.relationship = Relationship.objects.get(pk=request.data["relationship"])
        userBabyinstance.save()

        try:    
            serializer = BabySerializer(baby, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
            

    def retrieve(self, request, pk=None):
        """Handle GET requests for single baby

        Returns:
            Response -- JSON serialized baby instance
        """

        daily_user = DailyUser.objects.get(user=request.auth.user)

        try:
            baby = Baby.objects.get(pk=pk)
                
            serializer = BabySerializer(baby, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a baby
        Returns:
            Response -- Empty body with 204 status code
        """
        baby = Baby.objects.get(pk=pk)
        baby.first_name = request.data["firstName"]
        baby.middle_name = request.data["middleName"]
        baby.last_name = request.data["lastName"]
        baby.nickname = request.data["nickname"]
        baby.birth_date = request.data["birthdate"]
        baby.profile_image = request.data["profileImage"]
        baby.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests for babies

            Returns:
                Response -- JSON serialized list of babies
        """

        dailyUser = DailyUser.objects.get(user=request.auth.user)

        babies = UserBaby.objects.filter(user = dailyUser)

        serializer = UserBabySerializer(babies, many=True, context={'request': request})
        return Response(serializer.data)



class BabySerializer(serializers.ModelSerializer):
    class Meta:
        model = Baby
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'nickname', 'birth_date', 'profile_image')

class UserBabySerializer(serializers.ModelSerializer):
    """JSON serializer for userBabies"""
    baby = BabySerializer(many=False)

    class Meta:
        model = UserBaby
        fields = ('baby', )
