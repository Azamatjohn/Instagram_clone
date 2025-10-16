from django.urls import path

from post.views import (PostListAPIView, PostCreateAPIView, PostRetrieveUpdateDestroyAPIView, PostCommentListAPIView,
                        PostCommentCreateAPIView, CommentListCreateAPIView, PostLikeListAPIView, CommentRetrieveAPIView,
                        CommentLikeListAPIView, PostLikeCreateAPIView, PostLikeDeleteAPIView, CommentLikeToggleAPIView)

urlpatterns = [
    path('list/', PostListAPIView.as_view()),
    path('create/', PostCreateAPIView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('likes/<uuid:pk>/create/', PostLikeCreateAPIView.as_view()),
    path('likes/<uuid:pk>/delete/', PostLikeDeleteAPIView.as_view()),
    path('<uuid:pk>/comments/', PostCommentListAPIView.as_view()),
    path('<uuid:pk>/comments/create/', PostCommentCreateAPIView.as_view()),
    path('comments/<uuid:pk>/like-toggle/', CommentLikeToggleAPIView.as_view() ),
    path('<uuid:pk>/likes/', PostLikeListAPIView.as_view()),
    path('comments/<uuid:pk>/', CommentRetrieveAPIView.as_view()),
    path('comments/', CommentListCreateAPIView.as_view()),
    path('comments/<uuid:pk>/likes/', CommentRetrieveAPIView.as_view()),
    path('comments/<uuid:pk>/likes/', CommentLikeListAPIView.as_view()),
]