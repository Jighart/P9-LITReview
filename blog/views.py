from django.contrib import messages
from django.db.models import CharField, Value
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

from itertools import chain
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review
from .feed import get_user_viewable_reviews, get_user_viewable_tickets


def feed(request):
    reviews = get_user_viewable_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_user_viewable_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

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
        'title': 'Feed',
    }

    return render(request, 'blog/review/feed.html', context)


def own_posts(request):
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

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
        'title': 'Vos posts',
    }

    return render(request, 'blog/review/feed.html', context)


def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    review = None

    if ticket.has_review:
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
                user=request.user,
                title=ticket_form.cleaned_data['title'],
                body=ticket_form.cleaned_data['body'],
                picture=ticket_form.cleaned_data['picture'],
                has_review=True,
            )
            new_ticket.save()

            new_review = Review.objects.create(
                ticket=new_ticket,
                user=request.user,
                headline=review_form.cleaned_data['headline'],
                body=review_form.cleaned_data['body'],
                rating=review_form.cleaned_data['rating'],
            )
            new_review.save()

            messages.success(request, 'Votre critique a été publiée !')
            return redirect('feed')

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
                user=request.user,
                title=ticket_form.cleaned_data['title'],
                body=ticket_form.cleaned_data['body'],
                picture=ticket_form.cleaned_data['picture'],
            )
            new_ticket.save()

            messages.success(request, 'Votre ticket a été créé !')
            return redirect('feed')

    else:
        ticket_form = TicketForm()
    return render(request, 'blog/review/create_ticket.html', {'ticket_form': ticket_form})


def ticket_respond(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    review_form = ReviewForm(request.POST)

    if ticket.has_review:
        messages.error(request, 'Ce ticket a déjà reçu une critique en réponse')
        return redirect('/ticket/' + id)

    if request.method == 'POST' and review_form.is_valid():
        new_review = Review.objects.create(
            ticket=ticket,
            user=request.user,
            headline=review_form.cleaned_data['headline'],
            body=review_form.cleaned_data['body'],
            rating=review_form.cleaned_data['rating'],
        )
        new_review.save()

        ticket.has_review = True
        ticket.save()
        messages.success(request, 'Vous avez répondu au ticket !')
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

            messages.success(request, 'Votre critique a été modifiée !')
            return redirect('ticket_detail', review.ticket.id)

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

            messages.success(request, 'Votre ticket a été modifié !')
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
        messages.info(request, 'Votre ticket a été supprimé !')
        return redirect('feed')

    return render(request, 'blog/review/delete.html', {'ticket': ticket})


def review_delete(request, id):
    review = get_object_or_404(Review, id=id)

    if review.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        ticket = Ticket.objects.get(id=review.ticket.id)
        ticket.has_review = False
        ticket.save()

        review.delete()
        messages.info(request, 'Votre critique a été supprimée !')
        return redirect('feed')

    return render(request, 'blog/review/delete.html', {'review': review})
