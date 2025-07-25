from django.contrib.auth import get_user_model

User = get_user_model

def get_principal_from_central_db(user):
    return User.objects.using('default').get(pk=user.pk)