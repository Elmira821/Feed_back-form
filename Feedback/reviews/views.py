from typing import Any
from django.shortcuts import render
from django.http import HttpResponseRedirect
from reviews.forms import ReviewForm
from reviews.models import Review
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Review

# Create your views here.


class ReviewView(FormView):
    form_class = ReviewForm
    template_name = "reviews/review.html"

    # def get (self, request):
    #     form = ReviewForm()

    #     return render (request, "reviews/review.html",{
    #         "form" : form
    #     })

    def post(self, request):
        form = ReviewForm(request.POST)

        if form.is_valid():
            """ print(form.cleaned_data) """
            review = Review(user_name=form.cleaned_data['user_name'],
                            review_text=form.cleaned_data['review_text'],
                            rating=form.cleaned_data['rating'])
            review.save()
            return HttpResponseRedirect("/thank_you")

        return render(request, "reviews/review.html", {
            "form": form
        })


class ThankYouView(TemplateView):
    template_name = "reviews/thank_you.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[" message "] = "This works!"
        return context


class ReviewListView(ListView):
    template_name = "reviews/review_list.html"
    model = Review
    context_object_name = "reviews"

    #  def get_context_data(self, **kwargs):
    #     context=  super().get_context_data(**kwargs)
    #     reviews = Review.objects.all()
    #     context["reviews"] = reviews
    #     return context """                            This is when we used Template View
    #  we can add extra methods here, example:

    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query.filter(rating__gt=2)
        return data


class ReviewDetailView(DetailView):
    template_name = "reviews/review_detail.html"
    model = Review
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object 
        request = self.request
        favorite_id = request.session.get("favorite_review")
        context["is_favorite"] = favorite_id == str(loaded_review.id)
        return context

    # def get_context_data(self, **kwargs):
    #     context=  super().get_context_data(**kwargs)
    #     review_id = kwargs["id"]
    #     selected_review = Review.objects.get(pk=review_id)
    #     context["review"] = selected_review
    #     return context                                            This is when we used Template View


class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST["review_id"]
        request.session["favorite_review"] = review_id     #store string, boolean... simple data, do not store object in session
        return HttpResponseRedirect ("/reviews/" + review_id)