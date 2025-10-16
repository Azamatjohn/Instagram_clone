from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db import models

from shared.models import BaseModel

User = get_user_model()

class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic'])])
    caption = models.TextField(null=True, blank=True, validators=[MaxLengthValidator(2000)])


    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'{self.author} - {self.caption}'



class PostComment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return f'{self.author} - {self.comment}'

    class Meta:
        db_table = 'post_comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'



class PostLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'post'],
                name='unique_like_post'
            )
        ]


class CommentLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='comment_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_likes', null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'comment'],
                name='unique_comment_like'
            )
        ]
