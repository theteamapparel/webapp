from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('category-list',views.category_list,name='category-list'),
    path('brand-list',views.brand_list,name='brand-list'),
    path('product-list',views.product_list,name='product-list'),
    path('category-product-list/<int:cat_id>',views.category_product_list,name='category-product-list'),
    path('product_discount/<int:banner_id>',views.product_discount,name='product_discount'),
    path('brand-product-list/<int:brand_id>',views.brand_product_list,name='brand-product-list'),
    path('product/<str:slug>/<int:id>',views.product_detail,name='product_detail'),
    path('productattribute/<int:id>',views.product_attribute_detail,name='product_attribute_detail'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('load-more-data',views.load_more_data,name='load_more_data'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('add-to-cart-attribute',views.add_to_cart_attribute,name='add_to_cart_attribute'),
    path('cart',views.cart_list,name='cart'),    
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    path('checkout',views.checkout,name='checkout'),
    path('create-checkout-session/', views.CreateCheckoutSessionView, name='create-checkout-session'),
    #path('paypal-create-checkout-session/', views.PaypalCreateCheckoutSessionView, name='paypal-create-checkout-session'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-processing/', views.payment_processing, name='payment_processing'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('save-review/<int:pid>',views.save_review, name='save-review'),

    # Contact
    path('contact', views.contact, name='contact'),

    # Privacy Policy
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    
    # Return Policy
    path('return-policy', views.return_policy, name='return_policy'),

    # User Section Start
    path('my-dashboard',views.my_dashboard, name='my_dashboard'),
    path('my-orders',views.my_orders, name='my_orders'),
    path('my-orders-items/<int:id>',views.my_order_items, name='my_order_items'),
    # End

    # Wishlist
    path('add-wishlist',views.add_wishlist, name='add_wishlist'),
    path('delete-wishlist',views.delete_wishlist, name='delete_wishlist'),
    path('my-wishlist',views.my_wishlist, name='my_wishlist'),
    # My Reviews
    path('my-reviews',views.my_reviews, name='my-reviews'),
    path('delete-review',views.delete_review, name='delete-review'),
    # My AddressBook
    path('my-addressbook',views.my_addressbook, name='my-addressbook'),
    path('add-address',views.save_address, name='add-address'),
    path('activate-address',views.activate_address, name='activate-address'),
    path('update-address/<int:id>',views.update_address, name='update-address'),
    path('edit-profile',views.edit_profile, name='edit-profile'),
]