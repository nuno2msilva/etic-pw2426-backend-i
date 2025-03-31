from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from decimal import Decimal

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    name = models.CharField(max_length=20, verbose_name=_("Category Name"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            words = self.name.split()
            capitalized_words = []
            
            for word in words:
                print(f"Category save - word: '{word}', isupper: {word.isupper()}, islower: {word.islower()}")
                
                if not word:
                    continue
                elif word.upper() == word:
                    capitalized_words.append(word)
                    print(f"Preserving uppercase word: {word}")
                elif word[0].islower():
                    capitalized_words.append(word[0].upper() + word[1:])
                    print(f"Capitalizing: {word} -> {word[0].upper() + word[1:]}")
                else:
                    capitalized_words.append(word)
                    print(f"Keeping as is: {word}")
                    
            self.name = ' '.join(capitalized_words)
            print(f"Final category name: {self.name}")
            
        super().save(*args, **kwargs)
    
    def admin_display(self):
        return f"{self.name} @ {self.user.username}"

class Record(models.Model):
    TYPE_CHOICES = [
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name=_("Type"))
    date = models.DateField(verbose_name=_("Date"))
    item = models.CharField(max_length=20, verbose_name=_("Item"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Category"))
    volume = models.CharField(max_length=20, verbose_name=_("Volume"))
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], verbose_name=_("Cost"))

    class Meta:
        verbose_name = _("Record")
        verbose_name_plural = _("Records")
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.item} - {self.cost}"

    def save(self, *args, **kwargs):
        if self.item:
            words = self.item.split()
            capitalized_words = []
            for word in words:
                if not word:
                    continue
                elif word.upper() == word:
                    capitalized_words.append(word)
                elif word[0].islower():
                    capitalized_words.append(word[0].upper() + word[1:])
                else:
                    capitalized_words.append(word)
            self.item = ' '.join(capitalized_words)
        super().save(*args, **kwargs)

@receiver(post_delete, sender=Record)
def delete_unused_categories(sender, instance, **kwargs):
    """Delete categories that are no longer used by any records."""
    if instance.category:
        if not Record.objects.filter(category=instance.category).exists():
            print(f"Deleting unused category: {instance.category.name}")
            instance.category.delete()