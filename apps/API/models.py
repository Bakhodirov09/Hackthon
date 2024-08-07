from django.db import models
from apps.general.models import BaseModel
from apps.users.models import User


# BLOG API
class Blog(BaseModel):
    image = models.ImageField(
        upload_to="blog_img", verbose_name="Изображение блога", default="default_img/blog.png"
    )
    title = models.TextField(verbose_name="Тема блога")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Какому пользователю принадлежит"
    )

    def __str__(self):
        return self.title


class Like(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Принадлежность к пользователю"
    )
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, verbose_name="Принадлежность к блогу"
    )
    like_status = models.BooleanField(default=False, verbose_name="Ставил лайк или нет")

    def __str__(self):
        return f"Like by {self.user.full_name} on {self.blog.title}"


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.user.full_name} - {self.blog.title}"
