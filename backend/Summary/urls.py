from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns: list[URLPattern] = [
    path("website/", views.WebsiteView.as_view(), name="website"),
    path("text/", views.TextView.as_view(), name="text"),
    path("file/", views.FileView.as_view(), name="file_upload"),
    path("", views.SummaryList.as_view(), name="summary_list"),
    path("id/<int:id>/", views.SummaryDetail.as_view(), name="summary_detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]
