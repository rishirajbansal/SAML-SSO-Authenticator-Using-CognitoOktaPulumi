from django.urls import include, path
from application.authenticate.admin import adminsite


urlpatterns = [

    path('', adminsite.urls),
    path('admin/', adminsite.urls),
    path('saml/', include('application.authenticate.urls')),

]


