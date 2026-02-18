from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from tasks.models import Task
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .forms import CustomUserCreationForm, CompanyForm, UserUpdateForm
from .models import User, Company
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

@login_required
def dashboard(request):
    user = request.user
    
    context = {
        'total_tasks': 0,
        'pending_tasks': 0,
        'in_progress_tasks': 0,
        'completed_tasks': 0,
        'recent_tasks': [],
    }
    
    if user.is_manager() or user.is_admin():
        # Managers/Admins see all tasks
        tasks = Task.objects.all()
    else:
        # Staff see only their assigned tasks
        tasks = Task.objects.filter(assigned_to=user)
        
    # Calculate stats
    total = tasks.count()
    pending = tasks.filter(status='pending').count()
    in_progress = tasks.filter(status='in_progress').count()
    completed = tasks.filter(status='completed').count()
    
    context['total_tasks'] = total
    context['pending_tasks'] = pending
    context['in_progress_tasks'] = in_progress
    context['completed_tasks'] = completed
    
    # Priority stats for charts
    low = tasks.filter(priority='low').count()
    medium = tasks.filter(priority='medium').count()
    high = tasks.filter(priority='high').count()
    
    # Trend data (last 7 days)
    today = timezone.now().date()
    days = []
    trend_counts = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = tasks.filter(created_at__date=day).count()
        days.append(day.strftime('%b %d'))
        trend_counts.append(count)

    context['chart_data'] = {
        'status_labels': ['Pending', 'In Progress', 'Completed'],
        'status_data': [pending, in_progress, completed],
        'priority_labels': ['Low', 'Medium', 'High'],
        'priority_data': [low, medium, high],
        'trend_labels': days,
        'trend_data': trend_counts,
    }
    
    # Get recent tasks
    context['recent_tasks'] = tasks.order_by('-updated_at')[:5]
    
    
    return render(request, 'dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_admin())
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('user-list')
    else:
        form = CustomUserCreationForm()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'core/user_form_partial.html', {'form': form})
    return render(request, 'core/user_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_admin())
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('user-list')
    else:
        form = UserUpdateForm(instance=user)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'core/user_form_partial.html', {'form': form, 'target_user': user})
    return render(request, 'core/user_form.html', {'form': form, 'target_user': user})

@login_required
@user_passes_test(lambda u: u.is_admin())
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('user-list')
    return render(request, 'core/user_confirm_delete.html', {'target_user': user})

@login_required
@user_passes_test(lambda u: u.is_admin())
def user_list(request):
    users = User.objects.select_related('company').all().order_by('date_joined')
    return render(request, 'core/user_list.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_admin())
def get_monthly_stats(request):
    today = timezone.now().date()
    labels = []
    data = []
    for i in range(5, -1, -1):
        # Last 6 months
        first = today.replace(day=1) - timedelta(days=i*30) # Rough month calculation
        month_name = first.strftime('%b')
        count = Task.objects.filter(created_at__year=first.year, created_at__month=first.month).count()
        labels.append(month_name)
        data.append(count)
    
    return JsonResponse({
        'labels': labels,
        'data': data
    })

@login_required
@user_passes_test(lambda u: u.is_admin())
def monthly_report(request):
    return render(request, 'core/monthly_report.html')

# Company CRUD Views
@login_required
@user_passes_test(lambda u: u.is_admin())
def company_list(request):
    companies = Company.objects.all().order_by('-created_at')
    
    total_companies = companies.count()
    total_active = companies.filter(is_active=True).count()
    total_users = User.objects.exclude(company=None).count()
    
    context = {
        'companies': companies,
        'total_companies': total_companies,
        'total_active': total_active,
        'total_users': total_users,
    }
    return render(request, 'core/company_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_admin())
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company created successfully!')
            return redirect('company-list')
    else:
        form = CompanyForm()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'core/company_form_partial.html', {'form': form})
    return render(request, 'core/company_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_admin())
def company_update(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully!')
            return redirect('company-list')
    else:
        form = CompanyForm(instance=company)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'core/company_form_partial.html', {'form': form, 'company': company})
    return render(request, 'core/company_form.html', {'form': form, 'company': company})

@login_required
@user_passes_test(lambda u: u.is_admin())
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company.delete()
        messages.success(request, 'Company deleted successfully!')
        return redirect('company-list')
    return render(request, 'core/company_confirm_delete.html', {'company': company})
