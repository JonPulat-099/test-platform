import datetime

from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator, ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from main.manager import UserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(_('Kiritilgan sana'), auto_now_add=True)
    updated_at = models.DateTimeField(_('O\'zgartirilgan sana'), auto_now=True)

    class Meta:
        abstract = True


class UserGroup(BaseModel):
    LANGUAGES = (
        (1, "Rus"),
        (2, "O'zbek")
    )
    name = models.CharField(_('Guruh nomi'), max_length=128)
    language = models.PositiveSmallIntegerField(choices=LANGUAGES, default=1)

    class Meta:
        verbose_name = 'Guruh'
        verbose_name_plural = 'Guruhlar'

    def __str__(self):
        return f"{self.name}"


class BaseUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\d{9}$', message="Up to 13 digits allowed.")
    status = models.BooleanField(_('Aktiv'), default=True),
    phone = models.CharField(_('Telefon raqam'), unique=True, max_length=60, validators=[phone_regex], null=True,
                             blank=True)
    # full_name = models.CharField(max_length=256, null=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    middle_name = models.CharField(_('middle nama'), max_length=150, blank=True)
    photo = models.ImageField(upload_to='profile', null=True, blank=True)
    is_student = models.BooleanField(default=False)
    last_login = models.DateTimeField(_('Oxirgi aktiv holati'), null=True, blank=True)
    created_at = models.DateTimeField(_('Kiritilgan sana'), auto_now_add=True)
    updated_at = models.DateTimeField(_('O\'zgartirilgan sana'), auto_now=True)
    u_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True, blank=True)
    objects = UserManager()

    class Meta:
        verbose_name = 'Tizim Foydalanuvchisi'
        verbose_name_plural = 'Tizim Foydalanuvchilari'
    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}  {self.middle_name}"
    def __str__(self):
        if self.u_group is not None:
            group = ' - ' + self.u_group.name
        else:
            group = ''
        return f"{self.id} - {self.username} - {self.full_name}{group}"


class Subject(BaseModel):
    LANGUAGES = (
        (1, "Rus"),
        (2, "O'zbek")
    )
    name = models.CharField(_('Fan nomi'), max_length=128)
    language = models.PositiveSmallIntegerField(choices=LANGUAGES, default=1)
    status = models.BooleanField(_('Holati'), default=True)

    class Meta:
        verbose_name = 'Fan'
        verbose_name_plural = 'Fanlar'

    def __str__(self):
        return f"{self.name}- {self.get_language_display()}"


class Test(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('Fan'))
    name = models.CharField(max_length=256, verbose_name="Test nomi")
    status = models.BooleanField("Holati", default=False)

    def __str__(self):
        return self.name or f"{self.pk}"

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"


class Question(BaseModel):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Test", related_name='questions')
    question = RichTextUploadingField(verbose_name="Test savoli")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Tartib raqami")

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        ordering = ['test', 'order']
        verbose_name = 'Test savoli'
        verbose_name_plural = 'Test savollari'


class QuestionAnswer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Test Savoli', related_name='answers')
    value = models.TextField("Javob varianti")
    correct_answer = models.BooleanField('To\'g\'ri javob', default=False)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        ordering = ['question', '?']
        verbose_name = 'Test savol varianti'
        verbose_name_plural = 'Test savol variantlari'


class ConTest(BaseModel):
    name = models.CharField(max_length=128, null=True, blank=True)
    group = models.ManyToManyField(UserGroup, verbose_name=_("Belgilangan guruhlar"))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Fan"))
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    grade_per_question = models.FloatField("Bal", default=0)
    start_date = models.DateTimeField("Test boshlanish vaqti", null=True, blank=True)
    end_date = models.DateTimeField("Test tugash vaqti", null=True, blank=True)
    duration = models.PositiveIntegerField(default=60)
    status = models.BooleanField(default=True)

    def admin_unit_details(self):  # Button for admin to get to API
        return format_html(u'<a href="/export/contest/' + str(self.id) + '" class="button" '
                                                                         u'id="id_admin_unit_selected">Natijalarni yuklab olish</a>')

    admin_unit_details.allow_tags = True
    admin_unit_details.short_description = "Natijalar"

    def __str__(self):
        return f'{self.group}-{self.test}' or f"{self.pk}"

    class Meta:
        verbose_name = 'Contest'
        verbose_name_plural = 'Contest'


class UserTestAnswer(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Savol')
    answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE, verbose_name="Foydalanuvchining javobi",
                               null=True)
    correct_answer = models.BooleanField('To\'g\'ri javob', default=False)
    contest = models.ForeignKey(ConTest, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user.username} - #{self.question.id}'

    class Meta:
        verbose_name = 'Test foydalanuvchi javobi'
        verbose_name_plural = 'Test foydalanuvchi javoblari'


class UserTestResult(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    contest = models.ForeignKey(ConTest, on_delete=models.CASCADE, verbose_name="Test", null=True, related_name="contest_result")
    start_time = models.DateTimeField('Boshlangan vaqti', auto_now_add=True)
    due_time = models.DateTimeField('Tugatilishi kerak bo\'lgan vaqt', null=True, blank=True)
    passed_date = models.DateTimeField('Topshirilgan vaqt', null=True)
    correct_answers_count = models.IntegerField('To\'g\'ri', null=True)
    incorrect_answers_count = models.IntegerField('Noto\'g\'ri', null=True)
    percentage = models.PositiveIntegerField('Foiz', null=True)
    point = models.IntegerField('Umumiy ball', null=True)
    submitted = models.BooleanField(verbose_name="Topshirdi", default=False)
    status = models.BooleanField(default=False)
    ip_address = models.CharField("Ip Adres", max_length=50, blank=True, null=True)
    overall_ball = models.FloatField("Umumiy bal", default=0)
    questions = models.ManyToManyField(Question, verbose_name=_("Belgilangan savollar"),
                                       related_name='user_test_results')

    def __str__(self):
        return f'{self.user.username}' or f"{self.id}"

    class Meta:
        unique_together = ['user', 'contest']
        verbose_name = 'Test natijasi'
        verbose_name_plural = 'Test natijalari'


@receiver(post_save, sender=UserTestResult)
def create_order(sender, instance, created, **kwargs):
    if created:
        duration = datetime.datetime.now() + datetime.timedelta(minutes=instance.contest.duration)
        instance.due_time = duration
        instance.start_time = datetime.datetime.now()
        instance.save()
