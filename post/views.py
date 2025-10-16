from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, PostLike, PostComment, CommentLike
from .serializers import PostSerializer, PostLikeSerializer, CommentSerializer, CommentLikeSerializer
from shared.custom_pagination import CustomPagination


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny,]
    queryset = Post.objects.all()
    pagination_class = CustomPagination



class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    queryset = Post.objects.all()


    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response({
            "success": True,
            "message": "Post deleted successfully"
        })



class PostCommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post__id=post_id)
        return queryset



class PostCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)





class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    queryset = PostComment.objects.all()
    pagination_class = CustomPagination


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny,]
    queryset = PostComment.objects.all()




class CommentLikeListAPIView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        queryset = CommentLike.objects.filter(comment__id=comment_id)
        return queryset








class PostLikeListAPIView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [AllowAny,]
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return PostLike.objects.filter(post__id=post_id)

class PostLikeCreateAPIView(generics.CreateAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated,]


    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)

class PostLikeDeleteAPIView(generics.DestroyAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return PostLike.objects.filter(author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class CommentLikeToggleAPIView(APIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, pk):
        user = request.user

        try:
            comment = PostComment.objects.get(id=pk)
        except PostComment.DoesNotExist:
            return Response({'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        like = CommentLike.objects.filter(author=user, comment=comment).first()
        if like:
            like.delete()
            return Response({"Like removed successfully"}, status=status.HTTP_200_OK)
        else:
            like = CommentLike.objects.create(author=user, comment=comment)
            serializer = CommentLikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

