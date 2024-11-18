from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, IncomeForm, ExpenseForm, LoginForm
from .models import Income, Expense
from django.contrib.auth import get_user_model

User = get_user_model()

# Home page
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Debugging: Check if request.user is an instance of the custom User model
    print(isinstance(request.user, User))  # Should print True if it's the custom User model

    income = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user).order_by('-date')[:4]
    return render(request, 'home.html', context={'expenses': expenses, 'income': income})


# Login view
def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {email}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    return render(request, 'login.html', {'form': form})

# Register view
def register_view(request):
    form = RegisterForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Registration successful. Welcome!")
        return redirect('home')
    return render(request, 'register.html', context={'form': form})

# Logout view
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully.")
    return redirect('login')

# Expenses page
@login_required
def expenses(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses.html', context={'expenses': expenses})

# Add expense
@login_required
def expense_add(request):
    form = ExpenseForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        messages.success(request, "Expense added successfully.")
        return redirect('home')
    return render(request, 'expense_add.html', context={'form': form})

# Update expense
@login_required
def expense_update(request, id):
    expense = get_object_or_404(Expense, user=request.user, id=id)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully.")
            return redirect('home')  
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense_update.html', {'form': form})

# Delete expense
@login_required
def expense_delete(request, id):
    expense = get_object_or_404(Expense, user=request.user, id=id)
    expense.delete()
    messages.success(request, "Expense deleted successfully.")
    return redirect('home')

# Incomes page
@login_required
def incomes(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'incomes.html', context={'incomes': incomes})

# Add income
@login_required
def income_add(request):
    form = IncomeForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        income = form.save(commit=False)
        income.user = request.user
        income.save()
        messages.success(request, "Income added successfully.")
        return redirect('home')
    return render(request, 'income_add.html', context={'form': form})

# Update income
@login_required
def income_update(request, id):
    income = get_object_or_404(Income, user=request.user, id=id)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, "Income updated successfully.")
            return redirect('home')  
    else:
        form = IncomeForm(instance=income)
    return render(request, 'income_update.html', {'form': form})

# Delete income
@login_required
def income_delete(request, id):
    income = get_object_or_404(Income, user=request.user, id=id)
    income.delete()
    messages.success(request, "Income deleted successfully.")
    return redirect('home')
