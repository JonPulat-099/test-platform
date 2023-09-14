from html import escape
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin.options import csrf_protect_m, IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from django.db import transaction, router
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.translation import ugettext_lazy as _, gettext
from django import forms
from django.apps import apps
from rest_auth.views import sensitive_post_parameters_m
from rest_framework.exceptions import PermissionDenied
# Register your models here.
from searchableselect.widgets import SearchableSelect

from core import settings
from main.models import BaseUser, UserGroup, Subject, Test, Question, QuestionAnswer, UserTestAnswer, UserTestResult, \
    ConTest
from main.utils import queryset_to_workbook



from import_export.admin import ImportExportModelAdmin
from import_export import resources

from import_export.admin import ImportExportActionModelAdmin

class CustomUserAdmin(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name','last_name','middle_name', 'phone', 'photo', 'is_student','u_group'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    search_fields = ['username', 'first_name','last_name', 'u_group__name']

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
            Use special form during user creation
            """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_urls(self):
        return [
                   path(
                       '<id>/password/',
                       self.admin_site.admin_view(self.user_change_password),
                       name='auth_user_password_change',
                   ),
               ] + super().get_urls()

    def lookup_allowed(self, lookup, value):
        # Don't allow lookups involving passwords.
        return not lookup.startswith('password') and super().lookup_allowed(lookup, value)

    @sensitive_post_parameters_m
    @csrf_protect_m
    def add_view(self, request, form_url='', extra_context=None):
        with transaction.atomic(using=router.db_for_write(self.model)):
            return self._add_view(request, form_url, extra_context)

    def _add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(
                    'Your user does not have the "Change user" permission. In '
                    'order to add users, Django requires that your user '
                    'account have both the "Add user" and "Change user" '
                    'permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': username_field.help_text,
        }
        extra_context.update(defaults)
        return super().add_view(request, form_url, extra_context)

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        user = self.get_object(request, unquote(id))
        if not self.has_change_permission(request, user):
            raise PermissionDenied
        if user is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': self.model._meta.verbose_name,
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = gettext('Password changed successfully.')
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse('%s:%s_%s_change' % (
                        self.admin_site.name,
                        user._meta.app_label,
                        user._meta.model_name,
                    ),
                            args=(user.pk,),
                            )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            **self.admin_site.each_context(request),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context,
        )

    def response_add(self, request, obj, post_url_continue=None):
        """
            Determine the HttpResponse for the add_view stage. It mostly defers to
            its superclass implementation but is customized because the User model
            has a slightly different workflow.
            """
        # We should allow further modification of the user just added i.e. the
        # 'Save' button should behave like the 'Save and continue editing'
        # button except in two scenarios:
        # * The user has pressed the 'Save and add another' button
        # * We are adding a user in a popup
        if '_addanother' not in request.POST and IS_POPUP_VAR not in request.POST:
            request.POST = request.POST.copy()
            request.POST['_continue'] = 1
        return super().response_add(request, obj, post_url_continue)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'language']
    search_fields = ['name']


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'language']


class QuestionAnswerAdmin(admin.TabularInline):
    model = QuestionAnswer


class GroupTestAdmin(admin.TabularInline):
    model = ConTest


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'test', 'question']
    inlines = [QuestionAnswerAdmin]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'status']


class SubjectsModelForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name',)


class CustomConTestModelForm(forms.ModelForm):
    class Meta:
        model = ConTest
        exclude = ['subject', ]
        widgets = {
            # 'test': SearchableSelect(model='main.Test', search_field='subject__name',  many=False ),
        }

    def __init__(self, *args, **kwargs):
        super(CustomConTestModelForm, self).__init__(*args, **kwargs)
        # extra_field = self.cleaned_data.get('subjects', None)
        # subjects = SubjectsModelForm()
        # print(subjects)
        # self.fields['test'].queryset = Subject.objects.filter(status=True)


class ConTestInline(admin.TabularInline):
    model = ConTest


@admin.register(ConTest)
class ConTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'test', 'questions_length', 'start_date', 'end_date', 'status']
    list_filter = ('test',)
    readonly_fields = ('admin_unit_details',)
    form = CustomConTestModelForm

    def questions_length(self, obj):
        questions = obj.test.questions.all()
        return str(len(questions)) + ' ta'

    questions_length.short_description = 'Savollar soni'


class UserTestAnswerAdmin(admin.TabularInline):
    model = UserTestAnswer


class UserTestResultResource(resources.ModelResource):

    class Meta:
        fields = ('id', 'user__first_name','user__last_name', 'user__middle_name', 'contest__name', 'start_time', 'due_time', 'passed_date', 'ip_address', 'percentage','overall_ball')
        export_order = ('id', 'user__first_name','user__last_name', 'user__middle_name', 'contest__name', 'start_time', 'due_time', 'passed_date', 'ip_address', 'percentage','overall_ball')
        model = UserTestResult

@admin.register(UserTestResult)
class UserTestResultAdmin(ImportExportModelAdmin):
    list_display = ['id', 'user', 'test_nomi', 'start_time', 'due_time', 'passed_date', 'submitted', 'ip_address', 'percentage','overall_ball']
    list_filter = ('contest','status','start_time')
    resource_class = UserTestResultResource
    search_fields = ['user__first_name','user__last_name','user__middle_name']

    def test_nomi(self, obj):
        return obj.contest.name


class QuestionAnswerListAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'value']

@admin.register(UserTestAnswer)
class UserTestAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'question', 'answer', 'correct_answer']
    list_filter = ('user', 'question__test',)

admin.site.register(BaseUser, CustomUserAdmin)


# admin.site.register(QuestionAnswer, QuestionAnswerListAdmin)


class ExportAdminView(admin.AdminSite):
    def get_urls(self):
        # urls = super().get_urls()
        urls = [
            path('contest/<int:pk>/', self.admin_view(self.download_results))
        ]
        return urls

    @staticmethod
    def download_results(request, pk=None):
        contest = get_object_or_404(ConTest, id=pk)
        queryset = UserTestResult.objects.filter(contest=contest).order_by('-start_time').distinct()

        columns = {
            'user.username': 'Login',
            'user.first_name': 'Ismi',
            'user.last_name': 'Familiyasi',
            'user.middle_name': 'Sharifi',
            'user.u_group': 'Guruhi',
            'correct_answers_count': 'To‘g‘ri javoblar',
            'incorrect_answers_count': 'Noto‘g‘ri javoblar',
            'percentage': 'Foizda',
        }
        workbook = queryset_to_workbook(queryset, columns)
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename="contest-' + str(pk) + '.xls"'
        workbook.save(response)
        return response


export_admin = ExportAdminView()



models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
