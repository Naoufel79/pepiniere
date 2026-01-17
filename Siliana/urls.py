from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/stock/<int:product_id>/', views.add_stock, name='add_stock'),
    path('sales/new/', views.new_sale, name='new_sale'),
    path('sales/report/', views.sales_report, name='sales_report'),
    path('order/', views.public_order, name='public_order'),
    path('order/sent/', views.public_order_success, name='public_order_success'),
    path('product/', views.products_catalog, name='products_catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('orders/export/', views.export_orders, name='export_orders'),
    path('api/products/', views.api_products, name='api_products'),
    path('api/orders/', views.api_orders, name='api_orders'),
    path('api/orders/<int:order_id>/', views.api_order_detail, name='api_order_detail'),
    path('api/sales/', views.api_sales, name='api_sales'),
]
