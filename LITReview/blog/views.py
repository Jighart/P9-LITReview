from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,  PageNotAnInteger
from django.views import generic
from .models import Review

# def review_list(request):
#     object_list = Review.objects.all()
#     paginator = Paginator(object_list, 2)
#     page = request.GET.get('page')
#     try:
#         reviews = paginator.page(page)
#     except PageNotAnInteger:
#         reviews = paginator.page(1)
#     except EmptyPage:
#         reviews = paginator.page(paginator.num_pages)
#     context = {
#         'reviews': reviews,
#         'page': page,
#     }
        
#     return render(request, 'blog/review/list.html', context)

class ReviewListView(generic.ListView):
    queryset = Review.objects.all().order_by(('time_created')).reverse()
    paginate_by = 2
    template_name = 'blog/review/list.html'
    context_object_name = 'reviews'


def review_detail(request, id):
    review = get_object_or_404(Review, id=id)
    return render(request, 'blog/review/detail.html', {'review': review})