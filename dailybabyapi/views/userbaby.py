"""View module for handling requests about userbaby relationships"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers

from django.contrib.auth.models import User
from dailybabyapi.models import UserBaby
from dailybabyapi.models import Baby
from dailybabyapi.models import Relationship

class UserBaby( ViewSet):
    
    def list(self, request):
        """Handle GET requests to days_of_week resource

        Returns:
            Response -- JSON serialized list of days of the week
        """

        # Get all days of week records from the database
        days = DayOfWeek.objects.all()

        serializer = DaySerializer(
            days, many=True, context={'request': request}
        )
        return Response(serializer.data)

class DaySerializer(serializers.ModelSerializer):
    """JSON serializer for days"""
    class Meta:
        model = DayOfWeek
        fields = ('id', 'day')