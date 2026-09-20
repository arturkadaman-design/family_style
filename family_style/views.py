from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, AppointmentForm
from .models import Category, Service, Master, Appointment


def home(request):
    """Главная страница — показывает несколько услуг и категорий"""
    services = Service.objects.filter(is_active=True)[:6]
    categories = Category.objects.all()
    return render(request, "home.html", {
        "services": services,
        "categories": categories,
    })


def logout_now(request):
    """Страница после выхода"""
    return render(request, "logout.html")


def register(request):
    """Регистрация нового пользователя"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def service_list(request):
    """Список всех услуг"""
    services = Service.objects.filter(is_active=True)
    categories = Category.objects.all()
    return render(request, "service_list.html", {
        "services": services,
        "categories": categories,
    })


def category_detail(request, slug):
    """Услуги одной категории"""
    category = get_object_or_404(Category, slug=slug)
    services = category.services.filter(is_active=True)
    categories = Category.objects.all()
    return render(request, "service_list.html", {
        "category": category,
        "services": services,
        "categories": categories,
    })


def service_detail(request, slug):
    """Одна услуга — подробно"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, "service_detail.html", {
        "service": service,
    })

@login_required
def appointment_create(request, slug):
    """Запись на услугу"""
    service = get_object_or_404(Service, slug=slug, is_active=True)

    if request.method == "POST":
        form = AppointmentForm(request.POST, service=service)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.service = service
            appointment.save()
            return redirect("my_appointments")
    else:
        form = AppointmentForm(service=service)

    return render(request, "appointment_form.html", {
        "form": form,
        "service": service,
    })


@login_required
def my_appointments(request):
    """Мои записи"""
    appointments = request.user.appointments.all().order_by("-date", "-time")
    return render(request, "my_appointments.html", {
        "appointments": appointments,
    })

@login_required
def appointment_cancel(request, pk):
    """Отмена своей записи клиентом"""
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)

    if appointment.status in ("done", "cancelled"):
        # Нельзя отменить выполненную или уже отменённую
        return redirect("my_appointments")

    if request.method == "POST":
        appointment.status = "cancelled"
        appointment.save()
        return redirect("my_appointments")

    # Если GET — покажем страницу подтверждения
    return render(request, "appointment_cancel.html", {
        "appointment": appointment,
    })

def master_list(request):
    """Список всех мастеров"""
    masters = Master.objects.filter(is_active=True)
    return render(request, "master_list.html", {
        "masters": masters,
    })


def master_detail(request, pk):
    """Один мастер и его услуги"""
    master = get_object_or_404(Master, pk=pk, is_active=True)
    services = master.services.filter(is_active=True)
    return render(request, "master_detail.html", {
        "master": master,
        "services": services,
    })