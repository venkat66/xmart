from django.db import models

from customerapp.models import CustomerRegisterModel

# Create your models here.
class SellerRegisterModel(models.Model):
    seller_id=models.AutoField(primary_key=True)
    seller_name=models.CharField(help_text='seller_name',max_length=50)
    seller_email=models.EmailField(help_text='seller_email')
    seller_mobile=models.CharField(help_text='seller_mobile',max_length=15)
    seller_state=models.CharField(help_text='seller_state',max_length=50)
    seller_city=models.CharField(help_text='seller_city',max_length=50)
    seller_password=models.CharField(help_text='seller_password',max_length=50)  
    seller_picture=models.ImageField(upload_to='images/sellers/')
    seller_status=models.CharField(help_text='seller_status',max_length=15,default="Pending")
    seller_dob=models.DateField(help_text='seller_dob',null=True)
    seller_reg=models.DateField(auto_now=True,help_text='seller_registered_date')

    class Meta:
        db_table='seller_details'


class ProductsModel(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_creator=models.ForeignKey(SellerRegisterModel,on_delete=models.CASCADE,related_name="seller_products",null=True)
    product_name=models.CharField(help_text='product_name',max_length=100)
    product_size=models.CharField(help_text='product_size', max_length=10,blank=True)
    product_color=models.CharField(help_text="product_color",max_length=15,null=True)
    product_category=models.CharField(help_text='product_category',max_length=50,null=True)
    product_price=models.IntegerField(help_text='product_price')
    product_picture1=models.ImageField(upload_to='images/products/')
    product_picture2=models.ImageField(upload_to='images/products/')
    product_picture3=models.ImageField(upload_to='images/products/')
    product_watchlist=models.ManyToManyField(CustomerRegisterModel,help_text='watchlist',blank=True,related_name='my_watchlist')
    product_desc=models.CharField(help_text='product_description',max_length=500)

    class Meta:
        db_table='product_details'
