from django.shortcuts import render
from django.views.generic import ListView, TemplateView, FormView, CreateView
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView,CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

# Create your views here.

class IndexView(TemplateView):
    http_method_names = ["get"]
    login_url = "/login"
    template_name="index.html"

def page_not_found(request, exception):
    return render(request, "page_not_found.html", status=404)

class RegisterView(FormView):
    template_name = "auth/register.html"
    success_url="/"
    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")