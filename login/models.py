from django.db import models
from mongoengine.django.auth import User
from mongoengine import *
# Create your models here.

class Usuario(User):
    perm = ListField(StringField())