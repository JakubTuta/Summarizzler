import os
import typing

from bs4 import BeautifulSoup
from django.db.models.manager import BaseManager
from django.http import QueryDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from playwright.sync_api import sync_playwright

from . import models, serializers


def check_required_fields(
    data: typing.Dict[str, str] | QueryDict, required_fields: typing.List[str]
) -> list[str]:
    missing_fields = [field for field in required_fields if field not in data]

    return missing_fields


def create_summary(data: typing.Dict[str, str]) -> typing.Optional[models.Summary]:
    serializer = serializers.SummarySerializer(data=data)

    if not serializer.is_valid():
        error_message = ", ".join(
            [error_detail[0].__str__() for error_detail in serializer.errors.values()]  # type: ignore
        )

        raise Exception(error_message)

    serializer.save()

    if isinstance(serializer.instance, models.Summary):
        return serializer.instance


def get_langchain_template(content_type: str) -> str:
    match content_type:
        case "website":
            return (
                "You are tasked with extracting specific information from the following text content: {dom_content}. "
                "Please follow these instructions carefully: \n\n"
                "1. **Extract Information:** Only extract the information that directly matches the provided description: {user_prompt}. "
                "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
                "3. **Empty Response:** If no information matches the description, return an empty string ('')."
                "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
            )

        case _:
            return ""


def sort_summaries(
    summaries: BaseManager[models.Summary], sort_by: str
) -> BaseManager[models.Summary]:
    match sort_by:
        case "date":
            return summaries.order_by("-created_at")
        case "likes":
            return summaries.order_by("-likes")
        case "favorites":
            return summaries.order_by("-favorites")
        case _:
            return summaries


def filter_by_start_after(
    summaries: BaseManager[models.Summary], start_after: typing.Optional[str], sort: str
) -> BaseManager[models.Summary]:
    print(start_after)
    print(sort)
    if start_after is None:
        return summaries

    if (summary := get_summary_by_id(start_after)) is not None:
        print(summary)
        match sort:
            case "date":
                summaries = summaries.filter(
                    created_at__lt=summary.created_at
                ).order_by("-created_at")

            case "likes":
                summaries = summaries.filter(likes__lt=summary.likes).order_by("-likes")

            case "favorites":
                summaries = summaries.filter(favorites__lt=summary.favorites).order_by(
                    "-favorites"
                )

    return summaries


def get_summary_by_id(summary_id: str) -> typing.Optional[models.Summary]:
    try:
        summary = models.Summary.objects.get(id=summary_id)

        return summary
    except models.Summary.DoesNotExist:
        return None


class Website:
    content_type = "website"

    @staticmethod
    def get_dom_content(url: str) -> typing.Optional[str]:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url, timeout=60000)
                page.wait_for_selector("body", timeout=30000)
                dom_content = page.content()
                browser.close()

                return dom_content

        except Exception as e:
            print(f"Playwright scraping failed: {e}")

            return None

    @staticmethod
    def get_body_content(dom_content: str) -> typing.Optional[str]:
        soup = BeautifulSoup(dom_content, "html.parser")
        body_content = soup.body

        if body_content:
            return str(body_content)

        return None

    @staticmethod
    def clean_body_content(body_content: str) -> str:
        soup = BeautifulSoup(body_content, "html.parser")

        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()

        cleaned_content = soup.get_text(separator="\n")
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )

        return cleaned_content

    @staticmethod
    def get_title_for_content(dom_content: str) -> typing.Optional[str]:
        soup = BeautifulSoup(dom_content, "html.parser")

        if (head := soup.head) is not None and (title := head.title) is not None:
            return title.string

        return None

    @staticmethod
    def ask_bot(content: str, user_prompt: str) -> str:
        api_key = os.environ.get("GEMINI_API_KEY")

        model = ChatGoogleGenerativeAI(
            api_key=api_key,  # type: ignore
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        template = get_langchain_template(Website.content_type)
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model

        response = chain.invoke({"dom_content": content, "user_prompt": user_prompt})

        return str(response.content)
