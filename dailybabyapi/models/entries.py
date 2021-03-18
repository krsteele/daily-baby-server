from django.db import models


class Entry(models.Model):
    user_baby = models.ForeignKey("UserBaby", on_delete=models.CASCADE)
    prompt = models.ForeignKey("Prompt", on_delete=models.SET_NULL, null=True)
    created_on = models.DateField(auto_now=False, auto_now_add=False)
    text = models.CharField(max_length=1500)
    is_private = models.BooleanField(default=None)

    @property
    def by_current_user(self):
        return self.__by_current_user

    @by_current_user.setter
    def by_current_user(self, value):
        self.__by_current_user = value
    
    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, value):
        self.__comments = value
    
    @property
    def photos(self):
        return self.__photos

    @photos.setter
    def photos(self, value):
        self.__photos = value
