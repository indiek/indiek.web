from django.urls import path
from .views import (
        ItemListView, 
        ItemDetailView,
        ItemCreateView,
        ItemUpdateView,
        ItemDeleteView,
        UserItemListView,
        TopicListView, 
        TopicDetailView,
        TopicCreateView,
        TopicUpdateView,
        TopicDeleteView,
        UserTopicListView
        )
from . import views

urlpatterns = [
        path('', views.home, name='indiek-home'),
        path('user/<str:username>/items/', UserItemListView.as_view(), name='user-items'),
        path('user/<str:username>/topics/', UserTopicListView.as_view(), name='user-topics'),
        path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
        path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
        path('item/new/', ItemCreateView.as_view(), name='item-create'),
        path('topic/new/', TopicCreateView.as_view(), name='topic-create'),
        path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
        path('topic/<int:pk>/update/', TopicUpdateView.as_view(), name='topic-update'),
        path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
        path('topic/<int:pk>/delete/', TopicDeleteView.as_view(), name='topic-delete'),
]
