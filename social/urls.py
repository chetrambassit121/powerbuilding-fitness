from django.urls import path

from .views import (
    AddCommentDislike,
    AddCommentLike,
    AddDislike,
    AddFollower,
    AddLike,
    CommentDeleteView,
    CommentReplyView,
    CommentReplyViewPage,
    CreateMessage,
    CreateThread,
    Explore,
    FollowNotification,
    ListFollowers,
    ListFollowings,
    ListThreads,
    NotificationView,
    PostDeleteView,
    PostDetailAddDislike,
    PostDetailAddLike,
    PostDetailView,
    PostEditView,
    PostListView,
    PostNotification,
    ProfileAddDislike,
    ProfileAddLike,
    RemoveFollower,
    RemoveNotification,
    ReplyDeleteView,
    ReplyPageDeleteView,
    SharedPostView,
    SharedProfileAddDislike,
    SharedProfileAddLike,
    ThreadNotification,
    ThreadView,
    UserSearch,
    post_single,
    post_single_test,
)

urlpatterns = [
    # notifications
    path("notifications/", NotificationView.as_view(), name="notifications"),
    path(
        "notification/<int:notification_pk>/post/<int:post_pk>",
        PostNotification.as_view(),
        name="post-notification",
    ),
    path(
        "notification/<int:notification_pk>/profile/<int:profile_pk>",
        FollowNotification.as_view(),
        name="follow-notification",
    ),
    path(
        "notification/<int:notification_pk>/thread/<int:object_pk>",
        ThreadNotification.as_view(),
        name="thread-notification",
    ),
    path(
        "notification/delete/<int:notification_pk>",
        RemoveNotification.as_view(),
        name="notification-delete",
    ),

    # search bar
    path("search/", UserSearch.as_view(), name="profile-search"),

    # explore #hashtag icon in navbar
    path("explore/", Explore.as_view(), name="explore"),

    # inbox icon in navbar
    path("inbox/", ListThreads.as_view(), name="inbox"),
    path("inbox/create-thread/", CreateThread.as_view(), name="create-thread"),
    path("inbox/<int:pk>/", ThreadView.as_view(), name="thread"),
    path(
        "inbox/<int:pk>/create-message/", CreateMessage.as_view(), name="create-message"
    ),

    # public posts (main social feed)
    path("post-list/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/share", SharedPostView.as_view(), name="share-post"),
    path("post/<int:id>/like", AddLike.as_view(), name="like"),
    path("post/<int:id>/dislike", AddDislike.as_view(), name="dislike"),

    # post detail page which includes the post, editing post, deleting post, its comments, reply form and view replies link
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/edit/<int:pk>/", PostEditView.as_view(), name="post-edit"),
    path("post/delete/<int:pk>/", PostDeleteView.as_view(), name="post-delete"),
    path(
        "post/<int:pk>/post-detail-like",
        PostDetailAddLike.as_view(),
        name="post-detail-like",
    ),
    path(
        "post/<int:pk>/post-detail-dislike",
        PostDetailAddDislike.as_view(),
        name="post-detail-dislike",
    ),
    path(
        "post/<int:post_pk>/comment/delete/<int:pk>/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    path(
        "post/<int:post_pk>/comment/<int:pk>/like",
        AddCommentLike.as_view(),
        name="comment-like",
    ),
    path(
        "post/<int:post_pk>/comment/<int:pk>/dislike",
        AddCommentDislike.as_view(),
        name="comment-dislike",
    ),

    # replies
    path(
        "post/<int:post_pk>/comment/<int:pk>/reply",
        CommentReplyView.as_view(),
        name="comment-reply",
    ),
    path(
        "comment/<int:pk>/reply",
        CommentReplyViewPage.as_view(),
        name="view-comment-reply",
    ),
    path(
        "comment/<int:comment_pk>/reply/delete/<int:pk>/",
        ReplyDeleteView.as_view(),
        name="reply-delete",
    ),

    # user profile like / dislike for post
    path(
        "profile/<int:pk>/post/<int:id>/profile-like",
        ProfileAddLike.as_view(),
        name="profile-like",
    ),
    path(
        "profile/<int:pk>/post/<int:id>/profile-dislike",
        ProfileAddDislike.as_view(),
        name="profile-dislike",
    ),

    # sharedprofile like / dislike for sharedpost
    path(
        "profile/<int:pk>/post/<int:id>/shared-profile-like",
        SharedProfileAddLike.as_view(),
        name="shared-profile-like",
    ),
    path(
        "profile/<int:pk>/post/<int:id>/shared-profile-dislike",
        SharedProfileAddDislike.as_view(),
        name="shared-profile-dislike",
    ),

    # followers in user profile
    path("profile/<int:pk>/followers/", ListFollowers.as_view(), name="list-followers"),

    # # path('profile/<int:pk>/followers-list/remove', RemoveFollowerFromList.as_view(), name='remove-list-followers'),
    path("profile/<int:pk>/followers/add", AddFollower.as_view(), name="add-follower"),
    path(
        "profile/<int:pk>/followers/remove",
        RemoveFollower.as_view(),
        name="remove-follower",
    ),
    
    # path('profile/<int:pk>/followers/delete', DeleteFollower.as_view(), name='delete-follower'),
    path(
        "profile/<int:pk>/followings/", ListFollowings.as_view(), name="list-followings"
    ),
]
