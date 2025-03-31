from django.contrib import admin
from app.models import Record, Category

# Register your models here.
class RecordAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "date", "item", "category", "volume", "cost", "user")
    sortable_by = ("id", "date", "category", "user")
    list_filter = ("type", "user", "category")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user",)
    list_filter = ("user",)
    search_fields = ("name", "user__username")

# Register the models with their custom admin classes
admin.site.register(Record, RecordAdmin)
admin.site.register(Category, CategoryAdmin)