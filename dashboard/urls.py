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

    path('sample/list', views.SampleListView.as_view(), name='sample-list'),
    path('sample/form', views.SampleFormView.as_view(), name='sample-form'),

    # Category CRUD
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('category/create/', views.CategoryCreate.as_view(), name='category-create'),
    path("category/<int:pk>/update/", views.CategoryUpdateView.as_view(), name="category-update"),
    path("category/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category-delete"),

    # Coupon CRUD
    path('coupons/', views.CouponListView.as_view(), name='coupons-list'),
    path('coupons/create/', views.CouponCreate.as_view(), name='coupons-create'),
    path("coupons/<int:pk>/update/", views.CouponUpdateView.as_view(), name="coupons-update"),
    path("coupons/<int:pk>/delete/", views.CouponDeleteView.as_view(), name="coupons-delete"),

    # Size CRUD
    path('sizes/', views.SizeListView.as_view(), name='sizes-list'),
    path('sizes/create/', views.SizeCreateView.as_view(), name='sizes-create'),
    path('sizes/<int:pk>/update/', views.SizeUpdateView.as_view(), name='sizes-update'),
    path('sizes/<int:pk>/delete/', views.SizeDeleteView.as_view(), name='sizes-delete'),
    
    # Product CRUD
    path('product/', views.ProductListView.as_view(), name='products-list'),
    path('product/create/', views.ProductCreateView.as_view(), name='products-create'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='products-update'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='products-delete'),

    # Account CRUD
    path('accounts/', views.AccountListView.as_view(), name='accounts-list'),
]