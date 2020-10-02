from django.urls import path


from accounts.api.views import ObtainTokenView, RefreshTokenView, RegisterView, SetPasswordView

urlpatterns = [
    path('token/obtain/', ObtainTokenView.as_view(), name='obtain-token'),
    path('token/refresh/', RefreshTokenView.as_view(), name='refresh-token'),
    path('register/', RegisterView.as_view(), name='register'),
    path('set-password/', SetPasswordView.as_view(), name='set-password'),
]
