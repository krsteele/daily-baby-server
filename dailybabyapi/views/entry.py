"""View module for handling requests about entries"""

from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from django.contrib.auth.models import User
from dailybabyapi.models.daily_user import DailyUser
from dailybabyapi.models import Entry, user_baby
from dailybabyapi.models import Prompt
from dailybabyapi.models import Comment
from dailybabyapi.models import UserBaby
from dailybabyapi.models import Baby
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
        baby = Baby.objects.get(pk=request.data["babyId"])
        userBaby = UserBaby.objects.get(user=dailyUser, baby=baby)
        entry.user_baby = userBaby
        entry.save()
        # instantiate a Photo, assign value sent from client, save new Photo
        pic = Photo()
        pic.image = request.data["image"]
        pic.entry = entry
        pic.save()

        return Response({}, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pk=None):
        """Handle GET requests for a single entry

            Returns:
                Response -- JSON serialized entry instance
        """
        # get the current user
        dailyUser = DailyUser.objects.get(user=request.auth.user)

        try:
            # get the requested entry
            entry = Entry.objects.get(pk=pk)
            # get the comments for the requested entry
            entryComments = Comment.objects.filter(entry=entry)
            # if there are comments for the entry, add them
            if entryComments.count() > 0:
                entry.comments = entryComments
            # if not, empty list
            else:
                entry.comments = []
            # if the current user created this entry
            if entry.user_baby.user == dailyUser: 
                entry.by_current_user = True
            # if not
            else:
                entry.by_current_user = False
            # Is there a photo with a matching entry
            try:
                entryPhoto = Photo.objects.get(entry=entry)
                entry.photo = entryPhoto
            # If no photo
            except Photo.DoesNotExist as ex:
                pass
            # # Get the baby that matches this entry's user_baby
            # baby = Baby.objects.get(baby=entry.user_baby.baby)
            # Serialize needed data
            # dailyUser = DailyUserSerializer(dailyUser, many=False, context={'request': request})
            requestedEntry = EntrySerializer(entry, context={'request': request})
            # Contruct the JSON structure for the response

            return Response(requestedEntry.data)
        
        except Exception as ex:
            return HttpResponseServerError(ex)


    def update(self, request, pk=None):
        """Handle PUT operations

            Returns:
                Response -- 204_NO_CONTENT
        """

        # get the user via the auth token
        dailyUser = DailyUser.objects.get(user=request.auth.user)
        entry = Entry.objects.get(pk=pk)
        entry.created_on = request.data["created_on"]
        entry.text = request.data["text"]
        entry.is_private = request.data["is_private"]

        try:
            prompt = Prompt.objects.get(pk=request.data["prompt"])
            entry.prompt = prompt
        except Prompt.DoesNotExist:
            entry.prompt = None

        userBaby = UserBaby.objects.get(pk=request.data["userBaby"])
        entry.user_baby = userBaby
        entry.save()
        # find and delete photo with same entry id
        Photo.objects.filter(entry=entry).delete()
        # instantiate a Photo, assign value sent from client, save new Photo
        pic = Photo()
        pic.image = request.data["image"]
        pic.entry = entry
        pic.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    
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
        baby= Baby.objects.get(pk=request.query_params['babyId'])
    
        entries = Entry.objects.filter(user_baby__baby=baby).order_by('-created_on')

        for entry in entries:
            try:
                entryPhoto = Photo.objects.get(entry=entry)
                entry.photo = entryPhoto
            # If no photo
            except Photo.DoesNotExist as ex:
                entry.photo = None

        serializer = EntryListSerializer(
            entries, many=True, context={'request': request})
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for dailyuser's related Django user"""
    class Meta:
        model = User
        fields = ('username',)

class DailyUserSerializer(serializers.ModelSerializer):
    """JSON serializer for dailyuser"""
    user = UserSerializer(many=False)

    class Meta:
        model = DailyUser
        fields = ('user', 'profile_image')

class BabySerializer(serializers.ModelSerializer):
    """JSON serializer for baby"""
    class Meta:
        model = Baby
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'nickname', 'profile_image')

class UserBabySerializer(serializers.ModelSerializer):
    """JSON serializer for userBabies"""
    baby = BabySerializer(many=False)
    user = DailyUserSerializer(many=False)

    class Meta:
        model = UserBaby
        fields = ('id', 'baby', 'user', 'relationship')

class PhotoSerializer(serializers.ModelSerializer):
    """JSON serializer for photo"""
    class Meta:
        model = Photo
        fields = ('image',)

class CommentsSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    class Meta:
        model = Comment
        fields = ('id', 'user_baby', 'created_on', 'content')

class EntrySerializer(serializers.ModelSerializer):
    photo = PhotoSerializer(many=False)
    comments = CommentsSerializer(many=True)
    user_baby = UserBabySerializer(many=False)

    class Meta:
        model = Entry
        fields = ('id', 'user_baby', 'prompt', 'created_on', 'text', 'is_private', 'photo', 'by_current_user', 'comments')

class EntryListSerializer(serializers.ModelSerializer):
    photo = PhotoSerializer(many=False)
    user_baby = UserBabySerializer(many=False)

    class Meta:
        model = Entry
        fields = ('id', 'user_baby', 'prompt', 'created_on', 'text', 'is_private', 'photo')
