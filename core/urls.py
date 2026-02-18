from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('user/create/', views.create_user, name='create-user'),
    path('users/', views.user_list, name='user-list'),
    path('user/<int:pk>/update/', views.user_update, name='user-update'),
    path('user/<int:pk>/delete/', views.user_delete, name='user-delete'),
    path('api/admin/monthly-stats/', views.get_monthly_stats, name='monthly-stats'),
    path('monthly-report/', views.monthly_report, name='monthly-report'),
    
    # Companies
    path('companies/', views.company_list, name='company-list'),
    path('company/create/', views.company_create, name='company-create'),
    path('company/<int:pk>/update/', views.company_update, name='company-update'),
    path('company/<int:pk>/delete/', views.company_delete, name='company-delete'),
]
