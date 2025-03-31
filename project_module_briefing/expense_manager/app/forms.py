from django import forms
from app.models import Record, Category
from django.core.validators import MinValueValidator
from decimal import Decimal

class RecordForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        empty_label="No Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    new_category = forms.CharField(
        max_length=20,
        required=False,
        label="Add New Category",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New Category'})
    )
    type = forms.ChoiceField(
        choices=[('Expense', 'Expense'), ('Income', 'Income')],
        initial='Expense',
        widget=forms.RadioSelect(attrs={'style': 'display: inline-block; margin-right: 10px;'}),
        label="Type"  # Add a label for clarity
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date"  # Add a label for clarity
    )
    item = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Description'}),
        label="Item"
    )
    volume = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
        label="Volume"
    )
    cost = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost'}),
        label="Cost"
    )

    class Meta:
        model = Record
        fields = ['type', 'date', 'item', 'volume', 'cost', 'category']
        widgets = {
            'type': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields["category"].queryset = Category.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')
        if 'item' in cleaned_data and cleaned_data['item']:
            words = cleaned_data['item'].split()
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
            cleaned_data['item'] = ' '.join(capitalized_words)

        if new_category:
            words = new_category.split()
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
            cleaned_data['new_category'] = ' '.join(capitalized_words)
        
        return cleaned_data

    def save(self, commit=True):
        record = super().save(commit=False)
        
        if not hasattr(record, 'user') and self.user:
            record.user = self.user
        
        if commit:
            record.save()
        return record