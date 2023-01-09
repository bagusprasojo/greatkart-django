from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard_designer,name='dashboard_designer'),
    path('dashboard/',views.dashboard_designer,name='dashboard_designer'),
    path('add_product/',views.add_product,name='add_product'),
    path('my_products/',views.my_products,name='my_products'),
    # path('add_cart/<int:product_id>',views.add_cart,name='add_cart'),
    # path('remove_cart/<int:cart_item_id>',views.remove_cart,name='remove_cart'),
    # path('remove_cart_item/<int:cart_item_id>',views.remove_cart_item,name='remove_cart_item'),
    # path('checkout/',views.checkout,name='checkout'),
]
