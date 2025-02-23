from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'budget'

urlpatterns = [
    path('', views.welcome, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='budget:home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('edit_transaction/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('delete_transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('budget/add/', views.add_budget, name='add_budget'),
    path('savings/add', views.add_savings_goal, name='add_savings_goal'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('savings/edit/<int:goal_id>/', views.edit_savings_goal, name='edit_savings_goal'),
    path('analysis/', views.spending_analysis, name='spending_analysis'),
] 