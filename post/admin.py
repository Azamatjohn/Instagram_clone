from django.contrib import admin

from post.models import Post, PostComment, PostLike, CommentLike


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'caption', 'created_at')
    search_fields = ('id', 'author__username', 'caption')


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'id')
    search_fields = ('id', 'author__username', 'comment')


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'id')
    search_fields = ('id', 'author__username', 'like')


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'author', 'created_at', 'id')
    search_fields = ('id', 'author__username', 'comment')


admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)

