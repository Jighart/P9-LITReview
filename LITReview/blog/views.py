from django.shortcuts import render, get_object_or_404
from .models import Review

# Create your views here.
def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'blog/review/list.html', {'reviews': reviews})


def review_detail(request, id):
    review = get_object_or_404(Review, id=id)
    return render(request, 'blog/review/detail.html', {'review': review})