from django.shortcuts import render, redirect


def index(request):
    if request.user.is_active:
        return redirect("home")
    return render(request, 'start/index.html')
