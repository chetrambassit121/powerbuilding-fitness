# LOGIC .... USER API SETUP

from django.contrib.auth import get_user_model
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
from rest_framework.response import Response  
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST  
from rest_framework.views import APIView  

from members.models import User, UserProfile

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    ModelSerializer,
    UserCreateSerializer,
    UserCreateUpdateSerializer,
    UserDetailSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)

# from .pagination import PostLimitOffsetPagination, PostPageNumberPagination


class UserCreateAPIView(
    CreateAPIView
):  
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserLoginAPIView(APIView):  
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):  
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [AllowAny]


class UserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perform_update(self, serializer):
        serializer.save(username=self.request.user)


class UserProfileAPIView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]


class UserProfileUpdateAPIView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "username"

    def perform_update(self, serializer):
        serializer.save(username=self.request.user)
