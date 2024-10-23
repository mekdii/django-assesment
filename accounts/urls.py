# urls.py

from django.urls import path, include
from accounts.views import CustomLoginView, CustomRegisterView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')), #for password reset       
    path('register/', CustomRegisterView.as_view(), name='custom_register'),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('social/', include('allauth.socialaccount.urls')),
]
