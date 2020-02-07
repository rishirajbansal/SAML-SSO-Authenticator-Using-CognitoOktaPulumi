import logging
from functools import update_wrapper

from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from application.authenticate.forms.auth.login import AuthLoginForm
from application.authenticate.integration.cognito.facade.userManagement import CognitoUserMgmt
from application.generic.base.exception.exceptionUtility import ExceptionUtility
from application.generic.base.constants.genericConstants import *
from application.generic.base.constants.exceptionConstants import *
from application.generic.base.exception.genericExceptions import *
from application.generic.base.exception.businessExceptions import *
from django.urls import NoReverseMatch, reverse

from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


class CognitoAdmin(admin.AdminSite):
    logger = logging.getLogger(__name__)

    site_title = _('Nauge Admin')
    site_header = _('Nauge Administration')
    index_title = _('NaugeLogin')

    login_form = AuthLoginForm

    def admin_view(self, view, cacheable=False):

        # [BEGIN] SAML Customization
        def inner(request, *args, **kwargs):
            session = request.session

            if 'SAML_REDIRECTION' not in session:

                if not self.has_permission(request):
                    if request.path == reverse('admin:logout', current_app=self.name):
                        index_path = reverse('admin:index', current_app=self.name)
                        return HttpResponseRedirect(index_path)
                    # Inner import to prevent django.contrib.admin (app) from
                    # importing django.contrib.auth.models.User (unrelated model).
                    from django.contrib.auth.views import redirect_to_login
                    return redirect_to_login(
                        request.get_full_path(),
                        reverse('admin:login', current_app=self.name)
                    )
            if 'SAML_REDIRECTION' in session and session['SAML_REDIRECTION'] is True and \
                request.session['SAML_USER'] is not None:
                user = User.objects.get(username=request.session['SAML_USER'])
                request.user = user

            return view(request, *args, **kwargs)

            # [END] SAML Customization

        if not cacheable:
            inner = never_cache(inner)
        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)

    def password_change(self, request, extra_context=None):
        self.logger.debug("In Password change done")

        # Update password on Cognito User Pool
        if request.method == 'POST':
            try:
                cognitoUserMgmt = CognitoUserMgmt()

                new_password = request.POST['new_password1']
                old_password = request.POST['old_password']

                cognitoUserMgmt.cog_change_pwd(request.user.username, old_password, new_password)

            except CognitoUserMgmtException as cogEx:
                self.logger.error("CognitoUserMgmtException occurred in while changing password of user from Admin : "
                                  "{}". format(cogEx.message))
                raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
                                                           ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
                                                           cogEx.message,
                                                           BusinessException.__name__)

        # Handle Default Django Request processing
        from django.contrib.admin.forms import AdminPasswordChangeForm
        from django.contrib.auth.views import PasswordChangeView
        url = reverse('admin:password_change_done', current_app=self.name)
        defaults = {
            'form_class': AdminPasswordChangeForm,
            'success_url': url,
            'extra_context': {**self.each_context(request), **(extra_context or {})},
        }
        if self.password_change_template is not None:
            defaults['template_name'] = self.password_change_template
        request.current_app = self.name

        return PasswordChangeView.as_view(**defaults)(request)


adminsite = CognitoAdmin(name='nauge-cognito_admin')


from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

adminsite.register(Group, GroupAdmin)
# adminsite.register(User, UserAdmin)


class CognitoAdminUser(UserAdmin):

    logger = logging.getLogger(__name__)

    def save_model(self, request, obj, form, change):
        obj.user = request.user

        # Create User in Cognito
        try:
            cognitoUserMgmt = CognitoUserMgmt()

            if not change:
                self.logger.debug("New User Creation request: {}".format(obj.username))
                # username acts nauge5@test.com as a email
                cognitoUserMgmt.cog_create_user(obj.username, obj.username, form.data['password1'])
            else:
                self.logger.debug("Update User request: {}".format(obj.username))

                if 'username' in form.changed_data :
                    # Retrieve old details
                    old_details = User.objects.get(pk=obj.id)

                    # if 'username' in form.changed_data:
                    #     self.logger.debug("username is changed, need to delete and create new user in Cognito")
                    #
                    #     # username acts as a email
                    #     cognitoUserMgmt.cog_update_user(old_details.username, obj.username, old_details.username,
                    #                                     obj.password)

        except CognitoUserMgmtException as cogEx:
            self.logger.error("CognitoUserMgmtException occurred in while saving user in Admin Model : {}".
                              format(cogEx.message))
            raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
                                                           ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
                                                           cogEx.message,
                                                           CognitoUserMgmtException.__name__)

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):

        try:
            cognitoUserMgmt = CognitoUserMgmt()

            cognitoUserMgmt.cog_delete_user(obj.username)

        except CognitoUserMgmtException as cogEx:
            self.logger.error("CognitoUserMgmtException occurred in while deleting user from Admin Model : {}".
                              format(cogEx.message))
            self.logger.debug("This is not an error as as a user does not exist in Cognito so can't be deleted")
            # Commenting the raise exception code, to avoid throwing errors for the users which are
            # already created and do not exist in Cognito
            # raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
            #                                            ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
            #                                            cogEx.message,
            #                                            CognitoUserMgmtException.__name__)

        super().delete_model(request, obj)


adminsite.register(User, CognitoAdminUser)

