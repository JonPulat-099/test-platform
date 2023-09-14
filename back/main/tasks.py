from django.utils.timezone import datetime
from celery.task import task
from time import sleep
from .models import UserTestResult, UserTestAnswer
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@task(name='limit_test_task')
def limit_test_task(minute, result_id):
    logger.info("-------\n---------\n\n-----------\n-----------")
    sleep((minute * 60) + 2)
    try:
        logger.info("-------\n---------\n\n-----------\n-----------")
        result = UserTestResult.objects.get(id=result_id)
        if not result.submitted:
            user = result.user
            questions = result.questions.all()
            answers = UserTestAnswer.objects.filter(contest=result.contest, correct_answer=True, user=user)
            result.submitted = True
            result.passed_date = datetime.now()
            result.status = False
            result.correct_answers_count = len(answers)
            result.incorrect_answers_count = len(questions) - len(answers)
            questions_len = len(questions)
            if questions_len == 0:
                questions_len = 1
            result.percentage = round(100 * len(answers) / questions_len)
            result.point = result.correct_answers_count * 2
            logger.info(result.point)
            logger.info("-------\n---------\n\n-----------\n-----------")

            result.save()
    except Exception as e:
        logger.exception(e)
        logger.info(e)
        logger.info("-------\n---------\n\n-----------\n-----------")

        print(e)
        pass
    return (f'{result_id} :task_done')
