"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings
from app import views
from app.views import RecordsView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.IndexView.as_view(), name="index"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("records/", views.RecordsView.as_view(), name="records"),
    path("records/edit/<int:pk>/", views.EditRecordView.as_view(), name="edit_record"),
    path("records/delete/<int:pk>/", views.DeleteRecordView.as_view(), name="delete_record"),
    path('purge/', views.PurgeRecordsView.as_view(), name='purge_records'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = "views.page_not_found"
