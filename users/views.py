from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm ## ==  form used for user login 
                                   ### Django's pre-built registration form
                                                     ####Automatically has: username, password, password confirmation fields
from django.contrib.auth import login, logout

def register_view(request):
    if request.method == 'POST': ###checks if the user submitted the form
        form = UserCreationForm(request.POST)   ### request.POST = All the data the user typed (username, password)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('djangoapp:home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:        ### shecks if there is a safe url to redirect 
                return redirect(request.POST.get('next')) ##  URL that tells the login page where to redirect the user after successful login.
            else:
                return redirect("djangoapp:home")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", { "form": form })

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('djangoapp:home')