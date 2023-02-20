from django import template
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View, generic
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView

from members.models import User, UserProfile

from .forms import (
    CommentForm,
    EditPostForm,
    ExploreForm,
    MessageForm,
    PostForm,
    ShareForm,
    ThreadForm,
)
from .models import (
    Comment,
    MessageModel,
    Notification,
    Post,
    PostTest,
    Tag,
    ThreadModel,
)


def post_single_test(request):
    all_posts = PostTest.objects.all()
    return render(request, "social/detail_test.html", {"posts": all_posts})


def post_single(request, post):
    post = get_object_or_404(PostTest, slug=post)
    return render(request, "social/detail.html", {"post": post})


class NotificationView(View):
    def get(self, request, *args, **kwargs):
        request_user = request.user
        p = Paginator(
            Notification.objects.filter(to_user=request_user)
            .exclude(user_has_seen=True)
            .order_by("-date"),
            10,
        )
        page = request.GET.get("page")
        notifications = p.get_page(page)
        notificationss = Notification.notification_type
        context = {"notifications": notifications}

        if notificationss == 1:

            def get(
                self, request, notification_pk, post_pk, object_pk, *args, **kwargs
            ):
                notification = Notification.objects.get(pk=notification_pk)
                post = Post.objects.get(pk=post_pk)

                notification.user_has_seen = True
                notification.save()

                return redirect("post-detail", pk=post_pk)

        if notificationss == 2:

            def get(self, request, notification_pk, profile_pk, *args, **kwargs):
                notification = Notification.objects.get(pk=notification_pk)
                profile = UserProfile.objects.get(pk=profile_pk)

                notification.user_has_seen = True
                notification.save()

                return redirect("show_profile_page", pk=profile_pk)

        if notificationss == 3:

            def get(self, request, notification_pk, object_pk, *args, **kwargs):
                notification = Notification.objects.get(pk=notification_pk)
                thread = ThreadModel.objects.get(pk=object_pk)

                notification.user_has_seen = True
                notification.save()

                return redirect("thread", pk=object_pk)

        if notificationss == 4:

            def delete(self, request, notification_pk, *args, **kwargs):
                notification = Notification.objects.get(pk=notification_pk)

                notification.user_has_seen = True
                notification.save()

                return HttpResponse("Success", content_type="text/plain")

        return render(request, "social/all_notifications.html", context)


class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect("post-detail", pk=post_pk)


class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = UserProfile.objects.get(pk=profile_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect("show_profile_page", pk=profile_pk)


class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect("thread", pk=object_pk)


class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        notification.save()
        return HttpResponse("Success", content_type="text/plain")


class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("query")
        profile_list = UserProfile.objects.filter(Q(user__username__icontains=query))
        context = {
            "profile_list": profile_list,
        }
        return render(request, "social/search.html", context)


# explore #hastags
class Explore(View):
    def get(self, request, *args, **kwargs):
        explore_form = ExploreForm()
        query = self.request.GET.get("query")
        tag = Tag.objects.filter(name=query).first()

        if tag:
            p = Paginator(Post.objects.filter(tags__in=[tag]), 5)
            page = request.GET.get("page")
            posts = p.get_page(page)

        else:
            p = Paginator(Post.objects.all(), 5)
            page = request.GET.get("page")
            posts = p.get_page(page)

        context = {
            "tag": tag,
            "posts": posts,
            "explore_form": explore_form,
        }
        return render(request, "social/explore.html", context)

    def post(self, request, *args, **kwargs):
        explore_form = ExploreForm(request.POST)
        if explore_form.is_valid():
            query = explore_form.cleaned_data["query"]
            tag = Tag.objects.filter(name=query).first()

            posts = None
            if tag:
                posts = Post.objects.filter(tags__in=[tag])

            if posts:
                context = {
                    "tag": tag,
                    "posts": posts,
                }
            else:
                context = {
                    "tag": tag,
                }

            return HttpResponseRedirect(f"/social/explore?query={query}")
        return HttpResponseRedirect("/social/explore")


# inbox
class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(
            Q(user=request.user) | Q(receiver=request.user)
        )

        context = {
            "threads": threads,
        }

        return render(request, "social/inbox.html", context)


class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {"form": form}

        return render(request, "social/create_thread.html", context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get("username")

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(
                user=request.user, receiver=receiver
            ).exists():
                thread = ThreadModel.objects.filter(
                    user=request.user, receiver=receiver
                )[0]
                return redirect("thread", pk=thread.pk)
            elif ThreadModel.objects.filter(
                user=receiver, receiver=request.user
            ).exists():
                thread = ThreadModel.objects.filter(
                    user=receiver, receiver=request.user
                )[0]
                return redirect("thread", pk=thread.pk)
            if form.is_valid():
                thread = ThreadModel(user=request.user, receiver=receiver)
                thread.save()
                return redirect("thread", pk=thread.pk)
        except:
            messages.error(request, "Invalid username")
            return redirect("create-thread")


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        p = Paginator(MessageModel.objects.filter(thread__pk__contains=pk), 10)
        page = request.GET.get("page")
        message_list = p.get_page(page)
        context = {"thread": thread, "form": form, "message_list": message_list}
        return render(request, "social/thread.html", context)


class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()

        notification = Notification.objects.create(
            notification_type=4, from_user=request.user, to_user=receiver, thread=thread
        )
        context = {"thread": thread, "form": form, "message_list": message_list}
        if request.accepts("application/json"):
            html = render_to_string(
                "social/thread_messages.html", context, request=request
            )
            return JsonResponse({"form": html})
        return render(request, "social/thread.html", context)


# post list (main social feed)
class PostListView(View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        share_form = ShareForm()
        post = Post.objects.all()
        post_count = post.count()
        comment = Comment.objects.filter(post=post)
        p = Paginator(Post.objects.all(), 10)
        page = request.GET.get("page")
        posts = p.get_page(page)
        context = {
            "posts": posts,
            "shareform": share_form,
            "form": form,
            "post_count": post_count,
        }

        return render(request, "social/post_list.html", context)

    def post(self, request, *args, **kwargs):
        post = Post.objects.all()
        post_count = post.count()
        form = PostForm(request.POST, request.FILES)
        share_form = ShareForm()
        p = Paginator(Post.objects.all(), 10)
        page = request.GET.get("page")
        posts = p.get_page(page)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            form = PostForm()

        new_post.create_tags()

        context = {
            "posts": posts,
            # 'all_video': all_video,
            "shareform": share_form,
            "form": form,
            "post_count": post_count,
        }

        return render(request, "social/post_list.html", context)


# share post
class SharedPostView(View):
    def post(self, request, pk, *args, **kwargs):
        original_post = Post.objects.get(pk=pk)
        form = ShareForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = Post(
                shared_body=self.request.POST.get("body"),
                image=original_post.image,
                video=original_post.video,
                body=original_post.body,
                author=original_post.author,
                shared_on=original_post.created_on,
                shared_user=request.user,
                created_on=timezone.now(),
            )
            new_post.save()
            new_post.create_tags()

        return redirect("post-list")


# post like
class AddLike(LoginRequiredMixin, View):
    def post(self, request, id, *args, **kwargs):
        post = Post.objects.get(id=id)
        user = request.user
        
        Likes = False
        Dislikes = False
        if request.method == "POST":
            post_id = request.POST["post_id"]
            get_post = get_object_or_404(Post, id=post_id)

            if user in get_post.likes.all():
                get_post.likes.remove(user)
                Likes = False
            elif user in get_post.dislikes.all():
                get_post.dislikes.remove(user)
                Dislikes = False
                get_post.likes.add(user)
                Likes = True
            else:
                get_post.likes.add(user)
                Likes = True
                notification = Notification.objects.create(
                    notification_type=1, from_user=user, to_user=post.author, post=post
                )

            data = {
                "post_id": post_id,
                "liked": Likes,
                "likes_count": get_post.likes.all().count(),
                "disliked": Dislikes,
                "dislikes_count": get_post.dislikes.all().count(),
            }
            return JsonResponse(data, safe=False)
        return redirect(reverse("post-list"), args=[str(id)])


# post dislike
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, id, *args, **kwargs):
        post = Post.objects.get(id=id)
        user = request.user
        Dislikes = False
        Likes = False
        if request.method == "POST":
            post_id = request.POST["post_id"]
            post = get_object_or_404(Post, id=post_id)

            if user in post.dislikes.all():
                post.dislikes.remove(user)
                Dislikes = False

            elif user in post.likes.all():
                post.likes.remove(user)
                Likes = False
                post.dislikes.add(user)
                Dislikes = True
            else:
                post.dislikes.add(user)
                Dislikes = True

            data = {
                "liked": Likes,
                "likes_count": post.likes.all().count(),
                "disliked": Dislikes,
                "dislikes_count": post.dislikes.all().count(),
            }

            return JsonResponse(data, safe=False)
        return redirect(reverse("post-list"), args=[str(id)])


#  post detail
class PostDetailView(LoginRequiredMixin, ListView):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comment = Comment.objects.filter(post=post)
        comment_count = comment.count()
        p = Paginator(Comment.objects.filter(post=post), 10)
        page = request.GET.get("page")
        comments = p.get_page(page)

        context = {
            "post": post,
            "form": form,
            "comment_count": comment_count,
            "comments": comments,
        }

        return render(request, "social/post_detail.html", context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            new_comment.create_tags()
            form = CommentForm()

        p = Paginator(Comment.objects.filter(post=post), 10)
        page = request.GET.get("page")
        comments = p.get_page(page)

        notification = Notification.objects.create(
            notification_type=2, from_user=request.user, to_user=post.author, post=post
        )
        context = {
            "post": post,
            "form": form,
            "comments": comments,
        }

        return render(request, "social/post_detail.html", context)


# post edit
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["body", "image"]
    template_name = "social/post_edit.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("post-detail", kwargs={"pk": pk})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return self.request.user == post.author
        elif self.request.user == post.shared_user:
            return self.request.user == post.shared_user


# post delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "social/post_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return self.request.user == post.author
        elif self.request.user == post.shared_user:
            return self.request.user == post.shared_user

# the comment like on post detail page
class PostDetailAddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)
            notification = Notification.objects.create(
                notification_type=1,
                from_user=request.user,
                to_user=post.author,
                post=post,
            )

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get("next", "/")
        return HttpResponseRedirect(next)


# the comment dislike on post detail page
class PostDetailAddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True

                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get("next", "/")

        return HttpResponseRedirect(next)


# getting comments, posting comments
class CommentReplyView(LoginRequiredMixin, ListView):
    def get(self, request, pk, post_pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)

        form = CommentForm()
        comment = Comment.objects.get(pk=pk)
        context = {
            "form": form,
            "post": post,
            "comment": comment,
        }
        return render(request, "social/post_comment_replies.html", context)

    def post(self, request, pk, post_pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        notification = Notification.objects.create(
            notification_type=2,
            from_user=request.user,
            to_user=parent_comment.author,
            comment=new_comment,
        )
        return redirect("post-detail", pk=post_pk)


# comment delete
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "social/comment_delete.html"

    def get_success_url(self):
        pk = self.kwargs["post_pk"]
        return reverse_lazy("post-detail", kwargs={"pk": pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# comment like
class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        user = request.user
        Likes = False
        Dislikes = False
        if request.method == "POST":
            comment_pk = request.POST["comment_pk"]
            get_comment = get_object_or_404(Comment, pk=comment_pk)

            if user in get_comment.likes.all():
                get_comment.likes.remove(user)
                Likes = False
            elif user in get_comment.dislikes.all():
                get_comment.dislikes.remove(user)
                Dislikes = False
                get_comment.likes.add(user)
                Likes = True
            else:
                get_comment.likes.add(user)
                Likes = True
                notification = Notification.objects.create(
                    notification_type=1,
                    from_user=user,
                    to_user=comment.author,
                    comment=comment,
                )

            data = {
                "comment_pk": comment_pk,
                "liked": Likes,
                "likes_count": get_comment.likes.all().count(),
                "disliked": Dislikes,
                "dislikes_count": get_comment.dislikes.all().count(),
            }

            return JsonResponse(data, safe=False)
        return redirect(reverse("post-detail"))


# comment dislike
class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        user = request.user
        Dislikes = False
        Likes = False
        if request.method == "POST":
            comment_pk = request.POST["comment_pk"]
            get_comment = get_object_or_404(Comment, pk=comment_pk)
            if user in get_comment.dislikes.all():
                get_comment.dislikes.remove(user)
                Dislikes = False
            elif user in get_comment.likes.all():
                get_comment.likes.remove(user)
                Likes = False
                get_comment.dislikes.add(user)
                Dislikes = True
            else:
                get_comment.dislikes.add(user)
                Dislikes = True

            data = {
                "liked": Likes,
                "likes_count": get_comment.likes.all().count(),
                "disliked": Dislikes,
                "dislikes_count": get_comment.dislikes.all().count(),
            }

            return JsonResponse(data, safe=False)
        return redirect(reverse("post-detail"))


# reply delete on post detail view
class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "social/reply_delete.html"

    def get_success_url(self):
        pk = self.kwargs["comment_pk"]
        return reverse_lazy("view-comment-reply", kwargs={"pk": pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


# viewing all replies on seperate page and posting
class CommentReplyViewPage(LoginRequiredMixin, ListView):
    def get(self, request, pk, *args, **kwargs):
        form = CommentForm()
        comment = Comment.objects.get(pk=pk)
        context = {
            "form": form,
            "comment": comment,
        }
        return render(request, "social/post_comment_replies.html", context)

    def post(self, request, pk, post_pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.parent = parent_comment
            new_comment.save()

        notification = Notification.objects.create(
            notification_type=2,
            from_user=request.user,
            to_user=parent_comment.author,
            comment=new_comment,
        )
        context = {
            "post": post,
            "form": form,
            "parent_comment": parent_comment,
        }
        return redirect("view_comment_reply", pk=post_pk)


# reply delete on replies view page
class ReplyPageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "social/reply_delete.html"

    def get_success_url(self, post_pk):
        pk = self.kwargs["comment_pk"]
        return reverse_lazy("view-comment-reply", kwargs={"pk": post_pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


# followers
class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)

        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            "profile": profile,
            "followers": followers,
            "is_following": is_following,
            "number_of_followers": number_of_followers,
        }

        return render(request, "social/followers_list.html", context)


class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        notification = Notification.objects.create(
            notification_type=3, from_user=request.user, to_user=profile.user
        )
        return redirect("show_profile_page", pk=profile.pk)


class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        return redirect("show_profile_page", pk=profile.pk)


class ListFollowings(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followings = profile.followings.all()
        context = {
            "profile": profile,
            "followings": followings,
        }
        return render(request, "social/followings_list.html", context)


class ProfileAddLike(LoginRequiredMixin, View):
    def post(self, request, id, pk, *args, **kwargs):
        post = Post.objects.get(id=id)
        user = request.user
        profile = UserProfile.objects.get(pk=pk)
        Likes = False
        Dislikes = False
        if request.method == "POST":
            post_id = request.POST["post_id"]
            get_post = get_object_or_404(Post, id=post_id)
            if user in get_post.likes.all():
                get_post.likes.remove(user)
                Likes = False
            elif user in get_post.dislikes.all():
                get_post.dislikes.remove(user)
                Dislikes = False
                get_post.likes.add(user)
                Likes = True
            else:
                get_post.likes.add(user)
                Likes = True
                notification = Notification.objects.create(
                    notification_type=1, from_user=user, to_user=post.author, post=post
                )
            data = {
                "post_id": post_id,
                "liked": Likes,
                "likes_count": get_post.likes.all().count(),
                "disliked": Dislikes,
                "dislikes_count": get_post.dislikes.all().count(),
            }
            return JsonResponse(data, safe=False)
        return redirect(
            reverse("registration/show_profile_page", pk=profile.pk, args=[str(id)])
        )


class ProfileAddDislike(LoginRequiredMixin, View):
    def post(self, request, id, pk, *args, **kwargs):
        post = Post.objects.get(id=id)
        user = request.user
        profile = UserProfile.objects.get(pk=pk)
        Dislikes = False
        Likes = False
        if request.method == "POST":
            post_id = request.POST["post_id"]
            post = get_object_or_404(Post, id=post_id)

            if user in post.dislikes.all():
                post.dislikes.remove(user)
                Dislikes = False

            elif user in post.likes.all():
                post.likes.remove(user)
                Likes = False
                post.dislikes.add(user)
                Dislikes = True

            else:
                post.dislikes.add(user)
                Dislikes = True

            data = {
                "post_id": post_id,
                "liked": Likes,
                "likes_count": post.likes.all().count(),
                "disliked": Dislikes,
                "dislikes_count": post.dislikes.all().count(),
            }

            return JsonResponse(data, safe=False)
        return redirect(
            reverse("registration/show_profile_page", pk=profile.pk, args=[str(id)])
        )


class SharedProfileAddLike(LoginRequiredMixin, View):
    def post(self, request, id, pk, *args, **kwargs):
        post = Post.objects.get(id=id)
        user = request.user
        profile = UserProfile.objects.get(pk=pk)
        Likes = False
        Dislikes = False
        if request.method == "POST":
            post_id = request.POST["post_id"]
            get_post = get_object_or_404(Post, id=post_id)

            if user in get_post.likes.all():
                get_post.likes.remove(user)
                Likes = False
            elif user in get_post.dislikes.all():
                get_post.dislikes.remove(user)
                Dislikes = False
                get_post.likes.add(user)
                Likes = True
            else:
                get_post.likes.add(user)
                Likes = True
                notification = Notification.objects.create(
                    notification_type=1, from_user=user, to_user=post.author, post=post
                )

            data = {
                "post_id": post_id,
                "liked": Likes,
                "likes_count": get_post.likes.all().count(),
                "disliked": Dislikes,
                "dislikes_count": get_post.dislikes.all().count(),
            }

            return JsonResponse(data, safe=False)
        return redirect(
            reverse(
                "registration/show_shared_profile_page", pk=profile.pk, args=[str(id)]
            )
        )


class SharedProfileAddDislike(LoginRequiredMixin, View):
    def post(self, request, id, pk, *args, **kwargs):
        post = Post.objects.get(id=id)
        user = request.user
        profile = UserProfile.objects.get(pk=pk)
        Dislikes = False
        Likes = False
        if request.method == "POST":
            post_id = request.POST["post_id"]
            post = get_object_or_404(Post, id=post_id)

            if user in post.dislikes.all():
                post.dislikes.remove(user)
                Dislikes = False
            elif user in post.likes.all():
                post.likes.remove(user)
                Likes = False
                post.dislikes.add(user)
                Dislikes = True
            else:
                post.dislikes.add(user)
                Dislikes = True

            data = {
                "post_id": post_id,
                "liked": Likes,
                "likes_count": post.likes.all().count(),
                "disliked": Dislikes,
                "dislikes_count": post.dislikes.all().count(),
            }

            return JsonResponse(data, safe=False)
        return redirect(
            reverse(
                "registration/show_shared_profile_page", pk=profile.pk, args=[str(id)]
            )
        )
