from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage,  PageNotAnInteger
from django.views import generic

from blog.forms import TicketForm, ReviewForm
from .models import Ticket, Review

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


def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    return render(request, 'blog/review/detail.html', {'ticket': ticket})


def review_create(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES or None)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.save()
            return redirect('review_list')
    
    else:
        form = ReviewForm()
    return render(request, 'blog/review/create_review.html', {'form': form})


def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_ticket = Ticket.objects.create(
                user = request.user,
                title = form.cleaned_data['title'],
                body = form.cleaned_data['body']
            )
            new_ticket.save()
            messages.success(request, 'Created')

            # new_ticket = form.save(commit=False)
            # new_ticket.user = request.user
            # new_ticket.save()
            return redirect('review_list')
    
    else:
        form = TicketForm()
    return render(request, 'blog/review/create_ticket.html', {'form': form})


def ticket_respond(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if request.method == 'POST':
        form = ReviewForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.ticket = ticket
            new_review.save()
            return redirect('review_list')
    
    else:
        form = ReviewForm()
    return render(request, 'blog/review/create_review.html', {'form': form})