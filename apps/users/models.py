from django.db import models
from db.utils.hash import check_password, hash_password
from apps.general.models import BaseModel
from apps.general.choices import RolesChoices


class Contact(BaseModel):
    user_id = models.BigIntegerField(null=True, unique=True,
                                     verbose_name="ID пользователя (Telegram)")
    name = models.CharField(max_length=255, null=True,
                            verbose_name="Имя (Telegram)")
    username = models.CharField(max_length=255, null=True, blank=True,
                                verbose_name="Имя пользователя (Telegram)")
    is_blocked_bot = models.BooleanField(default=False,
                                         verbose_name="Блокнул бота")
    is_registered = models.BooleanField(default=False,
                                        verbose_name="Зарегистрирован")

    def __str__(self):
        return f"ТГ: {self.name}"
    
    class Meta:
        verbose_name = 'ТГ Профиль'
        verbose_name_plural = 'ТГ Профили'


class User(BaseModel):
    full_name = models.CharField(max_length=255, null=True, 
                                 verbose_name="Ф.И.О.")
    phone_number = models.CharField(max_length=255, null=True,
                                    verbose_name="Номер телефона")
    contact = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name="Telegram-аккаунт", default=None)
    role = models.CharField(max_length=255, choices=RolesChoices, default=RolesChoices.user,
                            verbose_name="Роль")
    points = models.IntegerField(default=0, verbose_name="Балл")
    password = models.CharField(max_length=255, verbose_name="Пароль")

    def save(self, *args, **kwargs):
        if self.pk is None or not User.objects.filter(pk=self.pk, password=self.password).exists():
            self.password = hash_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"Пользователь: {self.full_name}"
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
