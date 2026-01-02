"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework import permissions
from task_manager.views.categories import CategoryViewSet
from task_manager.views.tasks import (
    task_list,
    task_create,
    task_detail,
    task_status,
    TaskByWeekday,
    TaskListCreateView,
    TaskDetailView,
    MyTaskListView,
)
from task_manager.views.auth import RegisterView, LoginView, LogoutView, RefreshView
from task_manager.views.subtasks import (
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    SubTaskListCreateAPIView,
    SubTaskDetailAPIView
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Library Swagger',
        default_version='v2',
        description='API documentation',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],

)

router = DefaultRouter()
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('api/v2/', include(router.urls)),

    path('admin/', admin.site.urls),

    path('api/v1/tasks/', task_list),
    path('api/v1/tasks/create/', task_create),
    path('api/v1/tasks/<int:task_id>/', task_detail),
    path('api/v1/tasks/status/', task_status),

    path("api/v1/subtasks/", SubTaskListCreateView.as_view()),
    path("api/v1/subtasks/<int:subtask_id>/", SubTaskDetailUpdateDeleteView.as_view()),

    path('api/v2/tasks/weekday/', TaskByWeekday.as_view()),
    path("api/v2/tasks/", TaskListCreateView.as_view()),
    path("api/v2/mytasks/", MyTaskListView.as_view()),
    path("api/v2/tasks/<int:id>/", TaskDetailView.as_view()),
    path('api/v2/subtasks/', SubTaskListCreateAPIView.as_view()),
    path('api/v2/subtasks/<int:pk>/', SubTaskDetailAPIView.as_view()),

    path('api/v2/jwt-auth/', TokenObtainPairView.as_view()),
    path('api/v2/jwt-refresh/', TokenRefreshView.as_view()),

    path("api/v2/auth/register/", RegisterView.as_view()),
    path("api/v2/auth/login/", LoginView.as_view()),
    path("api/v2/auth/refresh/", RefreshView.as_view()),
    path("api/v2/auth/logout/", LogoutView.as_view()),

    path('swagger/', schema_view.with_ui('swagger')),
    path('redoc/', schema_view.with_ui('redoc')),

]
