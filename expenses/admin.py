from django.contrib import admin
from .models import Expense, Category

class expenseAdmin(admin.ModelAdmin):
    list_display = ['category', 'description', 'owner', 'amount','date']
    search_fields = ['category', 'description', 'amount']
    list_per_page =3
    list_filter = ['category', 'date']

    

# Register your models here.
admin.site.register(Expense, expenseAdmin)
admin.site.register(Category)