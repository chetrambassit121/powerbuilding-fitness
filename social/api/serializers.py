from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from members.api.serializers import UserDetailSerializer  
from members.models import User  
from social.models import Comment, Post


def create_comment_serializer(id, model_type="post", parent_id=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                "id",
                "comment",
                "parent",
                "tags",
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.id = id
            self.parent_obj = None
            if self.parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=self.id)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a id for this content type")
            return data
    return CommentCreateSerializer


class CommentSerializer(ModelSerializer):
    author = UserDetailSerializer()
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "comment",
            "created_on",
            "author",
            "likes",
            "dislikes",
            "parent",
            "tags",
            "reply_count",
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0



class CommentChildSerializer(ModelSerializer):
    author = (
        UserDetailSerializer()
    )  

    class Meta:
        model = Comment
        fields = [
            "id",
            "comment",
            "created_on",
            "author",
            "parent",
        ]


class CommentDetailSerializer(ModelSerializer):
    author = (
        UserDetailSerializer()
    )  
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "comment",
            "created_on",
            "author",
            "likes",
            "dislikes",
            "tags",
            "replies",
            "reply_count",
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "body",
            # 'slug',
            "image",
            "video",
        ]


post_detail_url = HyperlinkedIdentityField(view_name="detail", lookup_field="id")


class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    author = UserDetailSerializer(
        read_only=True
    )  
    html = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            "url",
            "id",
            # "slug",
            "author",
            "shared_user",
            "body",
            "shared_body",
            "image",
            "video",
            "created_on",
            "shared_on",
            "likes",
            "dislikes",
            "tags",
            "html"
        ]


    def get_html(self, obj):
        return obj.get_markdown()


class PostDetailCommentsSerializer(ModelSerializer):
    url = post_detail_url
    author = UserDetailSerializer(
        read_only=True
    ) 

    html = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "url",
            "pk",
            "author",
            "shared_user",
            "body",
            "shared_body",
            "image",
            "video",
            "created_on",
            "shared_on",
            "likes",
            "dislikes",
            "tags",
            "html",
            "comments",
        ]


    def get_html(self, obj):
        return obj.get_markdown()

    def get_comments(self, pk):
        post = Post.objects.get(pk=pk)
        c_qs = Comment.objects.filter(post=post)
        comments = CommentSerializer(c_qs, many=True).data
        return comments


class PostListSerializer(ModelSerializer):
    author = (
        UserDetailSerializer()
    )  
    html = SerializerMethodField()
    url = post_detail_url
    delete_url = HyperlinkedIdentityField(
        view_name="delete",
        lookup_field="id",
        
    )
    class Meta:
        model = Post
        fields = [
            "url",
            "id",
            "author",
            # "slug",
            "shared_user",
            "body",
            "shared_body",
            "image",
            "video",
            "html",
            "created_on",
            "shared_on",
            "likes",
            "dislikes",
            "tags",
            "delete_url",
        ]

    def get_html(self, obj):
        return obj.get_markdown()

