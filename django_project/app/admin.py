from django.contrib import admin
from .models import Phrase, Topic, UnknownQuestion


class PhraseAdmin(admin.ModelAdmin):
    list_display = ('topic', 'content')
    list_display_links = list_display
    fields = ('content', 'topic')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'answer')
    list_display_links = list_display


class UnknownQuestionAdmin(admin.ModelAdmin):
    list_display = ('user_select_topic', 'question')
    list_display_links = list_display


admin.site.register(Phrase, PhraseAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(UnknownQuestion, UnknownQuestionAdmin)
