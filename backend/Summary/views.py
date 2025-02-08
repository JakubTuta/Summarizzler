import Users.functions as users_functions
from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import functions, models, serializers


class Website(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest) -> Response:
        user: User = request.user  # type: ignore
        if (user_data := users_functions.find_user_data(user=user)) is None:
            return Response(
                {"message": "User data not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        request_data = request.data  # type: ignore
        required_fields = ["url", "prompt"]

        if len(
            missing_fields := functions.check_required_fields(
                request_data, required_fields
            )
        ):
            return Response(
                {"message": f"Missing fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        url = request_data["url"]
        user_prompt = request_data["prompt"]

        if (dom_content := functions.Website.get_dom_content(url)) is None:
            return Response(
                {"message": "Failed to scrape website"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (body_content := functions.Website.get_body_content(dom_content)) is None:
            return Response(
                {"message": "Failed to get body content"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cleaned_content = functions.Website.clean_body_content(body_content)
        bot_response = functions.Website.ask_bot(cleaned_content, user_prompt)

        if (title := functions.Website.get_title_for_content(dom_content)) is None:
            return Response(
                {"message": "Failed to get title for content"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "url": url,
            "title": title,
            "content_type": functions.Website.content_type,
            "summary": bot_response,
            "author": user_data,
            "user_prompt": user_prompt,
        }

        try:
            summary = functions.create_summary(data)
        except Exception as e:
            print(e)
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if summary is None:
            return Response(
                {"message": "Failed to create summary"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "id": summary.id,  # type: ignore
            },
            status=status.HTTP_200_OK,
        )
