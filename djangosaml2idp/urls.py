from django.urls import path
from . import views

app_name = 'djangosaml2idp'
urlpatterns = [
    path('sso/post', views.sso_entry, name="saml_login_post"),
    path('sso/redirect', views.sso_entry, name="saml_login_redirect"),
    path('login/process/', views.login_process, name='saml_login_process'),
    path('login/process_multi_factor/', views.process_multi_factor, name='saml_multi_factor'),
    path('metadata/', views.metadata, name='saml2_idp_metadata'),
]
