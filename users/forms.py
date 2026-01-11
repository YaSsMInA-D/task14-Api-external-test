from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    template_name = "user_registration_form_snippet.html"