from django.contrib.auth.models import User


def count_users():
    return User.objects.count()
