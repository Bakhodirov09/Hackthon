from django.db.models import TextChoices

class RolesChoices(TextChoices):
    user = "user", "Пользователь"
    staff = "staff", "Персонал"
    manager = "manager", "Менеджер"
    admin = "admin", "Администратор"
    ceo = "ceo", "Генеральный директор (CEO)"