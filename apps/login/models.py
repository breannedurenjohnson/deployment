from __future__ import unicode_literals
from django.db import models
import re
# from datetime import datetime, date

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        FIRST_NAME_REGEX = re.compile('[a-zA-Z]')
        if not FIRST_NAME_REGEX.match(postData['first_name']) or len(postData['first_name']) < 2: 
            errors['valid_first_name'] = "Please enter a valid first name."
            print(errors)
        LAST_NAME_REGEX = re.compile('[a-zA-Z]')
        if not LAST_NAME_REGEX.match(postData['last_name']) or len(postData['last_name']) < 2:
            errors['valid_last_name'] = "Please enter a valid last name."
            print(errors)
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):             
            errors['valid_email'] = "Invalid email address."
        users = User.objects.filter(email = postData['email'])
        if len(users) > 0:
            errors['email_duplicate'] = "Email is already taken."
        if len(postData['password']) < 8:
            errors['password_length'] = "Password is too short."
            print(errors)        
        if postData['password'] != postData['password_conf']:
            errors['password_match'] = "Password and password confirmation do not match."
        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['quote']) < 10:
            errors['quote_length'] = "Quote is too short."
            print(errors)
        if len(postData['author']) < 2:
            errors['author_length'] = "'Quoted by' field is too short."
            print(errors)
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="quotes")
    users_who_like = models.ManyToManyField(User, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()