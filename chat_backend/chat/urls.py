from django.urls import path
from . import views

urlpatterns = [
    path('chatrooms/', views.ChatRoomView.as_view(), name='chatroom-list-create'),
    path('chatrooms/<int:pk>/', views.ChatRoomDetailView.as_view(), name='chatroom-detail'),
    path('messages/', views.MessageView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message-detail'),
    path('reactions/', views.ReactionView.as_view(), name='reaction-list-create'),
    path('reactions/<int:pk>/', views.ReactionDetailView.as_view(), name='reaction-detail'),
    path('replies/', views.ReplyView.as_view(), name='reply-list-create'),
    path('replies/<int:pk>/', views.ReplyDetailView.as_view(), name='reply-detail'),
]