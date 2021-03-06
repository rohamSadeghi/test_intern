"""test_intern URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

from rest_framework_swagger.views import get_swagger_view

from products.views import home, product_detail_view, CustomLogoutView

schema_view = get_swagger_view(title='Shop APIs')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('products/', include('products.urls')),
    path('api/docs/', schema_view),
    path('api/comments/', include('commenting.api.urls')),
    path('api/accounts/', include('accounts.api.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
