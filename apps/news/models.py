from django.db import models

from apps.general.models import BaseModel
from apps.general.utils.uploaders import news_upload_diretory


# Create your models here.
class News(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to=news_upload_diretory)

    def __str__(self):
        return f"Новости: {self.title}"
    
    class Meta:
        verbose_name = "Новост"
        verbose_name_plural = "Новости"
