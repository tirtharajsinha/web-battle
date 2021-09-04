from django.db import models
from django.db.models.base import Model

# Create your models here.


class userdetail(models.Model):

    username = models.CharField(max_length=112, unique=True)
    title = models.CharField(max_length=112)
    bio = models.TextField()
    pic = models.ImageField(
        default="", upload_to="profiles")
    website = models.CharField(max_length=112, default="")
    instagram = models.CharField(
        max_length=112, default="")

    twitter = models.CharField(max_length=112, default="")
    objects = models.Manager()


class blog(models.Model):
    username = models.CharField(max_length=112)
    title = models.CharField(max_length=112)

    des = models.TextField()
    public = models.CharField(max_length=50, default="public")
    thumb = models.ImageField(
        default="", upload_to="thumbnail")
    blog = models.TextField()

    objects = models.Manager()


class bookmark(models.Model):
    username = models.CharField(max_length=112)
    blogid = models.IntegerField()
    objects = models.Manager()
