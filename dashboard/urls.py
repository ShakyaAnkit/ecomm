from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [

    # audit-trail
    path('audits', views.AuditTrailListView.as_view(), name='audittrail-list'),

    path('', views.DashboardView.as_view(), name='home'),
    path('accounts/login/', views.LoginPageView.as_view(), name='login'),
    path('accounts/logout/',views.LogoutView.as_view(), name='logout'),

    path('dashboard/sample/list', views.SampleListView.as_view(), name='sample-list'),
    path('dashboard/sample/form', views.SampleFormView.as_view(), name='sample-form')
]