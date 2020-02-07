import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, get_user_model, admin
from django.urls import reverse
from django.contrib.auth import authenticate


class SAMLRedirectView(View):

    logger = logging.getLogger(__name__)

    def get(self, request, *args, **kwargs):
        self.logger.debug("Processing the SAMLRedirectView...")

        if 'code' in request.GET:

            authorization_code = request.GET['code']

            try:
                user_cache = authenticate(request, authorization_code=authorization_code)

                if user_cache is not None:
                    self.logger.debug("Authorization Code is valid and user will be authenticated.")
                    username = user_cache.username

                    user = User.objects.get(username=username)
                    user.backend = 'django.contrib.auth.backends.ModelBackend'

                    login(request, user)

                    request.session['SAML_REDIRECTION'] = True
                    request.session['SAML_USER'] = username

                    index_path = reverse('admin:index')
                    return redirect(index_path)
                else:
                    self.logger.debug("Authorization Code Failed to authenticate, will be redirected to login screen.")
                    index_path = reverse('admin:login')
                    return redirect(index_path)
            except Exception as ex:
                self.logger.error("Exception occurred in SAML Custom Backend while "
                                  "authenticating user : {}".format(ex.message))
                # raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
                #                                                ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
                #                                                str(ex),
                #                                                BusinessException.__name__)
                index_path = reverse('admin:login')
                return redirect(index_path)
        else:
            if 'error' in request.GET:
                self.logger.error("Cognito Redirection error : ======================")
                self.logger.error("Error Received from AWS Cognito redirection [ERROR] : {}".format(request.GET['error']))
                self.logger.error(
                    "Error Received from AWS Cognito redirection [ERROR Details] : {}".format(request.GET['error_description']))

                index_path = reverse('admin:login')
                return redirect(index_path)

    def post(self, request, *args, **kwargs):
        self.logger.debug("In post(), going to forward to get()")
        self.get(request, *args, **kwargs)
