from django.urls import path

from reviews import views


urlpatterns = [
    path("",views.ReviewView.as_view()),
    path("thank_you", views.thank_you),
]
