from django.urls import path
from .views import CustomUserListCreateView, CustomUserRetrieveUpdateDestroyView, TaskList, TaskDetail, TeamList, TeamDetail

urlpatterns = [
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<pk>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/<pk>/', TaskDetail.as_view(), name='task-detail'),
    path('teams/', TeamList.as_view(), name='team-list'),
    path('teams/<pk>/', TeamDetail.as_view(), name='team-detail'),
]