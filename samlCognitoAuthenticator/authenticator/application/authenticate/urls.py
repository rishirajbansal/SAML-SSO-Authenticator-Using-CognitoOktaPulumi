from django.conf.urls import url
from django.urls import path
from . import views


# adminsite.site = adminsite
# adminsite.autodiscover()

from application.authenticate.views import SAMLRedirectView

app_name = 'application.authenticate'

urlpatterns = [

    path('sso/', SAMLRedirectView.as_view(), name='saml'),

]
