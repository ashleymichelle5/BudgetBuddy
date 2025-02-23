from django.contrib import admin
from .models import Category, Transaction, SavingsGoal, Budget, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) 
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'spend', 'date')
    list_filter = ('category', 'date',)
    search_fields = ('user__username', 'category__name')#__ busque el username en el modelo de user 

@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'target_amount', 'current_amount', 'target_date')
    list_filter = ('target_date',)
    search_fields = ('name', 'user__username')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'month')
    list_filter = ('category', 'month',)
    search_fields = ('user__username', 'category__name')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'monthly_income', 'currency')
    search_fields = ('user__username',)



