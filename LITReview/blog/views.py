from django.contrib import messages
from django.db.models import CharField, Value
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
# from django.views import generic
# from django.utils.datastructures import MultiValueDictKeyError

from itertools import chain
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review
from .feed import get_user_viewable_reviews, get_user_viewable_tickets, get_user_follows, get_replied_tickets


def feed(request):
    followed_users = get_user_follows(request.user)

    reviews = get_user_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_user_viewable_tickets(request.user) 
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    replied_tickets, replied_reviews = get_replied_tickets(tickets)

    posts = sorted(
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True
    )

    if posts:
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
    else:
        posts = None

    context = {
        'posts': posts,
        # 'r_tickets': replied_tickets,
        # 'r_reviews': replied_reviews,
        'title': 'Feed',
        # 'followed_users': followed_users
    }

    return render(request, 'blog/review/list.html', context)


def own_posts(request):
    user = request.user

    followed_users = get_user_follows(request.user)

    reviews = Review.objects.filter(user=user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.filter(user=user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    replied_tickets, replied_reviews = get_replied_tickets(tickets)

    posts = sorted(
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True
    )

    context = {
        'posts': posts,
        # 'r_tickets': replied_tickets,
        # 'r_reviews': replied_reviews,
        'title': 'Feed',
        # 'followed_users': followed_users
    }

    return render(request, 'blog/review/list.html', context)


def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    review = None
    if ticket.review_id:
        review = Review.objects.get(ticket=ticket)

    context = {
        'ticket': ticket,
        'review': review,
    }

    return render(request, 'blog/review/ticket_detail.html', context)    



def review_create(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES or None)
        review_form = ReviewForm(request.POST)
        if all([ticket_form.is_valid() and review_form.is_valid()]):
            new_ticket = Ticket.objects.create(
                user = request.user,
                title = ticket_form.cleaned_data['title'],
                body = ticket_form.cleaned_data['body'],
                picture = ticket_form.cleaned_data['picture'],
            )

            new_review = Review.objects.create(
                ticket = new_ticket,
                user = request.user,
                headline = review_form.cleaned_data['headline'],
                body = review_form.cleaned_data['body'],
                rating = review_form.cleaned_data['rating'],
            )

            new_ticket.review_id = new_review.id
            new_ticket.save()
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
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            picture = request.FILES.get('picture', None)
            new_ticket = Ticket.objects.create(
                user = request.user,
                title = ticket_form.cleaned_data['title'],
                body = ticket_form.cleaned_data['body'],
                picture = picture,
            )
            new_ticket.save()

            messages.success(request, 'Created')
            return redirect('review_list')
    
    else:
        ticket_form = TicketForm()
    return render(request, 'blog/review/create_ticket.html', {'ticket_form': ticket_form})


def ticket_respond(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    review_form = ReviewForm(request.POST)

    if ticket.review_id is not None:
        messages.error(request, 'Ce ticket a déjà reçu une critique en réponse')
        return redirect('/ticket/' + id)

    if request.method == 'POST' and review_form.is_valid():
        new_review = Review.objects.create(
                ticket = ticket,
                user = request.user,
                headline = review_form.cleaned_data['headline'],
                body = review_form.cleaned_data['body'],
                rating = review_form.cleaned_data['rating'],
            )
        new_review.save()

        ticket.review_id = new_review.id
        ticket.save()
        messages.success(request, 'Your review has been posted!')
        return redirect('/ticket/' + id)
    
    else:
        review_form = ReviewForm()

    context = {
        'ticket': ticket,
        'review_form': review_form,
        'title': 'Nouvelle critique'
    }
    return render(request, 'blog/review/create_review.html', context)


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
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()

            messages.success(request, 'Your ticket has been updated!')
            return redirect('ticket_detail', id)

    else:
        ticket_form = TicketForm(instance=ticket)

        context = {
            'ticket_form': ticket_form,
            'ticket': ticket,
            # 'title': 'Update Review'
    }
    return render(request, 'blog/review/create_ticket.html', context)


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
        ticket = Ticket.objects.get(id=review.ticket.id)
        ticket.review_id = None
        ticket.save()

        review.delete()
        return redirect('review_list')

    return render(request, 'blog/review/delete.html', {'review': review})

# ----------------------------------


