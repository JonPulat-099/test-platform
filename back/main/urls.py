from django.test import TestCase

# Create your tests here.
from django.urls import path, include

# INTERNAL MODULES
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), {}, name='login'),
    path('logout/', views.UserLogoutView.as_view(), {}, name='logout'),
 
    path('password-reset/', views.PasswordResetView.as_view(), {}, name='password-reset'),
    path('profile/', views.UserProfileView.as_view(), {}, name='profile'),

    path('tests/', views.UserTestListView.as_view(), {}, name='user_tests'),
    path('tests/<int:pk>/', views.UserTestDetailView.as_view(), {}, name='user_test_detail'),
    path('tests/<int:pk>/submit/', views.TestSubmitView.as_view(), {}, name='user_test_submit'),
    path('tests/<int:pk>/result/', views.TestResultView.as_view(), {}, name='user_test_result'),
    path('tests/<int:pk>/start/', views.ContestStart.as_view(), {}, name='user_test_start'),
    path('results/', views.TestResultListView.as_view(), {}, name='user_test_result_list'),

    path('tests/<int:pk>/question-answer/', views.UserTestAnswersCreateView.as_view(), name='question-answer'),
    path('question-answer/<int:pk>/', views.UserTestAnswersUpdateView.as_view(), name='question-answer-update'),
    path('core-tests/', views.TestListView.as_view(), name='core_test_view'),
    path('q-create/', views.QuestionsCreateApiView.as_view(), name='question_create'),
    path('pdf/<int:user_test_id>/', views.generate_pdf, name='generate_pdf'),
    path('multi-pdf/<int:user_id>/', views.multi_generate_pdf, name='multi_pdf'),
    path('users/', views.CreatUsers.as_view(), name='user_create'),
]
