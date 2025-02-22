import io

import Users.functions as users_functions
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from PyPDF2 import PdfReader
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import functions, models, serializers


def with_required_fields(required_fields):
    def decorator(view_func):
        def wrapper(self, request, *args, **kwargs):
            request_data = request.data
            if len(
                missing_fields := functions.check_required_fields(
                    request_data, required_fields
                )
            ):
                return Response(
                    {"message": f"Missing fields: {', '.join(missing_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return view_func(self, request, *args, **kwargs)

        return wrapper

    return decorator


class WebsiteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @with_required_fields(["url", "prompt"])
    def post(self, request: HttpRequest) -> Response:
        request_data = request.data  # type: ignore
        url = request_data["url"]
        user_prompt = request_data["prompt"]

        if (user_data := users_functions.find_user_data(user=request.user)) is None:  # type: ignore
            return Response(
                {"message": "Failed to get user data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
        title = functions.Website.get_title_for_content(dom_content)

        data = {
            "url": url,
            "title": title if title is not None else bot_response["title"],
            "content_type": functions.Website.content_type,
            "summary": bot_response["content"],
            "author": user_data,
            "user_prompt": user_prompt,
            "is_private": request_data.get("private", False),
            "tags": bot_response["tags"][:5],
            "category": bot_response["category"],
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
                "id": str(summary.id),  # type: ignore
            },
            status=status.HTTP_200_OK,
        )


class TextView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @with_required_fields(["text", "prompt"])
    def post(self, request: HttpRequest):
        request_data = request.data  # type: ignore
        input_text = request_data["text"]
        user_prompt = request_data["prompt"]

        if (user_data := users_functions.find_user_data(user=request.user)) is None:  # type: ignore
            return Response(
                {"message": "Failed to get user data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bot_response = functions.Text.ask_bot(input_text, user_prompt)

        data = {
            "title": bot_response["title"],
            "content_type": functions.Text.content_type,
            "summary": bot_response["content"],
            "author": user_data,
            "user_prompt": user_prompt,
            "is_private": request_data.get("private", False),
            "tags": bot_response["tags"],
            "category": bot_response["category"],
            "raw_text": input_text,
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
                "id": str(summary.id),  # type: ignore
            },
            status=status.HTTP_200_OK,
        )


class FileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @with_required_fields(["prompt"])
    def post(self, request: HttpRequest) -> Response:
        request_data = request.data  # type: ignore
        user = request.user  # type: ignore
        file = request.FILES.get("file")
        prompt = request_data.get("prompt")
        is_private = request_data.get("private", False)

        if not file:
            return Response(
                {"message": "No file uploaded"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not file.name.endswith(".pdf"):
            return Response(
                {"message": "Invalid file type. Only PDF files are supported."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            file_content = ""
            pdf_reader = PdfReader(io.BytesIO(file.read()))
            for page in pdf_reader.pages:
                file_content += page.extract_text()

            file_content = file_content.strip()

            bot_response = functions.File.process_file_content(file_content, prompt)

            data = {
                "title": file.name.split(".pdf")[0],
                "content_type": functions.File.content_type,
                "summary": bot_response["content"],
                "author": user,
                "user_prompt": prompt,
                "is_private": is_private,
                "tags": bot_response["tags"],
                "category": bot_response["category"],
                "raw_text": file_content,
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
                    "id": str(summary.id),  # type: ignore
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": f"Error processing file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SummaryList(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request: HttpRequest) -> Response:
        query_params = request.query_params  # type: ignore

        try:
            limit = int(query_params.get("limit", 10))

        except ValueError:
            return Response(
                {"message": "Invalid limit value"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sort_param = query_params.get("sort", "date")
        start_after_id = query_params.get("startAfter", None)
        content_type = query_params.get("contentType", None)
        category = query_params.get("category", None)

        summaries: BaseManager[models.Summary] = models.Summary.objects.all()
        summaries = functions.sort_summaries(summaries, sort_param)
        summaries = functions.filter_by_start_after(
            summaries, start_after_id, sort_param
        )
        summaries = functions.filter_by_content_type(summaries, content_type)
        summaries = functions.filter_by_category(summaries, category)

        if request.user.is_authenticated and (user := users_functions.find_user_data(user=request.user)):  # type: ignore
            me_param = query_params.get("me", "false")
            private_param = query_params.get("private", None)

            if me_param.lower() == "true":
                summaries = summaries.filter(author=user)

            if private_param is not None and private_param.lower() == "true":
                summaries = summaries.filter(author=user, is_private=True)

            elif private_param is not None and private_param.lower() == "false":
                summaries = summaries.filter(is_private=False)

        else:
            summaries = summaries.filter(is_private=False)

        summaries = summaries[:limit]
        serializer = serializers.SummaryPreviewSerializer(summaries, many=True)
        serializer_data = serializer.data
        for item in serializer_data:
            item["id"] = str(item["id"])

        return Response(serializer_data, status=status.HTTP_200_OK)


class SummaryDetail(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated()]

        return [AllowAny()]

    def get(self, request: HttpRequest, id: int) -> Response:
        user_data = None
        if request.user.is_authenticated:
            user_data = users_functions.find_user_data(user=request.user)  # type: ignore

        try:
            summary = models.Summary.objects.get(id=id)

            if (
                not summary.is_private
                and user_data is not None
                and user_data != summary.author
            ):
                return Response(
                    {"message": "Summary is private"}, status=status.HTTP_403_FORBIDDEN
                )

        except models.Summary.DoesNotExist:
            return Response(
                {"message": "Summary not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.SummarySerializer(summary)
        serializer_data = serializer.data
        serializer_data["id"] = str(serializer_data["id"])

        return Response(serializer_data, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, id: int) -> Response:
        if not request.user.is_authenticated:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if (user_data := users_functions.find_user_data(user=request.user)) is None:  # type: ignore
            return Response(
                {"message": "Failed to get user data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            summary = models.Summary.objects.get(id=id)
        except models.Summary.DoesNotExist:
            return Response(
                {"message": "Summary not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if summary.author != user_data:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        summary.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request: HttpRequest) -> Response:
        query_params = request.query_params  # type: ignore

        try:
            limit = int(query_params.get("limit", 5))
        except ValueError:
            return Response(
                {"message": "Invalid limit value"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (search_query := query_params.get("query", None)) is None:
            return Response(
                {"message": "Missing query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        format_query = search_query.lower().strip()

        summaries = models.Summary.objects.filter(
            Q(title__icontains=format_query) | Q(tags__icontains=format_query)
        )
        summaries = summaries[:limit]

        serializer = serializers.SummaryPreviewSerializer(summaries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
