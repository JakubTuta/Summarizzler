import os
import typing

import pydantic
import requests
from bs4 import BeautifulSoup
from django.db.models.manager import BaseManager
from django.http import QueryDict
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from . import models, serializers

langchain_template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Format the response in this JSON format: {format_instructions}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** If not stated otherwise by user, keep the response long, detailed and informative. Only extract the information that directly matches the provided description: {user_prompt}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    "5. **Format response:** Add to your response html tags like <br> for line breaks, <p> for paragraphs, <h1> for headers, <strong> for bold text, <em> for italic text, <a> for links, <ul> for unordered lists, <ol> for ordered lists, <li> for list items, <table> for tables, <tr> for table rows, <th> for table headers, <td> for table cells, to make the response more clean and readable."
)


def check_required_fields(
    data: typing.Dict[str, str] | QueryDict, required_fields: typing.List[str]
) -> list[str]:
    missing_fields = [field for field in required_fields if field not in data]

    return missing_fields


def create_summary(data: typing.Dict[str, str]) -> typing.Optional[models.Summary]:
    serializer = serializers.SummarySerializer(
        data=data, context={"author": data["author"]}
    )

    if not serializer.is_valid():
        error_message = ", ".join(
            [error_detail[0].__str__() for error_detail in serializer.errors.values()]  # type: ignore
        )

        raise Exception(error_message)

    serializer.save()

    if isinstance(serializer.instance, models.Summary):
        return serializer.instance


def sort_summaries(
    summaries: BaseManager[models.Summary], sort_by: str
) -> BaseManager[models.Summary]:
    match sort_by.lower():
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
    if start_after is None:
        return summaries

    if (summary := get_summary_by_id(start_after)) is not None:
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


def filter_by_content_type(
    summaries: BaseManager[models.Summary], content_type: typing.Optional[str]
) -> BaseManager[models.Summary]:
    if content_type is None:
        return summaries

    return summaries.filter(content_type=content_type.lower())


def filter_by_category(
    summaries: BaseManager[models.Summary], category: typing.Optional[str]
) -> BaseManager[models.Summary]:
    if category is None:
        return summaries

    return summaries.filter(category=category.lower())


def get_summary_by_id(summary_id: str) -> typing.Optional[models.Summary]:
    try:
        summary = models.Summary.objects.get(id=summary_id)

        return summary
    except models.Summary.DoesNotExist:
        return None


def get_api_key(model: str = "GEMINI"):
    match model.upper():
        case "GEMINI":
            return os.environ.get("GEMINI_API_KEY")
        case "OPENAI":
            return os.environ.get("OPENAI_API_KEY")


categories = [
    "technology",
    "business",
    "health & wellness",
    "education",
    "lifestyle",
    "entertainment",
    "science",
    "politics",
    "art & culture",
    "sports",
    "food & drink",
    "travel",
    "other",
]


class BotResponse(pydantic.BaseModel):
    title: str = pydantic.Field(description="The title of the content")
    content: str = pydantic.Field(description="The answer to the user's query")
    tags: typing.List[str] = pydantic.Field(description="Max 5 tags for the summary")
    category: str = pydantic.Field(
        description=f"The category of the content. Choose one from the list: [{', '.join(categories)}]"
    )


class Website:
    content_type = "website"

    @staticmethod
    def get_dom_content(url: str) -> typing.Optional[str]:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response: requests.Response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            return response.text

        except requests.exceptions.RequestException:
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
    def ask_bot(content: str, user_prompt: str) -> dict[str, str]:
        model = ChatGoogleGenerativeAI(
            api_key=get_api_key(),  # type: ignore
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        parser = JsonOutputParser(pydantic_object=BotResponse)

        prompt = PromptTemplate(
            template=langchain_template,
            input_variables=["dom_content", "user_prompt"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | model | parser

        response = chain.invoke({"dom_content": content, "user_prompt": user_prompt})

        for category in categories:
            if response["category"] in category:
                response["category"] = category
                break

        return response


class Text:
    content_type = "text"

    @staticmethod
    def ask_bot(content: str, user_prompt: str) -> dict[str, str]:
        model = ChatGoogleGenerativeAI(
            api_key=get_api_key(),  # type: ignore
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        parser = JsonOutputParser(pydantic_object=BotResponse)

        prompt = PromptTemplate(
            template=langchain_template,
            input_variables=["dom_content", "user_prompt"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | model | parser

        response = chain.invoke({"dom_content": content, "user_prompt": user_prompt})

        for category in categories:
            if response["category"] in category:
                response["category"] = category
                break

        return response


class File:
    content_type = "file"

    @staticmethod
    def process_file_content(file_content: str, user_prompt: str) -> dict[str, str]:
        model = ChatGoogleGenerativeAI(
            api_key=get_api_key(),  # type: ignore
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        parser = JsonOutputParser(pydantic_object=BotResponse)

        prompt = PromptTemplate(
            template=langchain_template,
            input_variables=["dom_content", "user_prompt"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | model | parser

        response = chain.invoke(
            {"dom_content": file_content, "user_prompt": user_prompt}
        )

        for category in categories:
            if response["category"] in category:
                response["category"] = category
                break

        return response
