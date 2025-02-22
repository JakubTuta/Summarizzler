from django.http import HttpRequest
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import functions, serializers


class User(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request: HttpRequest, user_id: int) -> Response:
        if user_id != request.user.id:  # type: ignore
            return Response(
                {"message": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if (user_data := functions.find_user_data(user_id=user_id)) is None:
            return Response(
                {"message": "User data not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user_data_serializer = serializers.UserDataSerializer(user_data)

        return Response(
            {
                "user": user_data_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class Login(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest) -> Response:
        request_data = request.data  # type: ignore
        required_fields = ["password"]

        if len(
            missing_fields := functions.check_required_fields(
                request_data, required_fields
            )
        ):
            return Response(
                {"message": f"Missing fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = request_data.get("username", None)
        email = request_data.get("email", None)
        password = request_data["password"]

        if username is None and email is None:
            return Response(
                {"message": "Either username or email must be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (user := functions.find_user(email, username)) is None:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not functions.check_if_password_correct(user, password):
            return Response(
                {"message": "Incorrect password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if (user_data := functions.find_user_data(user=user)) is None:
            return Response(
                {"message": "User data not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if (tokens := functions.get_jwt_token(username, password)) is None:
            return Response(
                {"message": "Failed to get token"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user_data_serializer = serializers.UserDataSerializer(user_data)

        return Response(
            {
                "user": user_data_serializer.data,
                "tokens": tokens,
            },
            status=status.HTTP_200_OK,
        )


class Register(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest) -> Response:
        request_data = request.data  # type: ignore
        required_fields = ["email", "username", "password"]

        if len(
            missing_fields := functions.check_required_fields(
                request_data, required_fields
            )
        ):
            return Response(
                {"message": f"Missing fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = request_data["email"]
        username = request_data["username"]
        password = request_data["password"]

        if functions.find_user(email, username) is not None:
            return Response(
                {"message": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = functions.create_user(email, username, password)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if user is None:
            return Response(
                {"message": "Failed to create user"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            user_data = functions.create_user_data(user)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if user_data is None:
            return Response(
                {"message": "Failed to create user data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if (tokens := functions.get_jwt_token(username, password)) is None:
            return Response(
                {"message": "Failed to get token"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user_data_serializer = serializers.UserDataSerializer(user_data)

        return Response(
            {
                "user": user_data_serializer.data,
                "tokens": tokens,
            },
            status=status.HTTP_201_CREATED,
        )
