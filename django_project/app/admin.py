from django.contrib import admin, messages
from django.db.models import QuerySet
from .models import Phrase, Topic, UnknownQuestion


class PhraseAdmin(admin.ModelAdmin):
    list_display = ('topic', 'content')
    list_display_links = list_display
    fields = ('content', 'topic')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'answer')
    list_display_links = list_display


class UnknownQuestionAdmin(admin.ModelAdmin):
    list_display = ('select_topic', 'question', 'resolved')
    list_display_links = list_display

    @admin.action(description='Создать вопросы')
    def create_questions(self, request, queryset: QuerySet[UnknownQuestion]):
        questions: list[Phrase] = []
        unknown_questions: list[UnknownQuestion] = []

        for unknown_question in queryset:
            if unknown_question.select_topic is None:
                messages.warning(
                    request,
                    f'Нельзя создать вопрос {unknown_question}, так как у него не указана тема',
                )
            elif unknown_question.resolved:
                messages.warning(
                    request,
                    f'Вопрос {unknown_question} уже помечен решенным. Вопрос повторно создан не будет.',
                )
            else:
                questions.append(Phrase(content=unknown_question.question, topic=unknown_question.select_topic))
                unknown_question.resolved = True
                unknown_questions.append(unknown_question)

        messages.info(request, f'Созданные вопросы: {Phrase.objects.bulk_create(questions)}')
        UnknownQuestion.objects.bulk_update(unknown_questions, fields=('resolved',))

    actions = [create_questions]


admin.site.register(Phrase, PhraseAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(UnknownQuestion, UnknownQuestionAdmin)
