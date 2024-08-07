from django.db import models
from apps.general.models import BaseModel
from apps.general.utils.uploaders import blog_upload_directory
from apps.users.models import User

# Create your models here.
class Blog(BaseModel):
    image = models.ImageField(
        upload_to=blog_upload_directory, verbose_name="Изображение блога", default="defaults/blog.png")
    title = models.TextField(verbose_name="Тема блога")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Какому пользователю принадлежит")

    def __str__(self):
        return f"Блог: {self.title}"


class BlogLike(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Принадлежность к пользователю")
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, verbose_name="Принадлежность к блогу")
    like_status = models.BooleanField(
        default=False, verbose_name="Ставил лайк или нет")

    def __str__(self):
        return f"Нравиться: {self.user.full_name} -> {self.blog.title}"


class BlogComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name="Пользователь")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,
                             verbose_name="Блог")
    text = models.TextField(verbose_name="Текст")

    def __str__(self):
        return f"Комментарий: {self.user.full_name} - {self.blog.title}"
