from django.contrib import admin
from .models import Phrase, Topic, UnknownQuestion

admin.site.register(Phrase)
admin.site.register(Topic)
admin.site.register(UnknownQuestion)
