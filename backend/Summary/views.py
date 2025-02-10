import Users.functions as users_functions
import Users.serializers as users_serializers
from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import functions, models, serializers


class Website(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: HttpRequest) -> Response:
        # url: /summary/website/

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
            "is_private": request_data.get("private", False),
        }

        try:
            summary = functions.create_summary(data)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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


class SummaryList(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request: HttpRequest) -> Response:
        try:
            limit = int(request.query_params.get("limit", 10))  # type: ignore

        except ValueError:
            return Response(
                {"message": "Invalid limit value"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        summaries = models.Summary.objects.all().order_by(
            "-favorites", "-likes", "-created_at"
        )

        if request.user.is_authenticated and (user := users_functions.find_user_data(user=request.user)) is not None:  # type: ignore
            query_params = request.query_params  # type: ignore
            me_param = query_params.get("me", "false")
            private_param = query_params.get("private", "all")

            if me_param == "true":
                summaries = summaries.filter(author=user)

            if private_param == "true":
                summaries = summaries.filter(author=user, is_private=True)

            elif private_param == "false":
                summaries = summaries.filter(is_private=False)

        else:
            summaries = summaries.filter(is_private=False)

        summaries = summaries[:limit]
        serializer = serializers.SummarySerializer(summaries, many=True)

        return_data = [
            {
                **summary,
                "author": (
                    users_serializers.UserDataSerializer(author).data
                    if author
                    else None
                ),
            }
            for summary in serializer.data
            if (author := users_functions.find_user_data(user=summary["author"]))
            is not None
            or not summary["author"]
        ]

        return Response(return_data, status=status.HTTP_200_OK)


class SummaryDetail(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request: HttpRequest, id: int) -> Response:
        user = None
        if request.user.is_authenticated:
            user = User(request.user)

        try:
            summary = models.Summary.objects.get(id=id)

            if not summary.is_private and user is not None and user != summary.author:
                return Response(
                    {"message": "Summary is private"}, status=status.HTTP_403_FORBIDDEN
                )

        except models.Summary.DoesNotExist:
            return Response(
                {"message": "Summary not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.SummarySerializer(summary)

        return Response(serializer.data, status=status.HTTP_200_OK)
