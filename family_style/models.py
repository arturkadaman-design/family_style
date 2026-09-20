from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class CustomUser(AbstractUser):
    pass


class Category(models.Model):
    """Категория услуг: парикмахерские, ногти, косметология и т.д."""
    name = models.CharField(_("Название"), max_length=100)
    slug = models.SlugField(_("Слаг"), unique=True)
    description = models.TextField(_("Описание"), blank=True)

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        return self.name


class Master(models.Model):
    """Мастер / специалист салона"""
    first_name = models.CharField(_("Имя"), max_length=50)
    last_name = models.CharField(_("Фамилия"), max_length=50)
    photo = models.ImageField(_("Фото"), upload_to="masters/", blank=True, null=True)
    description = models.TextField(_("О мастере"), blank=True)
    experience_years = models.PositiveIntegerField(_("Опыт (лет)"), default=0)
    is_active = models.BooleanField(_("Работает"), default=True)

    class Meta:
        verbose_name = _("Мастер")
        verbose_name_plural = _("Мастера")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Service(models.Model):
    """Конкретная услуга салона"""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name=_("Категория"),
    )
    masters = models.ManyToManyField(
        Master,
        related_name="services",
        verbose_name=_("Мастера"),
        blank=True,
    )
    name = models.CharField(_("Название"), max_length=200)
    slug = models.SlugField(_("Слаг"), unique=True)
    description = models.TextField(_("Описание"), blank=True)
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2)
    duration_minutes = models.PositiveIntegerField(_("Длительность (мин)"), default=60)
    image = models.ImageField(_("Картинка"), upload_to="services/", blank=True, null=True)
    is_active = models.BooleanField(_("Активна"), default=True)
    created_at = models.DateTimeField(_("Создана"), auto_now_add=True)

    class Meta:
        verbose_name = _("Услуга")
        verbose_name_plural = _("Услуги")

    def __str__(self):
        return self.name


class Appointment(models.Model):
    """Запись клиента на услугу"""
    STATUS_CHOICES = [
        ("new", _("Новая")),
        ("confirmed", _("Подтверждена")),
        ("done", _("Выполнена")),
        ("cancelled", _("Отменена")),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name=_("Клиент"),
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name=_("Услуга"),
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
        verbose_name=_("Мастер"),
    )
    date = models.DateField(_("Дата"))
    time = models.TimeField(_("Время"))
    status = models.CharField(
        _("Статус"), max_length=20, choices=STATUS_CHOICES, default="new"
    )
    comment = models.TextField(_("Комментарий"), blank=True)
    created_at = models.DateTimeField(_("Создана"), auto_now_add=True)

    class Meta:
        verbose_name = _("Запись")
        verbose_name_plural = _("Записи")
        ordering = ["-date", "-time"]

    def __str__(self):
        return f"{self.user} → {self.service} ({self.date} {self.time})"



