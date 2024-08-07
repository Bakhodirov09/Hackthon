from django.db import models

from apps.users.models import User
from apps.general.models import BaseModel
from apps.general.choices import CallsChoices
from apps.general.utils.uploaders import call_upload_diretory


# Create your models here.
class Call(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=255, choices=CallsChoices)

    def __str__(self):
        return f"Вызов: {self.title}"

    class Meta:
        verbose_name = "Вызов"
        verbose_name_plural = "Вызови"

class CallFile(BaseModel):
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    file = models.FileField(upload_to=call_upload_diretory)

    def __str__(self):
        return f"Файл: {self.call.title} | {self.file.name}"
    
    class Meta:
        verbose_name = "Файл (Вызов)"
        verbose_name_plural = "Файли (Вызов)"