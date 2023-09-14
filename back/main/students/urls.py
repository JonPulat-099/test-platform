from django.urls import path
from . import views

urlpatterns = [
    path('contests/',views.ConTestListView.as_view(),name='api-contest-list'),
    path('contests/<int:pk>/start/',views.ConTestStartView.as_view(),name='api-contest-start'),
    path('contests/answer/',views.UserConTestAnswerView.as_view(),name='api-contest-answer'),
]
