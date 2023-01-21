from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.views import generic

from .forms import TicketForm, ReviewForm
from .models import Ticket, Review


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
            new_ticket = Ticket.objects.create(
                user = request.user,
                title = ticket_form.cleaned_data['title'],
                body = ticket_form.cleaned_data['body']
            )
            new_ticket.save()

            new_review = Review.objects.create(
                ticket = new_ticket,
                user = request.user,
                headline = review_form.cleaned_data['headline'],
                body = review_form.cleaned_data['body']
            )
            new_review.save()

            messages.success(request, 'Your review has been posted!')
            return redirect('review_list')
    
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
        'title': 'Nouvelle critique'
    }
    return render(request, 'blog/review/create_review.html', context)


def ticket_create(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES or None)
        if ticket_form.is_valid():
            new_ticket = Ticket.objects.create(
                user = request.user,
                title = ticket_form.cleaned_data['title'],
                body = ticket_form.cleaned_data['body']
            )
            new_ticket.save()

            messages.success(request, 'Created')
            return redirect('review_list')
    
    else:
        ticket_form = TicketForm()
    return render(request, 'blog/review/create_ticket.html', {'ticket_form': ticket_form})


def ticket_respond(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES or None)
        if review_form.is_valid():
            new_review = Review.objects.create(
                ticket = ticket,
                user = request.user,
                headline = review_form.cleaned_data['headline'],
                body = review_form.cleaned_data['body']
            )
            new_review.save()

            messages.success(request, 'Created')
            return redirect('review_list')
    
    else:
        review_form = ReviewForm()
    return render(request, 'blog/review/create_review.html', {'review_form': review_form})


def review_edit(request, id):
    review = get_object_or_404(Review, id=id)

    if review.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()

            messages.success(request, 'Your review has been updated!')
            return redirect('review_detail', id)

    else:
        review_form = ReviewForm(instance=review)

    context = {
        'review_form': review_form,
        'ticket': review.ticket,
        # 'title': 'Update Review'
    }
    return render(request, 'blog/review/create_review.html', context)


def ticket_edit(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if ticket.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()

            messages.success(request, 'Your ticket has been updated!')
            return redirect('ticket_detail', id)

    else:
        ticket_form = TicketForm(instance=ticket)
    return render(request, 'blog/review/create_ticket.html', {'ticket_form': ticket_form})


def ticket_delete(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if ticket.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        ticket.delete()
        return redirect('review_list')

    return render(request, 'blog/review/delete.html', {'ticket': ticket})


def review_delete(request, id):
    review = get_object_or_404(Review, id=id)

    if review.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        review.delete()
        return redirect('review_list')

    return render(request, 'blog/review/delete.html', {'review': review})