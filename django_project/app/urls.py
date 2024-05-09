from django.urls import include, path

from .views import ask_question, UnknownQuestionViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'uk', UnknownQuestionViewSet)


urlpatterns = [
    path('ask_question', ask_question),
    path('', include(router.urls))
    # path('kaka', UnknownQuestionViewSet.as_view)
]
