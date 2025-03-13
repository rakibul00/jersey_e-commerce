from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/<int:jersi_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update-cart/<int:cart_item_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('jersi_dec/<int:jersi_id>/', views.jersi_dec_view, name='jersi_dec'),
    path('store/', views.store, name='store'),
    path('store/category/<int:category_id>/', views.store, name='store_by_category'), 
    path('register/', views.signup, name='register'),
    path('signin/', views.user_login, name='signin'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.search_jersi, name='search'),
    path('dashboard/', views.Profile, name='dashboard'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_complate/', views.order_complete, name='order_complate'),

]