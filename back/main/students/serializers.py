import datetime

from django.http import Http404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from main import models


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ['id', 'name', 'language', 'status']


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
        fields = ['id', 'name', 'language']


class ConTestTestSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = models.Test
        fields = ['id', 'name', 'subject', 'status']


class ConTestListSerializer(serializers.ModelSerializer):
    group = StudentGroupSerializer(many=True)
    test = ConTestTestSerializer()

    class Meta:
        model = models.ConTest
        fields = ['id', 'name', 'test', 'group', 'start_date', 'end_date', 'duration', 'status']


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionAnswer
        fields = ['id', 'value']


class ConTestStartQuestionSerializer(serializers.ModelSerializer):
    answers = QuestionAnswerSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ['id', 'question', 'order', 'answers']


class ConTestStartTestSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    questions = ConTestStartQuestionSerializer(many=True)

    class Meta:
        model = models.Test
        fields = ['id', 'name', 'status', 'subject', 'questions']


class ConTestStartSerializer(serializers.ModelSerializer):
    test = ConTestStartTestSerializer()

    class Meta:
        model = models.ConTest
        fields = ['id', 'name', 'start_date', 'end_date', 'duration', 'status', 'test']


class ConTestStartUserTestResultSerializer(serializers.ModelSerializer):
    contest = ConTestStartSerializer()

    class Meta:
        model = models.UserTestResult
        fields = ['id', 'start_time', 'due_time', 'contest']





class ConTestFinishUserTestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserTestResult
        fields = ['id', 'start_time', 'passed_date', 'correct_answers_count', 'incorrect_answers_count', 'percentage']
