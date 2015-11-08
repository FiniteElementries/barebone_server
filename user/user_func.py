# general functions for user application, includes:
# create new user
# change user password
# authenticate user

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# todo list
# add encryption on password

def create_new_user(username, first_name, last_name, email, password):
    """
    create new user from information given
    :param username:
    :param first_name:
    :param last_name:
    :param email:
    :param password:
    :return: true or false, maybe user ID as well
    """
    # todo list
    # need to check if username already exist

    user=User.objects.create_user(username=username, email=email, password=password)
    user.first_name=first_name
    user.last_name=last_name

    user.save()

    return True

def change_user_pwd(username, new_password):
    """
    :param username:
    :param new_password:
    :return: true or false
    """
    # todo list
    # need to check for authorizaiton
    # need to check if user exist
    u = User.objects.get(username=username)
    u.set_password(new_password)
    u.save()
    return True


def user_authentication(username, password):
    """
    authenticate user
    :param username:
    :param password:
    :return: true or false
    """

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            print("User is valid, active and authenticated")
            return True
        else:
            print("The password is valid, but the account has been disabled!")
    else:
        # the authentication system was unable to verify the username and password
        print("The username and password were incorrect.")

    return False