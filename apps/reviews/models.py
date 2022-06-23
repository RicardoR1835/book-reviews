from __future__ import unicode_literals
from django.db import models
import re
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        context = {
            "users": User.objects.all()
        }
        grab = User.objects.filter(email=postData['email'])
        print("in basic validator grab: ", grab)
        print("*" * 80)
        if len(postData["fn"]) < 2:
            errors["fn"] = "First name should be more than 2 characters"
        if len(postData['ln']) < 2:
            errors['ln'] = "Last name should be more than 2 characters"
        if not EMAIL_REGEX.match(postData["email"]):
            errors['email'] = "Email not entered in valid form"
        if len(grab) > 0:
            errors['email'] = "Email already exists"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Passwords do not match!"
        return errors

    def login_validator(self, postData):
        errors = {}
        context = {
            "users": User.objects.all()
        }
        email = User.objects.filter(email=postData['email'])
        print(email)
        if len(email) == 0:
            errors["emaillog"] = "Email is not registered"
        else:
            user = User.objects.get(email=postData['email'])
            if user.password != postData['password']:
                errors['pwlog'] = "Password does not match"
        return errors


class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        context = {
            "books": Book.objects.all()
        }
        grab = Book.objects.filter(title=postData['title'])
        if len(postData['title']) < 2:
            errors['title'] = "Title must be at least 2 characters long"
        if len(postData['review']) < 2:
            errors['review'] = "Review must have at least 2 characters"
        if len(grab) > 0:
            errors['books'] = "Book already registered"
        return errors

class AuthorManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        context = {
            "authors": Author.objects.all()
        }
        grab = Author.objects.filter(name=postData['add_author'])
        if len(postData['add_author']) < 2:
            errors['name'] = "Name must be at least 2 characters long"
        if len(grab) > 0:
            errors['books'] = "Author already registered"
        return errors

class RatingManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        context = {
            "ratings": Rating.objects.all()
        }
        if len(postData['review']) < 2:
            errors['name'] = "Review must be at least 2 characters long"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
    def __repr__(self):
        return f"<Users object: {self.id} ({self.email})>"

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = AuthorManager()
    def __repr__(self):
        return f"<Authors object: {self.id} ({self.name})>"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()
    def __repr__(self):
        return f"<Books object: {self.id} ({self.title})>"

class Rating(models.Model):
    rating = models.IntegerField()
    review = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, related_name="my_ratings", on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, related_name="ratings", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = RatingManager()
    def __repr__(self):
        return f"<Rating object: {self.id}>"
