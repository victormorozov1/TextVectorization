from .constants import PHRASE_MAX_LENGTH
from django.db.models import CharField, ForeignKey, IntegerField, JSONField, Model, PROTECT, TextField


class Topic(Model):
    id = IntegerField(primary_key=True)
    answer = TextField(max_length=3000)


class Phrase(Model):
    id = IntegerField(primary_key=True)
    content = CharField(max_length=PHRASE_MAX_LENGTH)
    embedding = JSONField(null=True, blank=True)
    topic = ForeignKey(Topic, on_delete=PROTECT, null=True)


class UnknownQuestion(Model):
    question = ForeignKey(Phrase, on_delete=PROTECT)
    user_select_answer = ForeignKey(Topic, on_delete=PROTECT)
