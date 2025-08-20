from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Transaction, Category, SavingsGoal, Budget, UserProfile
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TransactionForm, SavingsGoalForm, BudgetForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum 
from django.db import models
from datetime import datetime
from django.contrib import messages
from django.utils import timezone


def register (request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget:login')
    else:
        form = UserCreationForm()
    return render(request, 'budget/register.html', {'form' : form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('budget:dashboard')
    else: 
        form = AuthenticationForm()
    return render(request, 'budget/login.html', {'form' : form})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('budget:dashboard')
    else:
        form = TransactionForm()
    return render(request, 'budget/add_transaction.html', {'form' : form})

@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('budget:dashboard')
    else:
        form = TransactionForm(instance=transaction)
        context = {
            'form' : form, 
            'transaction' : transaction,
        }
    return render(request, 'budget/edit_transaction.html', context)

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('budget:dashboard')
    return render(request, 'budget/delete_transaction.html', {'transaction' : transaction})

@login_required
def dashboard(request):
    UserProfile.objects.get_or_create(user=request.user)

    now = datetime.now()
    current_month = now.month
    current_year = now.year
    all_budgets = Budget.objects.filter(user=request.user)
    budgets = Budget.objects.filter(
        user=request.user,
        month__year=current_year,
        month__month=current_month
    )
    transactions = Transaction.objects.filter(
        user=request.user,
        date__month=current_month
    ).order_by('-date')
    total_spent = transactions.aggregate(Sum('spend'))['spend__sum'] or 0

    total_budget = budgets.aggregate(Sum('amount'))['amount__sum'] or 0 

    savings_goals = SavingsGoal.objects.filter(user=request.user)

    category_totals = transactions.values('category__name')\
        .annotate(total=Sum('spend'))\
        .order_by('-total')

    context = {
        'transactions' : transactions,
        'category_totals': category_totals,
        'budgets' : budgets,
        'total_spent' : total_spent,
        'savings_goals' : savings_goals,
        'category_totals' : category_totals,
        'total_budget' : total_budget,
        'remaining_budget' : total_budget - total_spent,
        'current_month' : timezone.now().strftime('%B %Y'),
        'debug_current_month' : current_month,
        'debug_current_year' : current_year,
        'debug_all_budgets_count' : all_budgets.count(),

    }
    context.update({
        'profile':request.user.userprofile
    })

    return render(request, 'budget/dashboard.html', context)

def welcome(request):
    if request.user.is_authenticated:
        return redirect('budget:dashboard')
    return render(request, 'budget/welcome.html')

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request,'Budget set successfully')
            return redirect('budget:dashboard')
    else:
        form = BudgetForm()
    return render(request, 'budget/add-budget.html', {'form': form})

@login_required
def add_savings_goal(request):
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Savings goal created successfully')
            return redirect('budget:dashboard')
    else:
        form = SavingsGoalForm()
    return render(request, 'budget/add_savings_goal.html', {'form' : form})

@login_required
def edit_savings_goal(request, goal_id):
    goal = get_object_or_404(SavingsGoal, id=goal_id, user=request.user)
    if goal.is_completed:
        messages.info(request, 'This goal has been completed')
        return redirect('budget:dashboard')

    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('budget:dashboard')
    else:
        form = SavingsGoalForm(instance=goal)
    return render(request, 'budget/edit_savings_goal.html', {'form' : form})

@login_required
def edit_profile(request):
    profile = request.user.userprofile 
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('budget:dashboard')
    else: 
        form = UserProfileForm(instance=profile)
    return render(request, 'budget/edit_profile.html', {'form': form})

@login_required
def spending_analysis(request):
    current_month = timezone.now().month
    transactions = Transaction.objects.filter(
        user=request.user,
        date__month=current_month
    )

    total_spent= transactions.aggregate(Sum('spend'))['spend__sum'] or 0 
    if total_spent > 0:
        category_analysis= transactions.values('category__name')\
            .annotate(
                total_spent=Sum('spend'), 
                percentage=100* Sum('spend') / total_spent
            ).order_by('-total_spent')
    else:
        category_analysis = []
    
    context = {
        'category_analysis' : category_analysis,
        'total_spent' : total_spent,
        'current_month' : datetime.now().strftime('%B %Y')
    }

    return render(request, 'budget/spending_analysis.html', context)
