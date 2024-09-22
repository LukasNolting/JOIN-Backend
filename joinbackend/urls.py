"""
URL configuration for joinbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
import os
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from join.views import ContactsView, LoginView, TaskView, UserCreateView, UserGetView, docs_view




from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserCreateView.as_view(), name='user-register'),
    path('api/users/', UserGetView.as_view(), name='get_users'),
    path('api/tasks/', TaskView.as_view(), name='task-list'),  # Für alle Tasks
    path('api/tasks/<int:id>/', TaskView.as_view(), name='task-detail'),  # Für einen spezifischen Task
    path('api/contacts/', ContactsView.as_view(), name='contact-list'),
    path('api/contacts/<int:id>/', ContactsView.as_view(), name='contact-detail'),
    path('docs/', docs_view)
]

if settings.DEBUG:
    urlpatterns += static('/docs', document_root=settings.BASE_DIR / 'build')