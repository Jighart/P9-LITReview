from django.contrib.auth.models import User

from blog.models import Review, Ticket
from accounts.models import UserFollow


def get_user_follows(user):
    follows = UserFollow.objects.filter(user=user)
    followed_users = []
    for follow in follows:
        followed_users.append(follow.followed_user)
    
    return followed_users


def get_user_viewable_reviews(user: User):
    followed_users = get_user_follows(user)
    followed_users.append(user)

    reviews = []
    all_reviews = Review.objects.filter(user__in=followed_users).distinct()
    for review in all_reviews:
        reviews.append(review.id)

    own_tickets = Ticket.objects.filter(user=user)
    for ticket in own_tickets:
        received_responses = Review.objects.filter(ticket=ticket)
        for review in received_responses:
            reviews.append(review.id)

    reviews = Review.objects.filter(id__in=reviews).distinct()

    return reviews


def get_user_viewable_tickets(user: User):
    """
    All viewable tickets for user feed:
    Tickets by followed users + current user
    Filter out tickets with review response if review author is followed
    @param user: currently logged-in User instance
    @return: filtered tickets queryset
    """
    followed_users = get_user_follows(user)
    followed_users.append(user)

    tickets = Ticket.objects.filter(user__in=followed_users)
    for ticket in tickets:
        try:
            replied = Review.objects.get(ticket=ticket)
            if replied and replied.user in followed_users:
                tickets = tickets.exclude(id=ticket.id)

        except Review.DoesNotExist:
            pass

    return tickets
