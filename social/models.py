from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse, reverse_lazy
from django.utils import timezone

# markdown
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdown_deux import markdown

from members.models import User, UserProfile

from .validators import file_size


class PostTest(models.Model):
    bodytest = models.TextField(max_length=1000)
    slug = models.SlugField(max_length=250, default=None)
    likestest = models.ManyToManyField(
        User, related_name="likestest", default=None, blank=True
    )
    dislikestest = models.ManyToManyField(
        User, related_name="dislikestest", default=None, blank=True
    )

    def get_absolute_url(self):
        return reverse("post_single", args=[self.slug])

    def __str__(self):
        return self.bodytest


class Notification(models.Model):
    ''' 1 = Like, 2 = Comment, 3 = Follow, #4 = DM '''
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(
        User, related_name="notification_to", on_delete=models.CASCADE, null=True
    )
    from_user = models.ForeignKey(
        User, related_name="notification_from", on_delete=models.CASCADE, null=True
    )
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="+", blank=True, null=True
    )
    comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="+", blank=True, null=True
    )
    thread = models.ForeignKey(
        "ThreadModel", on_delete=models.CASCADE, related_name="+", blank=True, null=True
    )
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)


class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")


class MessageModel(models.Model):
    thread = models.ForeignKey(
        "ThreadModel", related_name="+", on_delete=models.CASCADE, blank=True, null=True
    )
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    body = models.CharField(max_length=1000)
    image = models.ImageField(
        upload_to="media/uploads/message_photos", blank=True, null=True
    )
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_on"]


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Post(models.Model):
    body = models.TextField()
    image = models.ImageField(
        upload_to="media/uploads/post_photos", blank=True, null=True
    )
    video = models.FileField(
        upload_to="media/uploads/post_videos",
        validators=[file_size],
        blank=True,
        null=True,
    )
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="+"
    )
    shared_body = models.TextField(blank=True, null=True)
    shared_on = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likess")
    dislikes = models.ManyToManyField(User, blank=True, related_name="dislikess")
    tags = models.ManyToManyField("Tag", blank=True)

    def create_tags(self):
        for word in self.body.split():
            if word[0] == "#":
                tag = Tag.objects.filter(name=word[1:]).first()
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                self.save()

        if self.shared_body:
            for word in self.shared_body.split():
                if word[0] == "#":
                    tag = Tag.objects.filter(name=word[1:]).first()
                    if tag:
                        self.tags.add(tag.pk)
                    else:
                        tag = Tag(name=word[1:])
                        tag.save()
                        self.tags.add(tag.pk)
                    self.save()

    class Meta:
        ordering = ["-created_on"]

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    def get_markdown(self):
        body = self.body
        markdown_text = markdown(body)
        return mark_safe(markdown_text)


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, default=False)
    likes = models.ManyToManyField(User, blank=True, related_name="comment_likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="comment_dislikes")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="+"
    )
    tags = models.ManyToManyField("Tag", blank=True)


    def create_tags(self):
        for word in self.comment.split():
            if word[0] == "#":
                tag = Tag.objects.get(name=word[1:])
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                self.save()

    # def get_absolute_url(self):
    #     return reverse("post-detail", kwargs={"id": self.id})

    def children(self):
        return Comment.objects.filter(parent=self).order_by("-created_on").all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    class Meta:
        ordering = ["-created_on"]
