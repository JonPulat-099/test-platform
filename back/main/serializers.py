import datetime

from django.http import Http404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from main.models import BaseUser, Test, Question, QuestionAnswer, UserTestAnswer, UserTestResult, ConTest


class BaseUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)    
    u_group_name = serializers.StringRelatedField(source="u_group")     
    
    class Meta:
        model = BaseUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=180, required=True, label='Eski parol')
    password = serializers.CharField(max_length=180, required=True, label='Parol')
    password1 = serializers.CharField(max_length=180, required=True, label='Parolni tasdiqlash')

    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password": "Yangi parol mos emas"})
        return attrs


class ConTestSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.name', required=False, read_only=True)
    test_status = serializers.SerializerMethodField(read_only=True, required=False)
    add_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ConTest
        # exclude = ['updated_at']
        fields = '__all__'

    def get_test_status(self, obj):
        submitted = UserTestResult.objects.filter(contest=obj, user=self.context['request'].user,submitted=True)
        if submitted.exists():
            sub = submitted.last()
            if sub.due_time < datetime.datetime.now() or sub.passed_date:
                return 1  # submitted
            else:
                return 4
        elif obj.start_date > datetime.datetime.now():
            return 2  # not started
        elif obj.end_date < datetime.datetime.now():
            return 3  # not submited and inactive
        else:
            return 4  # active
    
    def get_add_info(self, obj):
        result = UserTestResult.objects.filter(contest=obj, user=self.context['request'].user).first()
        return UserTestResultSerializer(result).data


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ['id', 'value']


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'test', 'question', 'order', 'options']

    def get_options(self, obj):
        data = QuestionAnswer.objects.filter(question=obj)
        return QuestionAnswerSerializer(data, many=True).data


class UserConTestDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField(read_only=True, required=False)
    subject = serializers.CharField(source='subject.name', required=False, read_only=True)
    test_status = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = ConTest
        fields = ['id', 'subject', 'name', 'status', 'test_status', 'questions']

    def get_questions(self, obj):
        test_result = UserTestResult.objects.filter(contest=obj, user=self.context['request'].user).first()
        questions = test_result.questions.all()

        if test_result is None:
            raise Http404('Test is not started')

        return QuestionSerializer(questions, many=True).data

    def get_test_status(self, obj):
        submitted = UserTestResult.objects.filter(contest=obj, user=self.context['request'].user,submitted=True)
        if submitted.exists():
            sub = submitted.last()
            if sub.due_time < datetime.datetime.now() or sub.passed_date:
                return 1  # submitted
            else:
                return 4
        elif obj.start_date > datetime.datetime.now():
            return 2  # not started
        elif obj.end_date < datetime.datetime.now():
            return 3  # not submited and inactive
        else:
            return 4  # active


class UserTestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTestAnswer
        fields = ("id","user","question","answer","contest")
        read_only_fields = ('user',  'contest')

    def create(self, validated_data):
        user = BaseUser.objects.get(id=self.context['request'].user.id)
        question = validated_data.get('question')
        answer = validated_data.get('answer')
        contest = ConTest.objects.get(id=self.context['contest'])
        start = contest.start_date
        end = contest.end_date
        now = datetime.datetime.now()
        if start <= now < end:
            test_result = UserTestResult.objects.filter(contest=contest, user=user).first()
            if now > test_result.due_time:
                raise ValidationError({'message': 'Vaqt tugadi'})
            if test_result is None:  # check if answer belongs to question
                raise ValidationError({'message': 'Test boshlanmagan'})

            allowed_questions = test_result.questions.all()

            if question not in allowed_questions:
                raise ValidationError({'message': 'Bunday savol yo\'q'})

            if not answer.question == question:  # check if answer belongs to question
                raise ValidationError({'message': 'Javob varianti savolga tegishli emas'})

            existint_q_answer = UserTestAnswer.objects.filter(user=user, question=question, contest=contest)
            if existint_q_answer.exists():
                raise ValidationError({'message': 'Savolga javob berilgan'})
            else:
                u_answer = UserTestAnswer.objects.create(user=user, contest=contest,
                                                         correct_answer=answer.correct_answer,
                                                         **validated_data)
            return u_answer
        else:
            raise ValidationError(
                {'message': 'Test faol emas'})  # id start date is grater than now or end date is less than now

class UserTestAnswerSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTestAnswer
        fields = ("user","question","answer","contest", "correct_answer")
        read_only_fields = ('user',  'contest')


class UserTestResultSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='contest.name', required=False, read_only=True)

    class Meta:
        model = UserTestResult
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
