from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import CustomUser, Appointment


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")


class AppointmentForm(forms.ModelForm):
    """Форма записи на услугу"""

    class Meta:
        model = Appointment
        fields = ("master", "date", "time", "comment")
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Пожелания (необязательно)"}),
        }
        labels = {
            "master": "Мастер",
            "date": "Дата",
            "time": "Время",
            "comment": "Комментарий",
        }

    def __init__(self, *args, service=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service
        if service is not None:
            self.fields["master"].queryset = service.masters.all()
            self.fields["master"].required = False
            self.fields["master"].empty_label = "Любой мастер"

    def clean_date(self):
        """Запрет прошедших дат"""
        date = self.cleaned_data.get("date")
        if date and date < timezone.localdate():
            raise forms.ValidationError("Нельзя записаться на прошедшую дату.")
        return date

    def clean(self):
        """Проверка, что мастер свободен в это время"""
        cleaned_data = super().clean()
        master = cleaned_data.get("master")
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if master and date and time:
            conflict = Appointment.objects.filter(
                master=master,
                date=date,
                time=time,
            ).exclude(status="cancelled")

            if self.instance.pk:
                conflict = conflict.exclude(pk=self.instance.pk)

            if conflict.exists():
                raise forms.ValidationError(
                    "Этот мастер уже занят в выбранное время. "
                    "Выберите другое время или другого мастера."
                )

        return cleaned_data