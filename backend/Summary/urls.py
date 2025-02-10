from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns: list[URLPattern] = [
    path("website/", views.Website.as_view(), name="website"),
    path("", views.SummaryList.as_view(), name="summary_list"),
    path("<int:id>/", views.SummaryDetail.as_view(), name="summary_detail"),
]
