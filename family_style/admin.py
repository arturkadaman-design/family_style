from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Master, Service, Appointment
from django.utils.html import format_html

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "experience_years", "is_active")
    list_filter = ("is_active",)
    search_fields = ("first_name", "last_name")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "duration_minutes", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("masters",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "master", "date", "time", "colored_status", "created_at")
    list_filter = ("status", "date", "master")
    search_fields = ("user__username", "service__name", "master__last_name")
    date_hierarchy = "date"
    ordering = ("-date", "-time")
    actions = ["mark_confirmed", "mark_done", "mark_cancelled", "mark_new"]

    @admin.action(description="✅ Подтвердить выбранные записи")
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status="confirmed")
        self.message_user(request, f"Подтверждено записей: {updated}")

    @admin.action(description="✔️ Отметить как выполненные")
    def mark_done(self, request, queryset):
        updated = queryset.update(status="done")
        self.message_user(request, f"Отмечено выполненными: {updated}")

    @admin.action(description="❌ Отменить выбранные записи")
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status="cancelled")
        self.message_user(request, f"Отменено записей: {updated}")

    @admin.action(description="🆕 Вернуть в статус «Новая»")
    def mark_new(self, request, queryset):
        updated = queryset.update(status="new")
        self.message_user(request, f"Вернуто в «Новую»: {updated}")

    @admin.display(description="Статус")
    def colored_status(self, obj):
        colors = {
            "new": "#e67e22",       # оранжевый
            "confirmed": "#27ae60", # зелёный
            "done": "#2980b9",      # синий
            "cancelled": "#c0392b", # красный
        }
        color = colors.get(obj.status, "#333")
        return format_html(
            '<span style="color:{}; font-weight:600;">{}</span>',
            color,
            obj.get_status_display(),
        )