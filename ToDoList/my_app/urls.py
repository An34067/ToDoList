from django.urls import path

from .views import *

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/undone/', UndoneTaskListView.as_view(), name='task-undone'),
    path('tasks/by-tag/<int:tag_id>/', TasksByTagView.as_view(), name='task-by-tag'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagDetailView.as_view(), name='tag-detail'),
]