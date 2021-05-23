from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [

    # audit-trail
    path('audits', views.AuditTrailListView.as_view(), name='audittrail-list'),

    path('', views.DashboardView.as_view(), name='home'),
    path('accounts/login/', views.LoginPageView.as_view(), name='login'),
    path('accounts/logout/',views.LogoutView.as_view(), name='logout'),

     # Brand CRUD
    path("brands/", views.BrandListView.as_view(), name="brands-list"),
    path("brand/create/", views.BrandCreateView.as_view(), name="brands-create"),
    path("brand/<int:pk>/update/", views.BrandUpdateView.as_view(), name="brands-update"),
    path("brand/<int:pk>/delete/", views.BrandDeleteView.as_view(), name="brands-delete"),


    path('dashboard/sample/list', views.SampleListView.as_view(), name='sample-list'),
    path('dashboard/sample/form', views.SampleFormView.as_view(), name='sample-form')
]