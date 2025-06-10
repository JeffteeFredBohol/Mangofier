from django.urls import path
from .views import login_view, dashboard_view, logout_view, record_sale, profit_report
from .views import stock_view, edit_product, delete_product, add_product, delete_all_sales


urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('stock/', stock_view, name='stock'),
    path('stock/add/', add_product, name='add_product'),
    path('stock/edit/<int:pk>/', edit_product, name='edit_product'),
    path('stock/delete/<int:pk>/', delete_product, name='delete_product'),
    path('sales/', record_sale, name='record_sale'),
    path('profits/', profit_report, name='profit_report'),
    path('profits/delete_all/', delete_all_sales, name='delete_all_sales'),
]
