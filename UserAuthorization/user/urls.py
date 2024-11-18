from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Income
    path('incomes/', views.incomes, name='incomes'),
    path('income/add/', views.income_add, name='income_add'),
    path('income/update/<int:id>/', views.income_update, name='income_update'),
    path('income/delete/<int:id>/', views.income_delete, name='income_delete'),

    # Expense
    path('expenses/', views.expenses, name='expenses'),
    path('expense/add/', views.expense_add, name='expense_add'),
    path('expense/update/<int:id>/', views.expense_update, name='expense_update'),
    path('expense/delete/<int:id>/', views.expense_delete, name='expense_delete'),
]
