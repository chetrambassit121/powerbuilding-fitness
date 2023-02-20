# LOGIC .... comments api

from django.db.models import Q
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from social.api.permissions import IsOwnerOrReadOnly
from social.api.serializers import (  
    CommentSerializer,
    CommentDetailSerializer,
    PostCreateUpdateSerializer,
    PostDetailCommentsSerializer,
    PostDetailSerializer,
    PostListSerializer,
)
from social.models import Comment, Post  

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination


class CommentDetailAPIView(RetrieveAPIView):  
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"


class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"


class CommentListAPIView(ListAPIView):  
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["content", "first_name", "last_name", "author"]
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(comment__icontains=query)
                |
                Q(author__first_name__icontains=query)
                | Q(author__last_name__icontains=query)
            ).distinct()
        return queryset_list


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


class PostDetailCommentsAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailCommentsSerializer
    lookup_field = "pk"


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["body", "first_name", "last_name", "author"]
    permission_classes = [AllowAny]
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(body__icontains=query)
                |
                Q(author__first_name__icontains=query)
                | Q(author__last_name__icontains=query)
            ).distinct()
        return queryset_list


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
