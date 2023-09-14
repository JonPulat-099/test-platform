from django.db.models import Q
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from main.models import UserTestResult, Question, UserTestAnswer


class TestResultCheck(MiddlewareMixin):
    def process_response(self, request, response):
        results = UserTestResult.objects.filter(submitted=False, status=True, due_time__lte=timezone.datetime.now())
        if results:
            for i in results:
                i.submitted = True
                i.status = False
                i.passed_date = i.due_time
                questions = i.questions.all()
                answers = UserTestAnswer.objects.filter(contest=i.contest, correct_answer=True)
                i.correct_answers_count = len(answers)
                i.incorrect_answers_count = len(questions) - len(answers)
                questions_len = len(questions)
                if questions_len == 0:
                    questions_len = 1
                i.percentage = round(100*len(answers)/questions_len)
                i.save()

        results = UserTestResult.objects.filter(
            Q(percentage__gt=100) | Q(percentage__lt=0)
        )
        results.delete()
        return response
