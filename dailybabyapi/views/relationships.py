"""View module for handling requests about relationships"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from dailybabyapi.models import Relationship

class RelationshipView(ViewSet):
    
    def list(self, request):
        """Handle GET requests to relationship resource

        Returns:
            Response -- JSON serialized list of relationships
        """

        # Get all relationship records from the database
        relationships = Relationship.objects.all()

        serializer = RelationshipSerializer(
            relationships, many=True, context={'request': request}
        )
        return Response(serializer.data)

class RelationshipSerializer(serializers.ModelSerializer):
    """JSON serializer for relationships"""
    class Meta:
        model = Relationship
        fields = ('id', 'type')