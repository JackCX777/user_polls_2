from datetime import datetime
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import PollsAssignedToUser, Poll


class PaginationPolls(PageNumberPagination):
    page_size = 2
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'links': {'next': self.get_next_link(), 'previous': self.get_previous_link()},
            'results': data
        })


class AvailablePollsMixin:
    def update_polls(self):
        spoilt_polls = Poll.objects.filter(Q(is_active=True) & Q(date_finish__lt=datetime.now()))

        for spoilt_poll in spoilt_polls:
            polls_for_editing = PollsAssignedToUser.objects.filter(poll_id=spoilt_poll.id)
            for poll in polls_for_editing:
                poll.is_active = False
                poll.save()

    def get_polls_for_new_user(self):
        polls = Poll.objects.filter(is_active=True)

        if self.request.user.is_authenticated:
            for poll in polls:
                p = PollsAssignedToUser(poll=poll, user=self.request.user, anonymous_user_id=None, is_active=True)
                p.save()
            return PollsAssignedToUser.objects.filter(user=self.request.user)
        else:
            for poll in polls:
                p = PollsAssignedToUser(poll=poll, anonymous_user_id=self.request.session.session_key, is_active=True)
                p.save()
            return PollsAssignedToUser.objects.filter(anonymous_user_id=self.request.session.session_key)

    def get_personalised_polls(self):
        if self.request.user.is_authenticated:
            queryset = PollsAssignedToUser.objects.filter(user=self.request.user)

            if not queryset:
                if self.request.user.groups.filter(name='Poll users').exists():
                    queryset = self.get_polls_for_new_user()
                else:
                    # messages.error(self.request, 'You are not allowed to take polls')
                    print('You are not allowed to take polls')
        else:
            queryset = PollsAssignedToUser.objects.filter(anonymous_user_id=self.request.session.session_key)
            if not queryset:
                queryset = self.get_polls_for_new_user()

        self.update_polls()

        return queryset.filter(is_active=True)
