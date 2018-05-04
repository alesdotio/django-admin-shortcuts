from django.contrib.auth.models import User, Group


def count_users():
    return User.objects.count()


def count_groups():
    return Group.objects.count()


def has_perms_to_users(request):
    return request.user.is_authenticated and request.user.is_superuser
