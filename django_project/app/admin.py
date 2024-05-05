from django.contrib import admin
from .models import Phrase, Topic, UnknownQuestion


class PhraseAdmin(admin.ModelAdmin):
    fields = ('content', 'topic')


admin.site.register(Phrase, PhraseAdmin)
admin.site.register(Topic)
admin.site.register(UnknownQuestion)
