"""mart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainapp import views  as mainapp_views
from customerapp import views as customerapp_views
from sellerapp import views as sellerappp_views
from adminapp import views as adminapp_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp_views.index,name='index'),

    #mainapp
    path('contact', mainapp_views.contact, name='contact'),
    path('about', mainapp_views.about, name='about'),

    #customerapp
    path('customer-register', customerapp_views.customer_register,name='customer_register'),
    path('customer-login', customerapp_views.customer_login,name='customer_login'),
    path('customer-logout',customerapp_views.customer_logout,name="customer_logout"),
    path('customer-index', customerapp_views.customer_index,name='customer_index'),
    path('customer-my-account', customerapp_views.customer_my_account,name='customer_my_account'),
    path('customer-cart', customerapp_views.customer_cart,name='customer_cart'),
    path('customer-products/<str:category>', customerapp_views.customer_products,name='customer_products'),
    path('customer-product-details/<int:id>', customerapp_views.customer_product_details,name='customer_product_details'),
    path('customer-add-to-cart/<int:id>/<str:redirect_page>',customerapp_views.add_to_cart,name='add_to_cart'),
    path('update-cart/<int:id>',customerapp_views.update_cart,name='update_cart'),
    path('delte-cart-item/<int:id>',customerapp_views.delete_cart_item,name='delete_cart_item'),
    path('customer-change-wathclist/<int:product_id>/<str:redirect_method>',customerapp_views.change_watchlist,name='change_watchlist'),
    path('customer-wishlist',customerapp_views.customer_wishlist,name='customer_wishlist'),
    path('customer-orders',customerapp_views.customer_orders,name='customer_orders'),
    path('customer-checkout',customerapp_views.customer_checkout,name='customer_checkout'),
    path('paymenthandler/', customerapp_views.paymenthandler, name='paymenthandler'),
    path('make-order/<str:order_id>/<str:payment_id>',customerapp_views.make_order,name='make_order'),
    path('customer-order-details/<int:id>',customerapp_views.customer_order_details,name='customer_order_details'),
    path('customer-address',customerapp_views.customer_address,name='customer_address'),
    path('customer-address-form',customerapp_views.customer_address_form,name='customer_address_form'),
    path('customer-edit-address/<int:id>',customerapp_views.customer_edit_address,name='customer_edit_address'),
    path('customer-feedback/<int:id>',customerapp_views.customer_feedback,name='customer_feedback'),
    path('customer-feedbacks-map/<int:id>',customerapp_views.customer_feedbacks_map,name='customer_feedbacks_map'),
    path('customer-feedbacks-map/<int:id>/<str:city>',customerapp_views.customer_feedbacks_filter,name='customer_feedbacks_filter'),

    #sellerapp
    path('seller-register', sellerappp_views.seller_register,name='seller_register'),
    path('seller-login', sellerappp_views.seller_login,name='seller_login'),
    path('seller-logout', sellerappp_views.seller_logout,name='seller_logout'),
    path('seller-my-profile',sellerappp_views.seller_my_profile,name='seller_my_profile'),
    path('seller-dashboard', sellerappp_views.seller_dashboard,name='seller_dashboard'),
    path('seller-add-products', sellerappp_views.seller_add_products,name='seller_add_products'),
    path('seller-completed-orders', sellerappp_views.seller_completed_orders,name='seller_completed_orders'),
    path('seller-feedbacks-product', sellerappp_views.seller_feedbacks_product,name='seller_feedbacks_product'),
    path('seller-feedbacks-location',sellerappp_views.seller_feedbacks_location,name='seller_feedbacks_location'),
    path('seller-manage-products', sellerappp_views.seller_manage_products,name='seller_manage_products'),
    path('seller-pending-orders', sellerappp_views.seller_pending_orders,name='seller_pending_orders'),
    path('seller-proudct-details/<int:id>', sellerappp_views.seller_product_details,name='seller_product_details'),
    path('seller-order-details/<int:id>', sellerappp_views.seller_order_details,name='seller_order_details'),
    path('seller-feedbacks-map/<int:id>',sellerappp_views.seller_feedbacks_map,name='seller_feedbacks_map'),
    path('seller-feedbacks-map/<int:id>/<str:city>',sellerappp_views.seller_feedback_location_filter,name='seller_feedbacks_map'),
    path('seller-feedback-product-filter/<int:id>',sellerappp_views.seller_feedback_product_filter,name='seller_feedback_product_filter'),

    #adminapp
    path('admin-login', adminapp_views.admin_login,name='admin_login'),
    path('admin-logout', adminapp_views.admin_logout,name='admin_logout'),
    path('admin-dashboard', adminapp_views.admin_dashboard,name='admin_dashboard'),
    path('admin-feedbacks', adminapp_views.admin_feedbacks,name='admin_feedbacks'),
    path('admin-pending-sellers', adminapp_views.admin_pending_sellers, name='admin_pending_sellers'),
    path('admin-manage-sellers', adminapp_views.admin_manage_sellers,name='admin_manage_sellers'),
    path('admin-view_customers', adminapp_views.admin_view_customers,name='admin_view_customers'),
    path('admin-seller-status/<int:id>', adminapp_views.admin_seller_status,name='admin_seller_status'),
    path('admin-seller-accept/<int:id>/<str:status>',adminapp_views.admin_seller_accept,name='admin_seller_accept')


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
