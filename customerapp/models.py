from django.db import models

# from sellerapp.models import ProductsModel, SellerRegisterModel

# Create your models here.
class CustomerRegisterModel(models.Model):
    customer_id=models.AutoField(primary_key=True)
    customer_name=models.CharField(help_text='customer_name',max_length=50)
    customer_email=models.EmailField(help_text='customer_email')
    customer_mobile=models.CharField(help_text='customer_mobile',max_length=15)
    customer_state=models.CharField(help_text='customer_state',max_length=50)
    customer_city=models.CharField(help_text='customer_city',max_length=50)
    customer_password=models.CharField(help_text='customer_password',max_length=50)  
    customer_picture=models.ImageField(upload_to='images/customers/')
    customer_dob=models.DateField(help_text='customer_dob',null=True)
    customer_reg=models.DateField(auto_now=True,help_text='customer_registered_date')
    customer_cart_address=models.IntegerField(help_text='address_id',default=0)

    class Meta:
        db_table='customer_details'


class CustomerAddress(models.Model):
    address_id=models.AutoField(primary_key=True)
    state=models.CharField(max_length=200,help_text='customer_address')
    city=models.CharField(max_length=20,null=True)
    zip_code=models.CharField(max_length=10,null=True)
    flat_no=models.CharField(max_length=100,null=True)
    contact_no=models.CharField(max_length=15,null=True)
    landmark=models.CharField(max_length=50,null=True)
    address_name=models.CharField(max_length=20,null=True)
    customer=models.ForeignKey(CustomerRegisterModel,on_delete=models.CASCADE,related_name='customer_address_list')

    class Meta:
        db_table='customer_address'


from sellerapp.models import ProductsModel, SellerRegisterModel

class CartModel(models.Model):
    cart_id=models.AutoField(primary_key=True)
    cart_owner=models.ForeignKey(CustomerRegisterModel,on_delete=models.CASCADE,related_name="cart_creator")
    cart_product=models.ForeignKey(ProductsModel,on_delete=models.CASCADE,related_name="user_cart_items",null=True)
    cart_product_qty=models.IntegerField(help_text='product_quantity')
    cart_product_price=models.IntegerField(help_text='Prodcuts_price')

    class Meta:
        db_table='cart_details'


class OrdersModels(models.Model):
    order_id=models.AutoField(primary_key=True)
    order_unique_id=models.CharField(max_length=100,help_text='order_id_from_razorpay',null=True)
    order_payment_id=models.CharField(max_length=100,help_text='Payment_id_from_razorpay',null=True)
    order_customer=models.ForeignKey(CustomerRegisterModel,on_delete=models.CASCADE,related_name='user_orders')
    order_product=models.ForeignKey(ProductsModel,on_delete=models.CASCADE,null=True,related_name='orderd_products_list')
    order_product_price=models.IntegerField(help_text='order_price',null=True)
    order_product_qty=models.IntegerField(help_text='order_product_qty',null=True)
    order_product_amount=models.IntegerField(help_text='order_product_amount',null=True)
    order_product_seller=models.ForeignKey(SellerRegisterModel,on_delete=models.CASCADE,related_name='seller_ordered_products',null=True)
    order_date=models.DateTimeField(auto_now=True,help_text='order_date')
    order_payment_status=models.CharField(max_length=20,help_text='payment_status',default='Pending')
    order_status=models.CharField(max_length=100,default='Pending',help_text='order_status')
    order_address=models.ForeignKey(CustomerAddress,on_delete=models.CASCADE,related_name='order_address',null=True)

    class Meta:
        db_table='order_details'


class FeedbackModel(models.Model):
    feedback_id=models.AutoField(primary_key=True)
    feedback_message=models.CharField(max_length=200,help_text='feedback_message')
    feedback_sentiment=models.CharField(max_length=20,help_text='sentiment_analysis',null=True)
    feedback_customer=models.ForeignKey(CustomerRegisterModel,on_delete=models.CASCADE,related_name='customer_all_feedbacks')
    feedback_product=models.ForeignKey(ProductsModel,on_delete=models.CASCADE,related_name='product_feedbacks')
    feedback_seller=models.ForeignKey(SellerRegisterModel,on_delete=models.CASCADE,related_name='seller_feedbacks')
    feedback_date=models.DateField(auto_now_add=True)

    class Meta:
        db_table='feedback_details'
