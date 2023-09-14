# Create your views here.
from rest_auth.views import LoginView
from rest_framework import status, generics, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.timezone import datetime, timedelta
from .permissions import StudentOnlyPermission
from main import models
from main.pagination import CustomPagination
from . import serializers


class ConTestListView(generics.ListAPIView):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    queryset = models.ConTest.objects.select_related('test').prefetch_related('group')
    serializer_class = serializers.ConTestListSerializer

    def get_queryset(self):
        if self.request.user.is_student:
            return self.queryset.filter(group=self.request.user.u_group)
        return self.queryset


class ConTestStartView(generics.RetrieveAPIView):
    pagination_class = CustomPagination
    permission_classes = [StudentOnlyPermission]
    queryset = models.ConTest.objects.select_related('test')
    serializer_class = serializers.ConTestStartUserTestResultSerializer

    def get_object(self):
        user = self.request.user
        now = datetime.now()
        queryset = self.queryset.filter(group=user.u_group, start_date__lte=now, end_date__gte=now)
        contest = generics.get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        due_time = now + timedelta(minutes=contest.duration)
        try:
            if due_time <= contest.end_date:
                instance = models.UserTestResult.objects.create(user=user, contest=contest, due_time=due_time)
            else:
                instance = models.UserTestResult.objects.create(user=user, contest=contest, due_time=contest.end_date)
            # TODO vaqtni tugatish feature qoshish kerak
            return instance
        except:
            raise exceptions.NotFound()


class UserConTestAnswerView(generics.CreateAPIView):
    pagination_class = CustomPagination
    permission_classes = [StudentOnlyPermission]
    # queryset = models.UserConTestAnswer.objects.all()
    # serializer_class = serializers.UserConTestAnswerSerializer
    #
    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     data = serializer.data
    #     self.queryset.model.objects.update_or_create(user_test_id=data.get('user_test'),
    #                                                  question_id=data.get('question'),
    #                                                  defaults={'answer_id': data.get('answer')})
    #     # self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response({}, status=status.HTTP_201_CREATED, headers=headers)



class ConTestFinishView(generics.RetrieveAPIView):
    pagination_class = CustomPagination
    permission_classes = [StudentOnlyPermission]
    queryset = models.ConTest.objects.select_related('test')
    serializer_class = serializers.ConTestStartUserTestResultSerializer

    def get_object(self):
        user = self.request.user
        now = datetime.now()
        queryset = self.queryset.filter(group=user.u_group, start_date__lte=now, end_date__gte=now)
        contest = generics.get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        due_time = now + timedelta(minutes=contest.duration)
        try:
            if due_time <= contest.end_date:
                instance = models.UserTestResult.objects.create(user=user, contest=contest, due_time=due_time)
            else:
                instance = models.UserTestResult.objects.create(user=user, contest=contest, due_time=contest.end_date)
            # TODO vaqtni tugatish feature qoshish kerak
            return instance
        except:
            raise exceptions.NotFound()

