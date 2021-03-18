"""View module for handling requests about entries"""

from dailybabyapi.models.daily_user import DailyUser
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from django.contrib.auth.models import User
from dailybabyapi.models import Entry, user_baby
from dailybabyapi.models import Prompt
from dailybabyapi.models import Comment
from dailybabyapi.models import UserBaby
from dailybabyapi.models import Baby
from dailybabyapi.models import EntryPhoto
from dailybabyapi.models import Photo

from datetime import date


class EntryView(ViewSet):
    """Daily Baby journal entries"""

    def create(self, request):
        """Handle POST requests to entry resource

            Returns:
                Response -- JSON serialized entry instance
        """
        # get the user via the auth token
        dailyUser = DailyUser.objects.get(user=request.auth.user)
        # get and format today's date
        today = date.today()
        created_on = today.strftime("%Y-%m-%d")
        # instantiate an Entry, assign values sent from client, save new Entry
        entry = Entry()
        entry.created_on = created_on
        entry.text = request.data["text"]
        entry.is_private = request.data["is_private"]
        prompt = Prompt.objects.get(pk=request.data["prompt"])
        entry.prompt = prompt
        userBaby = UserBaby.objects.get(user=dailyUser)
        entry.user_baby = userBaby
        entry.save()
        # instantiate a Photo, assign value sent from client, save new Photo
        pic = Photo()
        pic.image = request.data["image"]
        pic.save()
        # instantiate an EntryPhoto, assign values of newly created objects, save relationship
        entryPhoto = EntryPhoto()
        entryPhoto.photo = pic
        entryPhoto.entry = entry
        entryPhoto.save()

        try:
            serializer = EntrySerializer(entry, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for a single entry

            Returns:
                Response -- JSON serialized entry instance
        """

        dailyUser = DailyUser.objects.get(user=request.auth.user)

        try:
            entry = Entry.objects.get(pk=pk)

            if entry.user_baby.user == dailyUser: 
                entry.by_current_user = True
            else:
                entry.by_current_user = False

            serializer = EntrySerializer(entry, context={'request': request})
            return Response(serializer.data)
        
        except Exception as ex:
            return HttpResponseServerError(ex)

    
    def destroy(self, request, pk=None):
            """Handle DELETE requests for a single entry

            Returns:
                Response -- 200, 404, or 500 status code
            """
            try:
                entry = Entry.objects.get(pk=pk)
                entry.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except Entry.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """Handle GET requests for entries

            Returns:
                Response -- JSON serialized list of entries filtered by userbaby id
        """

        entries = Entry.objects.all()
        # dailyUser = DailyUser.objects.get(user=request.auth.user)
        
    
        # userBabyRelationships = UserBaby.objects.filter(user=dailyUser)

        #HALP! I need entries where entry.userbaby.user_id == dailyUser
        # can't figure out how to access that relationship. filter? for...in?

        ordered_entries = entries.order_by('created_on')

        serializer = EntrySerializer(
            ordered_entries, many=True, context={'request': request})
        return Response(serializer.data)



class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('id', 'user_baby', 'prompt', 'created_on', 'text', 'is_private', 'by_current_user')
        depth = 3
