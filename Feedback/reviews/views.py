from typing import Any
from django.shortcuts import render
from django.http import HttpResponseRedirect
from reviews.forms import ReviewForm
from reviews.models import Review
from django.views import View
from django.views.generic.base import TemplateView
from .models import Review

# Create your views here.

class ReviewView(View):
    def get (self, request):
        form = ReviewForm()
    
        return render (request, "reviews/review.html",{
            "form" : form
        })
    
       
    def post(self, request):
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            """ print(form.cleaned_data) """
            review = Review(user_name=form.cleaned_data['user_name'],
                            review_text=form.cleaned_data['review_text'],
                            rating=form.cleaned_data['rating'])
            review.save()
            return HttpResponseRedirect("/thank_you")
        
        return render (request, "reviews/review.html",{
            "form" : form
        })
        

class ThankYouView(TemplateView):
    template_name = "reviews/thank_you.html"
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context [" message "] = "This works!"
        return context


class ReviewListView(TemplateView):
    template_name = "reviews/review_list.html"
    
    def get_context_data(self, **kwargs):
        context=  super().get_context_data(**kwargs)
        reviews = Review.objects.all()
        context["reviews"] = reviews
        return context

class ReviewDetailView(TemplateView):
    template_name = "reviews/review_detail.html"
    
    def get_context_data(self, **kwargs):
        context=  super().get_context_data(**kwargs)
        review_id = kwargs["id"]
        selected_review = Review.objects.get(pk=review_id)
        context["review"] = selected_review
        return context