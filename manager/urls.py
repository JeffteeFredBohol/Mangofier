from django.urls import path
from .views import SaleListView, SaleCreateView
from .views import SalesSummaryView
from .views import confirm_sale_view
from .views import home_redirect_view
from .views import (
    StockListView,
    StockCreateView,
    StockUpdateView,
    StockDeleteView,
)

urlpatterns = [
    path('', home_redirect_view, name='home'),
    path('stock/', StockListView.as_view(), name='stock_list'),
    path('add/', StockCreateView.as_view(), name='stock_add'),
    path('edit/<int:pk>/', StockUpdateView.as_view(), name='stock_edit'),
    path('delete/<int:pk>/', StockDeleteView.as_view(), name='stock_delete'),
    path('sales/', SaleListView.as_view(), name='sale_list'),
    path('sales/add/', SaleCreateView.as_view(), name='sale_add'),
    path('sales/summary/', SalesSummaryView.as_view(), name='sales_summary'),
    path('sales/confirm/', confirm_sale_view, name='sale_confirm'),
]