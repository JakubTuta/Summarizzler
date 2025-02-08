import os
import typing

import requests
from django.contrib.auth.models import User
from django.http import QueryDict

from . import models, serializers


def check_required_fields(
    data: typing.Dict[str, str] | QueryDict, required_fields: typing.List[str]
) -> list[str]:
    missing_fields = [field for field in required_fields if field not in data]

    return missing_fields


def find_user(
    email: typing.Optional[str] = None,
    username: typing.Optional[str] = None,
    user_id: typing.Optional[int] = None,
) -> typing.Optional[User]:
    if user_id is not None:
        return User.objects.get(id=user_id)

    if email is not None:
        return User.objects.get(email=email)

    elif username is not None:
        return User.objects.get(username=username)


def find_user_data(
    user: typing.Optional[User] = None, user_id: typing.Optional[int] = None
) -> typing.Optional[models.UserData]:
    if user is not None:
        return models.UserData.objects.get(user=user)

    elif user_id is not None:
        return models.UserData.objects.get(user=user_id)


def check_if_password_correct(user: User, password: str) -> bool:
    return user.check_password(password)


def create_user(email: str, username: str, password: str) -> typing.Optional[User]:
    data = {
        "email": email,
        "username": username,
        "password": password,
    }

    serializer = serializers.UserSerializer(data=data)

    if not serializer.is_valid():
        error_message = ", ".join(
            [error_detail[0].__str__() for error_detail in serializer.errors.values()]  # type: ignore
        )
        raise Exception(error_message)

    serializer.save()

    if isinstance(serializer.instance, User):
        return serializer.instance


def create_user_data(user: User) -> typing.Optional[models.UserData]:
    data = {}
    serializer = serializers.UserDataSerializer(data=data, context={"user": user})

    if not serializer.is_valid():
        error_message = ", ".join(
            [error_detail[0].__str__() for error_detail in serializer.errors.values()]  # type: ignore
        )
        raise Exception(error_message)

    serializer.save()

    if isinstance(serializer.instance, models.UserData):
        return serializer.instance


def get_jwt_token(
    username: str, password: str
) -> typing.Optional[typing.Dict[str, str]]:
    base_url = os.getenv("SERVER_URL")
    url = f"{base_url}/auth/token/"

    data = {
        "username": username,
        "password": password,
    }
    response = requests.post(url, data=data)

    if response.status_code != 200:
        return None

    response_data = response.json()
    tokens = {
        "access": response_data["access"],
        "refresh": response_data["refresh"],
    }

    return tokens


def refresh_token(token: str) -> typing.Optional[typing.Dict[str, str]]:
    base_url = os.getenv("SERVER_URL")
    url = f"{base_url}/auth/token/refresh/"

    data: dict[str, str] = {
        "refresh": token,
    }
    response: requests.Response = requests.post(url, data=data)

    if response.status_code != 200:
        return None

    response_data = response.json()
    tokens = {
        "access": response_data["access"],
        "refresh": response_data["refresh"],
    }

    return tokens


def verify_token(token: str) -> bool:
    base_url = os.getenv("SERVER_URL")
    url = f"{base_url}/auth/token/verify/"

    data: dict[str, str] = {
        "token": token,
    }

    response: requests.Response = requests.post(url, data=data)

    return response.status_code == 200
