# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm  # Import your custom form

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use custom form
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('djangoapp:home')
    else:
        form = CustomUserCreationForm()  # Use custom form
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("djangoapp:home")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", { "form": form })

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('djangoapp:home')