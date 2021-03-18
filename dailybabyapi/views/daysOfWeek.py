"""View module for handling requests about days of the week"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dailybabyapi.models import DayOfWeek, days_of_week

class DaysOfWeek(ViewSet):
    
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

