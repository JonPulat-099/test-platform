from django.template.loader import render_to_string
from django.utils.timezone import datetime, timedelta
from django.utils import timezone
import xlrd

# Create your views here.
from rest_auth.views import LoginView
from rest_framework import status, serializers, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import BaseUser, Test, ConTest, UserTestAnswer, UserTestResult, Question, QuestionAnswer, UserGroup
from main.pagination import CustomPagination
from main.serializers import BaseUserSerializer, PasswordResetSerializer, UserConTestDetailSerializer, \
    UserTestAnswerSerializer, ConTestSerializer, UserTestResultSerializer, TestSerializer, UserTestAnswerSubmitSerializer
from django.http import HttpResponse


import pdfkit
from main.models import UserTestResult
from .tasks import limit_test_task


class UserLoginView(LoginView):

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data, context={'request': request})
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()

    def get_response(self):
        original_response = super().get_response()
        token = Token.objects.get(key=original_response.data['key'])
        user = BaseUser.objects.get(id=token.user.id)
        data = {
            'message': 'Successfully logged in',
            'status': 200,
            'token': token.key
        }
        original_response.data.update(data)
        return Response(data)


# LOGOUT
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# LOGOUT
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BaseUserSerializer

    def get(self, request, format=None):
        user = self.request.user
        data = self.serializer_class(user).data
        return Response(data)


class PasswordResetView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not instance.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Parol noto'g'ri"]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            instance.set_password(serializer.data.get("password"))
            instance.save()
            response = {
                'status': 'success',
                'message': 'Parol muvafaqqiyatli yangilandi',
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTestListView(generics.ListAPIView):
    queryset = ConTest.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ConTestSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        user = self.request.user
        user = BaseUser.objects.get(id=user.id)
        g_tests = ConTest.objects.filter(group__in=[user.u_group], status=True)
        # queryset = Test.objects.filter(id__in=Subquery(g_tests.values('test_id'))).order_by('-start_date')
        page = self.paginate_queryset(g_tests)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': self.request})
            return self.get_paginated_response(serializer.data)


class UserTestDetailView(generics.RetrieveAPIView):
    queryset = ConTest.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserConTestDetailSerializer


class UserTestAnswersCreateView(generics.ListCreateAPIView):
    queryset = UserTestAnswer.objects.all()
    serializer_class = UserTestAnswerSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, pk=None, *args, **kwargs):
        user = self.request.user
        data = UserTestAnswer.objects.filter(user=user, contest=pk)
        serializers = self.get_serializer(data, many=True, context={'contest': pk, 'request': self.request})

        try:
            contest = ConTest.objects.get(id=pk)
            result = UserTestResult.objects.get(user=user, contest=contest)
            end = result.due_time
            now = timezone.now()
            if result.submitted or result.passed_date or end < now:
                serializers = UserTestAnswerSubmitSerializer(
                    data, many=True, context={'contest': pk, 'request': self.request})
        except Exception as e:  # noqa
            print(e)
            pass

        return Response(serializers.data)

    def post(self, request, pk=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'contest': pk, 'request': self.request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserTestAnswersUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserTestAnswer.objects.all()
    serializer_class = UserTestAnswerSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        now = datetime.now()
        contest = instance.contest
        user = request.user
        if contest.start_date >= now or now >= contest.end_date:
            return Response({'message': 'Test faol emas!'}, status=status.HTTP_400_BAD_REQUEST)
        result = UserTestResult.objects.get(user=user, contest=contest)
        if now > result.due_time:
            return Response({'message': "Test vaqti tugagan!"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            qa = serializer.validated_data.get('answer')
            instance.answer = qa
            instance.correct_answer = qa.correct_answer
            instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestSubmitView(APIView):

    def get_ip_address(self, request):
        ip_adress: str
        user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip_address:
            ip_adress = user_ip_address.split(',')[0]
        else:
            ip_adress = request.META.get('REMOTE_ADDR')
        return ip_adress

    def post(self, request, pk=None):
        user = self.request.user
        # test
        g_tests = ConTest.objects.filter(group__in=[user.u_group], status=True)
        test_len = g_tests.count()
        is_submitted = 0
        total = 0
        max = 0
        for c in g_tests:
            result = UserTestResult.objects.filter(contest=c, user=user,submitted=True)
            if result.count() > 0:
                max += c.grade_per_question * (result[0].correct_answers_count + result[0].incorrect_answers_count)
                total += result[0].overall_ball
                is_submitted += 1
        # test

        try:
            contest = ConTest.objects.get(id=pk)
        except ValueError:
            return Response({"message": "test topilmadi"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = UserTestResult.objects.get(contest=contest, user=user)
        except UserTestResult.DoesNotExist:
            return Response({'message': "Test mavjud emas"}, status=status.HTTP_404_NOT_FOUND)
        if result:
            now = datetime.now()
            if result.due_time < now:
                return Response({'message': "Vaqt tugadi"}, status=status.HTTP_400_BAD_REQUEST)
            elif result.submitted:
                return Response({'message': "Test avval saqlangan"}, status=status.HTTP_400_BAD_REQUEST)

            questions = result.questions.all()
            answers = UserTestAnswer.objects.filter(contest=result.contest, correct_answer=True, user=user)
            result.submitted = True
            result.passed_date = now
            result.status = False
            result.correct_answers_count = len(answers)
            result.incorrect_answers_count = len(questions) - len(answers)
            questions_len = len(questions)
            if questions_len == 0:
                questions_len = 1

            percentage = round(100 * len(answers) / questions_len)
            overall_ball = contest.grade_per_question * len(answers)
            # test
            start_percent = 2
            end_percent = 30
            additional_percent = 30
            print('test_len: ', test_len, 'is_submitted: ', is_submitted, 'total: ', total, 'max: ', max)
            if test_len == 1 and is_submitted == 0:
                print('if -> 1: ', overall_ball, percentage)
                if (percentage < end_percent and percentage > start_percent):
                    overall_ball += (additional_percent * (contest.grade_per_question * len(questions)))/100
                    percentage = round(percentage + additional_percent)
                    print('success: ', overall_ball, percentage)
            if (test_len == 2 and is_submitted == 1):
                total += overall_ball
                max += contest.grade_per_question * len(questions)
                p = round((total / max) * 100, 2)
                print('if -> 2: ', overall_ball, percentage, total, max, 'percent -> ', p, p < end_percent and p > start_percent)
                if (p < end_percent and p > start_percent):
                    overall_ball += (additional_percent * max)/100
                    percentage = round((overall_ball * 100) / (contest.grade_per_question * len(questions)))
                    print('success: ', overall_ball, percentage)
            # test
            result.percentage = percentage
            result.overall_ball = round(overall_ball, 1)
            result.point = result.correct_answers_count * 2
            result.ip_address = self.get_ip_address(request)
            result.save()
            serializer = UserTestResultSerializer(result, many=False).data
            return Response({"message": "Test topshirildi", "data": serializer}, status=status.HTTP_200_OK)
        return Response({"message": "test topshirilgan"}, status=status.HTTP_400_BAD_REQUEST)


class TestResultView(generics.RetrieveAPIView):
    queryset = UserTestResult.objects.all()
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, *args, **kwargs):
        user = self.request.user
        data = UserTestResult.objects.filter(contest__id=pk, user=user).first()
        if data:
            serializer = UserTestResultSerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Foydalanuvchi natichasi topilmadi'}, status=status.HTTP_404_NOT_FOUND)


class TestResultListView(generics.ListAPIView):
    queryset = UserTestResult.objects.all()
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        data = UserTestResult.objects.filter(user=user)
        serializer = UserTestResultSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContestStart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        contest = ConTest.objects.filter(id=pk).first()
        user = self.request.user
        if contest:
            check_existing = UserTestResult.objects.filter(user=user, contest=contest).first()
            if not check_existing:
                due_time = datetime.now() + timedelta(minutes=contest.duration)
                if due_time <= contest.end_date:
                    result = UserTestResult.objects.create(user=user, contest=contest, status=True,
                                                           due_time=due_time)
                else:
                    result = UserTestResult.objects.create(user=user, contest=contest, status=True,
                                                           due_time=contest.end_date)
                limit_test_task.delay(contest.duration, result.id)

                questions = Question.objects.filter(test=contest.test).order_by('?')[:30]
                result.questions.set(questions)
                result.save()
                return Response(
                    {"time": result.start_time, "duration": result.contest.duration, 'due_time': result.due_time,
                     'message': 'Just started'}, status=status.HTTP_200_OK)
            return Response({"time": check_existing.start_time, "duration": check_existing.contest.duration,
                             'message': 'already started'}, status=status.HTTP_200_OK)
        return Response({'message': 'Test topilmadi'}, status=status.HTTP_404_NOT_FOUND)


class TestListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Test.objects.filter(status=True)
    serializer_class = TestSerializer
    pagination_class = None


class QuestionsCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not self.request.user.is_student:
            try:
                test = self.request.data.get('test')
                data = self.request.data.get('data')
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            test = Test.objects.filter(id=int(test)).first()
            for item in data:
                question = Question.objects.create(test=test, question=item['question'])
                for option in item['answers']:
                    QuestionAnswer.objects.create(question=question, value=option['answer'],
                                                  correct_answer=option['isCorrect'])
            return Response(status=status.HTTP_200_OK)
        return Response({"message": 'Only admin users can create questions'}, status=status.HTTP_400_BAD_REQUEST)


def generate_pdf(request, user_test_id):
    """Generate pdf."""
    # Model data
    people = generics.get_object_or_404(UserTestResult.objects.filter(submitted=True), id=user_test_id)
    if not people.point:
        people.point = people.correct_answers_count * 3
        print(people.point)
    print(people.point)
    people.save()
    payload = {
        'first_name': people.user.first_name,
        'last_name': people.user.last_name,
        'middle_name': people.user.middle_name,
        'u_group': people.user.u_group,
        'title': people.contest.name,
        'point': people.point or 0,
    }

    # Rendered
    html_string = render_to_string('result_remplate.html', payload)
    result = pdfkit.from_string(html_string, False)

    #
    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = f'inline; filename={people.user.full_name}.pdf'

    return response

class CreatUsers(APIView):
    print('start')
    def post(self, request):
        if request.method == 'POST':
            try:
                file = request.FILES.get('file')
                book = xlrd.open_workbook(file.name, file_contents=file.read())
                sheet = book.sheets()[0]
                for rx in range(1,sheet.nrows):
                    row = sheet.row(rx)

                    user = BaseUser.objects.create(
                        first_name=row[1].value,
                        last_name=row[2].value,
                        middle_name=row[3].value,
                        u_group=UserGroup.objects.get_or_create(name=str(row[4].value).strip())[0],
                        username=row[6].value,
                        is_student=True
                    )
                    user.set_password(row[7].value)
                    user.save()
                return Response({"message": "Foydalanuvchilar qo'shildi"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message":  "No to`g`ri so`rov"}, status=status.HTTP_400_BAD_REQUEST)
    

def multi_generate_pdf(request, user_id):
    user = generics.get_object_or_404(BaseUser.objects.filter(id=user_id))
    user.save()
    tests = UserTestResult.objects.filter(user=user, submitted=True)
    total = 0
    for t in tests:
        total += t.overall_ball

    payload = {
        'id': user_id,
        'user_name': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'middle_name': user.middle_name,
        'u_group': user.u_group,
        'tests': tests,
        'total': round(total, 1)
    }
     # Rendered
    html_string = render_to_string('pdf.html', payload)
    result = pdfkit.from_string(html_string, False)

    #
    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = f'inline; filename={user.full_name}.pdf'

    return response