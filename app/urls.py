from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customers', views.customers, name='customers'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('products/', views.products, name='products'),
    path('user/', views.userPage, name="user-page"),
    path('account/', views.accountSettings, name="account"),
    path('product/<str:pk>/', views.product, name="product"),
    path('add_product/', views.add_product, name="add_product"),
    path('update_product/<str:pk>/', views.update_product, name="update_product"),
    path('delete_product/<str:pk>/', views.delete_product, name="delete_product"),
    path('delete_customer/<str:pk>/', views.delete_customer, name="delete_customer"),
    # search path
    path('search/', views.search_view, name='search'),
    path('search-customer/', views.search_customer, name='search-customer'),
    # path('products_search/', views.products_search, name='products_search'),
    

    path('create_order/<str:pk>/', views.create_order, name='create_order'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),
    path('delete_all_orders/', views.delete_all_orders, name='delete_all_orders'),


    # user-side path
    path('order_details/<str:pk>/', views.order_details, name='order_details'),
    path('cancel_order/<str:pk>/', views.cancel_order, name='cancel_order'),


    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
]