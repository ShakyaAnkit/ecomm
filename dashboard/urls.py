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

    # Category CRUD
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('category/create/', views.CategoryCreate.as_view(), name='category-create'),
    path("category/<int:pk>/update/", views.CategoryUpdateView.as_view(), name="category-update"),
    path("category/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category-delete"),

    # Coupon CRUD
    path('coupons/', views.CouponListView.as_view(), name='coupon-list'),
    path('coupons/create/', views.CouponCreate.as_view(), name='coupon-create'),
    path("coupons/<int:pk>/update/", views.CouponUpdateView.as_view(), name="coupon-update"),
    path("coupons/<int:pk>/delete/", views.CouponDeleteView.as_view(), name="coupon-delete"),
]