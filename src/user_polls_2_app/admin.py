from django.contrib import admin
from user_polls_2_app.models import Poll, PollQuestion, PollAnswer, UserAnswer, PollsAssignedToUsers


class PollAdmin(admin.ModelAdmin):
    model = Poll
    readonly_fields = ('date_start', )
    fieldsets = (
        (None, {'fields': ('name', 'description', 'date_start', 'date_finish', 'is_active', )}),
    )


class PollQuestionAdmin(admin.ModelAdmin):
    model = PollQuestion
    fieldsets = (
        (None, {'fields': ('poll', 'type', 'text', )}),
    )


class PollAnswerAdmin(admin.ModelAdmin):
    model = PollAnswer
    fieldsets = (
        (None, {'fields': ('question', 'text', )}),
    )


class UserAnswerAdmin(admin.ModelAdmin):
    model = UserAnswer
    fieldsets = (
        (None, {'fields': ('user', 'anonymous_user_id', 'choice_answer', 'text_answer', )}),
    )


class PollsAssignedToUsersAdmin(admin.ModelAdmin):
    model = PollsAssignedToUsers
    fieldsets = (
        (None, {'fields': ('poll', 'user', 'is_active', )}),
    )


admin.site.register(Poll, PollAdmin)
admin.site.register(PollQuestion, PollQuestionAdmin)
admin.site.register(PollAnswer, PollAnswerAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(PollsAssignedToUsers, PollsAssignedToUsersAdmin)
