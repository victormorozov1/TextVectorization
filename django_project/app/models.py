from .constants import PHRASE_MAX_LENGTH
from django.db.models import AutoField, CharField, ForeignKey, IntegerField, JSONField, Model, PROTECT, TextField


class Topic(Model):
    answer = TextField(max_length=3000)
    name = CharField(max_length=30, null=True)  # TODO: null=False

    def __str__(self) -> str:
        return self.name or ''


class Phrase(Model):
    content = CharField(max_length=PHRASE_MAX_LENGTH)
    embedding = JSONField(null=True, blank=True)
    topic = ForeignKey(Topic, on_delete=PROTECT, null=True)

    def __str__(self) -> str:
        return f'{self.content[:120]}' + ('...' if len(self.content) > 120 else '')


class UnknownQuestion(Model):
    question = ForeignKey(Phrase, on_delete=PROTECT)
    user_select_answer = ForeignKey(Topic, on_delete=PROTECT)
