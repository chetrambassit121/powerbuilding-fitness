# from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import (
    CommentDeleteAPIView,
    CommentDetailAPIView,
    CommentListAPIView,
    PostCreateAPIView,
    PostDeleteAPIView,
    PostDetailAPIView,
    PostDetailCommentsAPIView,
    PostListAPIView,
    PostUpdateAPIView,
)

urlpatterns = [
    # comments api urls
    path(
        "comments/", CommentListAPIView.as_view(), name="comments"
    ),  
    # url to display comment fields/data including the replies
    path(
        "comments/<int:id>/", CommentDetailAPIView.as_view(), name="comment-detail"
    ),  
    path(
        "comments/delete/<int:id>/",
        CommentDeleteAPIView.as_view(),
        name="comment-delete",
    ),

    # posts api urls
    # url to display posts fields/data
    path(
        "", PostListAPIView.as_view(), name="list"
    ),  
     # url to create post
    path("create/", PostCreateAPIView.as_view(), name="create"), 
    # url to display post detail fields/data
    path(
        "post/<int:id>/", PostDetailAPIView.as_view(), name="detail"
    ),  
    # url to display post detail fields/data
    path(
        "post/comments/<int:pk>/",
        PostDetailCommentsAPIView.as_view(),
        name="post-comments",
    ),  
     # url to edit a post
    path(
        "post/edit/<int:id>/", PostUpdateAPIView.as_view(), name="update"
    ), 
    path(
        "post/delete/<int:id>/", PostDeleteAPIView.as_view(), name="delete"
    ),  
]
