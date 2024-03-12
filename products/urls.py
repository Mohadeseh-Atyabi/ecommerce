from django.urls import path
from . import views
from .apis import product, payment, order

urlpatterns = [
    path('createproduct/', views.CreateProduct.as_view(), name='create_product'),
    path('productseller/', views.ProductSeller.as_view(), name='product_seller'),
    path('editproduct/<int:pk>/', views.EditProduct.as_view(), name='edit_product'),
    path('deleteproduct/<int:pk>/', views.DeleteProduct.as_view(), name='delete_product'),
    path('productcustomer/', views.ProductCustomer.as_view(), name='product_customer'),
    path('buyproduct/<int:pk>/', views.Buy.as_view(), name='buy_product'),
    path('pay/', views.PayPayment.as_view(), name='pay_payment'),
    path('editorder/<int:pk>/', views.EditOrder.as_view(), name='edit_order'),
    path('deleteorder/<int:pk>/', views.DeleteOrder.as_view(), name='delete_order'),
    path('showpayments/', views.ShowPayments.as_view(), name='show_payments'),
    path('viewproduct/<int:pk>/', views.ViewProduct.as_view(), name='view_product'),
    path('completepayment/', views.CompletePayment.as_view(), name='complete_payment'),
    path('productapi/', product.ProductApi.as_view(), name='product_api'),
    path('productapi/account/', product.ProductAccountApi.as_view(), name='product_account_api'),
    path('productapi/account/<int:pk>/', product.RetrieveUpdateDeleteProductApi.as_view(),
         name='retrieve_update_delete_product_account_api'),
    path('buyapi/account/', order.BuyAPI.as_view(), name='buy_product_api'),
    path('paymentapi/account/', payment.PaymentAPI.as_view(), name='payment_api'),
    path('paypaymentapi/account/', payment.PayPaymentAPI.as_view(), name='pay_payment_api'),
    path('orderapi/account/<int:pk>/', order.OrderAPI.as_view(), name='order_api'),
    path('completepaymentapi/account/', payment.CompletePaymentAPI.as_view(), name='complete_payment_api')
]
