from rest_framework import serializers

from post.models import Post, PostLike, PostComment, CommentLike
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'photo']


class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    post_likes_count = serializers.SerializerMethodField('get_post_likes_count')
    post_comments_count = serializers.SerializerMethodField('get_post_comments_count')
    me_liked = serializers.SerializerMethodField('get_me_liked')

    class Meta:
        model = Post
        fields = ('id', 'author', 'image', 'caption', 'created_at', 'post_likes_count', 'post_comments_count', 'me_liked')
        extra_kwargs = {
            "image": {'required': False},
        }



    @staticmethod
    def get_post_likes_count(obj):
        return obj.likes.count()

    @staticmethod
    def get_post_comments_count(obj):
        return obj.comments.count()


    def get_me_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            try:
                PostLike.objects.get(author=request.user, post=obj)
                return True
            except PostLike.DoesNotExist:
                return False


class CommentSerializer(serializers.ModelSerializer):


    class Meta:
        model = PostComment
        fields = ('id', 'author', 'created_at', 'comment', 'parent', 'post')
        read_only_fields = ('author', 'created_at', 'id')

    def get_replies(self, obj):
        if obj.children.exists():
            serializer = CommentSerializer(obj.children.all(), many=True, context=self.context)
            return serializer.data
        else:
            return None

    def get_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated():
            return obj.comments.filter(author=user).exists()
        else:
            return False


    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()



class CommentLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ('id', 'author', 'comment')
        read_only_fields = ('author', 'comment')


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ('id', 'author', 'post')
        read_only_fields = ('author', 'post')

