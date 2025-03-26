from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns: list[URLPattern] = [
    path("website/", views.WebsiteView.as_view(), name="website"),
    path("text/", views.TextView.as_view(), name="text"),
    path("file/", views.FileView.as_view(), name="file_upload"),
    path("video/", views.VideoView.as_view(), name="video"),
    path("", views.SummaryList.as_view(), name="summary_list"),
    path("id/<int:id>/", views.SummaryDetail.as_view(), name="summary_detail"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("like/<int:id>/", views.LikeView.as_view(), name="like"),
    path("dislike/<int:id>/", views.DislikeView.as_view(), name="dislike"),
    path("favorite/<int:id>/", views.FavoriteView.as_view(), name="favorite"),
]
