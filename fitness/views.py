from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import (
    redirect,
    
)  
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.urls import reverse


class HomeView(View):
    def get(
        self, request
    ):  
        return render(
            request, "home.html"
        )  

class AboutView(View):
    def get(
        self, request
    ):  
        return render(
            request, "about.html"
        )  

class ClassesView(View):
    def get(
        self, request
    ):  
        return render(
            request, "classes.html"
        )  

class TrainerView(View):
    def get(
        self, request
    ):  
        return render(
            request, "trainer.html"
        )  

class ScheduleView(View):
    def get(
        self, request
    ):  
        return render(
            request, "schedule.html"
        )  

class ContactView(View):
    def get(
        self, request
    ):  
        return render(
            request, "contact.html"
        )  

# class HomeTwoView(View):
#     def get(
#         self, request
#     ):  
        
#         return render(
#             request, "index.html"
#         )  


# def SurveyView(request):
#     survey = Survey.objects.all()
#     return render(request, "surveys.html", {"survey": survey})


# class AboutView(View):
#     def get(self, request):
#         return render(request, "about.html")


# def Powerlifting(request):
#     return render(request, "powerlifting.html")


# def Bodybuilding(request):
#     return render(request, "bodybuilding.html")


# def Powerbuilding(request):
#     return render(request, "powerbuilding.html")


# # @login_required
# def like(request, id):
#     user = request.user
#     Likes = False
#     Dislikes = False
#     if request.method == "POST":
#         survey_id = request.POST["survey_id"]
#         get_video = get_object_or_404(Survey, id=survey_id)

#         if user in get_video.likes.all():
#             get_video.likes.remove(user)
#             Likes = False
#         elif user in get_video.dislikes.all():
#             get_video.dislikes.remove(user)
#             Dislikes = False
#             get_video.likes.add(user)
#             Likes = True

#         else:
#             get_video.likes.add(user)
#             Likes = True

#         data = {
#             "liked": Likes,
#             "likes_count": get_video.likes.all().count(),
#             "disliked": Dislikes,
#             "dislikes_count": get_video.dislikes.all().count(),
#         }

#         return JsonResponse(data, safe=False)
#     return redirect(reverse("surveys", args=[str(id)]))


# # @login_required
# def dislike(request, id):
#     user = request.user
#     Dislikes = False
#     Likes = False
#     if request.method == "POST":
#         survey_id = request.POST["survey_id"]
#         watch = get_object_or_404(Survey, id=survey_id)

#         if user in watch.dislikes.all():
#             watch.dislikes.remove(user)
#             Dislikes = False

#         elif user in watch.likes.all():
#             watch.likes.remove(user)
#             Likes = False
#             watch.dislikes.add(user)
#             Dislikes = True

#         else:
#             watch.dislikes.add(user)
#             Dislikes = True

#         data = {
#             "liked": Likes,
#             "likes_count": watch.likes.all().count(),
#             "disliked": Dislikes,
#             "dislikes_count": watch.dislikes.all().count(),
#         }

#         return JsonResponse(data, safe=False)
#     return redirect(reverse("surveys", args=[str(id)]))
