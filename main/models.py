from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.
class NewUser(AbstractUser):
    profile_pic = models.ImageField(upload_to='pictures', default='default.jpg')

    # def __str__(self):
    #     return User.username


class Post(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    # pic = models.ImageField(upload_to='pictures', default='not_found.png')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(default='no name', max_length=50)
    comment = models.CharField(max_length=400)

    def __str__(self):
        return self.name + "=>" + self.comment
