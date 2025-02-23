from django import forms 
from .models import Transaction, SavingsGoal, Budget, UserProfile

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'spend', 'date']
        widgets = {
            'date' : forms.DateInput(attrs={'type' : 'date'})
        }

class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['name', 'target_amount', 'current_amount', 'target_date']
        widgets = {
            'target_date' : forms.DateInput(attrs={'type' : 'date'})
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']
        widgets = {
            'month' : forms.DateInput(attrs={'type' : 'month'})
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['monthly_income', 'currency']

