import logging
import numpy as np
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from scipy.spatial.distance import cdist

from .constants import EMBEDDING_FOUND_ANSWER_LEVEL
from .embedding import get_embedding, get_or_load_phrase_embedding
from .models import Phrase, UnknownQuestion

logger = logging.getLogger(__name__)


@api_view(['GET'])
def ask_question(request):
    # TODO validation
    question = request.data['question']

    logger.info(f'Received {question=}')

    question_embedding = get_embedding(question)

    phrases = list(Phrase.objects.all())

    # Вычисляем косинусное расстояние
    dist = cdist(
        question_embedding[None, :],
        [get_or_load_phrase_embedding(phrase) for phrase in phrases],
        metric='cosine',
    )

    # Вычисляем косинусное сходство
    sim = 1 - dist

    if sim.max() > EMBEDDING_FOUND_ANSWER_LEVEL:
        return Response({'found_answer': True, 'answer': phrases[np.argmax(sim)].topic.answer})
    else:
        sim.resize(sim.shape[1])
        top3_questions = []
        used_topics = []
        for i in np.argpartition(sim, -len(sim)):
            question = phrases[i]
            if question.topic_id not in used_topics:
                used_topics.append(question.topic_id)
                top3_questions.append(question)
            if len(top3_questions) == 3:
                break

        return Response(
            {
                'found_answer': False,
                'possible_answers': [
                    {
                        'topic_id': question.topic.id,
                        'topic': question.topic.name,
                        'answer': question.topic.answer,
                    }
                    for question in top3_questions
                ],
            }
        )


class UnknownQuestionSerializer(ModelSerializer):
    class Meta:
        model = UnknownQuestion
        fields = ['question', 'user_select_topic']


class UnknownQuestionViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UnknownQuestion.objects.all()
    serializer_class = UnknownQuestionSerializer
