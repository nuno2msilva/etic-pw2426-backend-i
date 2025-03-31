from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import logout
from app.models import Record, Category
from app.forms import RecordForm
from django.urls import reverse_lazy, reverse
from django.db.models import Sum, Q
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.

class IndexView(TemplateView):
    http_method_names = ["get"]
    template_name = "index.html"

class RegisterView(FormView):
    template_name = "auth/register.html"
    success_url = reverse_lazy("login")
    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class LoginView(AuthLoginView):
    template_name = "auth/login.html"
    success_url = reverse_lazy("records")

    def get_success_url(self):
        return self.success_url

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("index")

class RecordsView(LoginRequiredMixin, CreateView):
    model = Record
    template_name = "app/records.html"
    form_class = RecordForm
    success_url = reverse_lazy("records")
    login_url = reverse_lazy("login")
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        sort_param = self.request.GET.get('sort', 'id')  # Default to sorting by ID
        
        sort_reverse = sort_param.startswith('-')
        if sort_reverse:
            sort_field = sort_param[1:]
        else:
            sort_field = sort_param
        
        context['sort_by'] = sort_field
        context['sort_reverse'] = sort_reverse
        
        records = Record.objects.filter(user=self.request.user).order_by(sort_param)
        context["object_list"] = records
        
        expenses = records.filter(type="Expense").aggregate(total=Sum("cost"))["total"] or 0
        incomes = records.filter(type="Income").aggregate(total=Sum("cost"))["total"] or 0
        context["total_amount"] = incomes - expenses
        
        category_spending = {}
        for record in records:
            category_name = record.category.name if record.category else "Uncategorized"
            if category_name not in category_spending:
                category_spending[category_name] = 0
                
            if record.type == "Expense":
                category_spending[category_name] -= record.cost
            else:
                category_spending[category_name] += record.cost
        
        sorted_category_spending = dict(sorted(category_spending.items()))
        context["category_spending"] = sorted_category_spending
        
        return context

    def form_valid(self, form):
        """Handle form submission for record creation."""
        new_category_name = self.request.POST.get('new_category')
        
        if new_category_name:
            words = new_category_name.split()
            capitalized_words = []
            
            for word in words:
                if not word:
                    continue
                elif word.isupper():
                    capitalized_words.append(word)
                    print(f"Keeping uppercase word: {word}")
                elif word[0].islower():
                    capitalized_words.append(word[0].upper() + word[1:])
                else:
                    capitalized_words.append(word)
                    
            new_category_name = ' '.join(capitalized_words)
            print(f"Final category name: {new_category_name}")
            
            category, created = Category.objects.get_or_create(
                user=self.request.user,
                name=new_category_name
            )
            
            form.instance.category = category
        
        form.instance.user = self.request.user
        
        return super().form_valid(form)

class EditRecordView(LoginRequiredMixin, UpdateView):
    model = Record
    form_class = RecordForm
    template_name = 'app/edit.html'
    success_url = reverse_lazy('records')
    login_url = reverse_lazy('login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        """Only allow users to edit their own records."""
        return Record.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """Handle form submission for record editing."""
        current_record = Record.objects.get(id=self.object.id)
        
        old_category_id = current_record.category_id
        print(f"Edit view - old category ID: {old_category_id}")
        
        new_category_id = form.cleaned_data.get('category').id if form.cleaned_data.get('category') else None
        print(f"Edit view - form category ID: {new_category_id}")
        
        new_category_name = self.request.POST.get('new_category')
        if new_category_name:
            words = new_category_name.split()
            capitalized_words = []
            
            for word in words:
                if not word:
                    continue
                elif word.isupper():
                    capitalized_words.append(word)
                elif word[0].islower():
                    capitalized_words.append(word[0].upper() + word[1:])
                else:
                    capitalized_words.append(word)
                    
            new_category_name = ' '.join(capitalized_words)
            
            category, created = Category.objects.get_or_create(
                user=self.request.user,
                name=new_category_name
            )
            
            form.instance.category = category
            new_category_id = category.id  # Update new_category_id
        
        response = super().form_valid(form)
        
        if old_category_id and old_category_id != new_category_id:
            remaining = Record.objects.filter(category_id=old_category_id).count()
            print(f"Edit view - records using old category {old_category_id}: {remaining}")
            
            if remaining == 0:
                print(f"Edit view - deleting orphaned category {old_category_id}")
                Category.objects.filter(id=old_category_id).delete()
        
        return response

class DeleteRecordView(LoginRequiredMixin, DeleteView):
    model = Record
    template_name = "app/delete.html"
    success_url = reverse_lazy("records")
    login_url = reverse_lazy("login")

    def get_queryset(self):
        """Only allow users to delete their own records."""
        return Record.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        record = self.get_object()
        category_id = None
        user_id = None
        
        if record.category:
            category_id = record.category.id
            user_id = record.user.id
            print(f"Will check category {category_id} after deletion")
        
        response = super().delete(request, *args, **kwargs)
        
        if category_id and user_id:
            remaining_count = Record.objects.filter(category_id=category_id).count()
            print(f"Found {remaining_count} records still using category {category_id}")
            
            if remaining_count == 0:
                print(f"Deleting category {category_id}")
                Category.objects.filter(id=category_id).delete()
                print(f"Category {category_id} deleted")
        
        return response

class PurgeRecordsView(LoginRequiredMixin, View):
    """View to purge all records for the current user."""
    template_name = "app/purge.html"
    login_url = reverse_lazy("login")
    
    def get(self, request):
        """Handle GET requests: display the purge confirmation page."""
        record_count = Record.objects.filter(user=request.user).count()
        return render(request, self.template_name, {'record_count': record_count})
    
    def post(self, request):
        """Handle POST requests: delete all records."""
        user_category_ids = Category.objects.filter(user=request.user).values_list('id', flat=True)
        records = Record.objects.filter(user=request.user)
        count = records.count()
        records.delete()
        deleted_cats = Category.objects.filter(user=request.user).delete()[0]
        messages.success(request, f"Successfully deleted all {count} records and {deleted_cats} categories.")
        return redirect('records')