from django.db import models

from user.models import User


class Gift(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название подарка")
    description = models.TextField(blank=True, verbose_name="Описание")
    url = models.URLField(blank=True, verbose_name="Ссылка на подарок")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Примерная цена")
    is_reserved = models.BooleanField(default=False, verbose_name="Зарезервирован")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gifts", verbose_name="Кому подарок")
    reserved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name="reserved_gifts", verbose_name="Зарезервировал")

    def __str__(self):
        return self.name
