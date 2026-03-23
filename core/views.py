from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Sum

import json

from .models import Component, Build, Order, Profile

# ✅ IMPORT YOUR LIBRARY (ALL MODULES USED)
from BYP_lib.power import calculate_power
from BYP_lib.compatibility import check_compatibility
from BYP_lib.performance import calculate_performance
from BYP_lib.pricing import calculate_total


# ---------------------------
# HOME
# ---------------------------
def home(request):
    return render(request, "home.html")


# ---------------------------
# CONFIGURATOR PAGE
# ---------------------------
def builder_view(request):

    if request.user.is_staff:
        return redirect("admin_dashboard")

    selected_usecase = request.GET.get("type", "gaming")

    items = Component.objects.filter(use_case=selected_usecase)

    context = {
        "usecase": selected_usecase,
        "components": items
    }

    return render(request, "builder.html", context)


# ---------------------------
# SAVE CONFIGURATION
# ---------------------------
@login_required
def save_configuration(request):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    payload = json.loads(request.body)

    def extract(part):
        return payload.get(part, {}).get("name", "")

    # ---------------------------
    # ✅ USE LIBRARY FOR ALL LOGIC
    # ---------------------------
    try:
        total = calculate_total(payload)
    except:
        total = 0

    try:
        total_power = calculate_power(payload)
    except:
        total_power = 0

    try:
        compatibility_status = check_compatibility(payload)
    except:
        compatibility_status = "unknown"

    try:
        performance_score = calculate_performance(payload)
    except:
        performance_score = 0

    # ---------------------------
    # SAVE BUILD
    # ---------------------------
    Build.objects.create(
        owner=request.user,
        cpu=extract("cpu"),
        gpu=extract("gpu"),
        ram=extract("ram"),
        motherboard=extract("motherboard"),
        storage=extract("storage"),
        psu=extract("psu"),
        case=extract("case"),
        cooling=extract("cooling"),
        total_price=total
    )

    # ---------------------------
    # RETURN RESPONSE
    # ---------------------------
    return JsonResponse({
        "status": "saved",
        "total": total,
        "power": total_power,
        "compatibility": compatibility_status,
        "performance": performance_score
    })


# ---------------------------
# MY BUILDS
# ---------------------------
@login_required
def my_builds(request):

    if request.user.is_staff:
        return redirect("admin_dashboard")

    data = Build.objects.filter(owner=request.user)

    return render(request, "my_builds.html", {"builds": data})


# ---------------------------
# DELETE BUILD
# ---------------------------
@login_required
def remove_build(request, build_id):

    record = get_object_or_404(Build, id=build_id, owner=request.user)
    record.delete()

    return redirect("my_builds")


# ---------------------------
# CHECKOUT
# ---------------------------
@login_required
def checkout_view(request):

    if request.user.is_staff:
        return redirect("admin_dashboard")

    if request.method == "POST":

        order_data = {
            "cpu": request.POST.get("cpu"),
            "gpu": request.POST.get("gpu"),
            "ram": request.POST.get("ram"),
            "motherboard": request.POST.get("motherboard"),
            "storage": request.POST.get("storage"),
            "psu": request.POST.get("psu"),
            "case": request.POST.get("case"),
            "cooling": request.POST.get("cooling"),
        }

        total_price = request.POST.get("total_price", 0)

        Order.objects.create(
            user=request.user,
            **order_data,
            total_price=total_price,
            customer_name=request.POST.get("name"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            phone=request.POST.get("phone"),
            payment_method=request.POST.get("payment_method")
        )

        messages.success(request, "Order placed successfully")

        return render(request, "checkout.html", {"order_success": True})

    return render(request, "checkout.html")


# ---------------------------
# MY ORDERS
# ---------------------------
@login_required
def my_orders(request):

    if request.user.is_staff:
        return redirect("admin_dashboard")

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "my_orders.html", {"orders": orders})


# ---------------------------
# ADMIN DASHBOARD
# ---------------------------
@staff_member_required
def admin_dashboard(request):

    stats = {
        "orders": Order.objects.count(),
        "revenue": Order.objects.aggregate(Sum("total_price"))["total_price__sum"] or 0,
        "profit": Order.objects.aggregate(Sum("profit"))["profit__sum"] or 0,
        "users": User.objects.count(),
    }

    status_counts = {
        "pending": Order.objects.filter(status="pending").count(),
        "processing": Order.objects.filter(status="processing").count(),
        "shipped": Order.objects.filter(status="shipped").count(),
        "delivered": Order.objects.filter(status="delivered").count(),
    }

    recent = Order.objects.order_by("-created_at")[:5]

    context = {**stats, **status_counts, "recent_orders": recent}

    return render(request, "admin_dashboard.html", context)


# ---------------------------
# AUTHENTICATION
# ---------------------------
def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        Profile.objects.create(user=user, phone=phone)

        messages.success(request, "Account created successfully")
        return redirect("home")

    return render(request, "registration/signup.html")


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(request.META.get("HTTP_REFERER", "/"))

        else:
            messages.error(request, "Invalid credentials")

    return render(request, "registration/login.html")


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out")
    return redirect("home")