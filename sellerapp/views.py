from itertools import product
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.contrib import messages
from customerapp.models import CustomerRegisterModel, FeedbackModel, OrdersModels
from mart.GmapsApi import GmapsClient
import json
from sellerapp.models import ProductsModel, SellerRegisterModel

states = settings.STATES_LIST
# Create your views here.
def seller_register(request):
    fed1 = FeedbackModel.objects.all().order_by('-feedback_id')[0]
    fed2 = FeedbackModel.objects.all().order_by('-feedback_id')[1]
    fed3 = FeedbackModel.objects.all().order_by('-feedback_id')[2]
    fed4 = FeedbackModel.objects.all().order_by('-feedback_id')[3]
    if request.method == "POST":
        name=request.POST["seller_name"]
        email=request.POST["seller_email"]
        try:
            check = SellerRegisterModel.objects.get(seller_email=email)
            messages.error(request,'Email already exists')
            return redirect('seller_register')
        except:
            pass
        mobile=request.POST["seller_mobile"]
        password=request.POST["seller_password"]
        state=request.POST["seller_state"]
        city=request.POST["seller_city"]
        dob=request.POST["seller_dob"]
        #replacing '_' with a space
        state2= state.replace('_',' ')
        picture=request.FILES["seller_picture"]
        obj = SellerRegisterModel(seller_name=name,seller_email=email,seller_mobile=mobile,
                                    seller_state=state2,seller_city=city,seller_password=password,
                                    seller_picture=picture,seller_dob=dob)
        obj.save()
        messages.success(request, "Registration request sent sucessfully")
        return redirect('seller_login')

    return render(request, 'main/seller-register.html',{
        'states':states,
        'fed1':fed1,
        'fed2':fed2,
        'fed3':fed3,
        'fed4':fed4
    })


def seller_login(request):
    fed1 = FeedbackModel.objects.all().order_by('-feedback_id')[0]
    fed2 = FeedbackModel.objects.all().order_by('-feedback_id')[1]
    fed3 = FeedbackModel.objects.all().order_by('-feedback_id')[2]
    fed4 = FeedbackModel.objects.all().order_by('-feedback_id')[3]
    if request.method == 'POST':
        email=request.POST['seller_email']
        password=request.POST['seller_password']
        print(email,password)
        try:
            check = SellerRegisterModel.objects.get(seller_email=email,seller_password=password)
            
            if check.seller_status == 'Authorized':
                request.session['seller_id'] = check.seller_id
                
                messages.success(request,'Login Successful')
                return redirect('seller_dashboard')
            elif check.seller_status == 'Pending':
                
                messages.error(request,'Account is not Approved yet !Login failed')
                return redirect('seller_login')
            elif check.seller_status == 'Rejected':
                messages.error(request,'Your Account has been Rejected You cannot login')
                return redirect('seller_login')
            elif check.seller_status == 'Unauthorized':
                messages.error(request,'Authorization Denied Please contact Admin')
                return redirect('seller_login')
        except:
            
            messages.error(request,'Invalid Credentials or Account Does Not Exist')
            return redirect('seller_login')
    return render(request, 'main/seller-login.html',{
        'fed1':fed1,
        'fed2':fed2,
        'fed3':fed3,
        'fed4':fed4
    })


def seller_logout(request):
    request.session["seller_id"]=None
    return redirect('index')


def seller_my_profile(request):
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    if request.method=='POST':
        obj = get_object_or_404(SellerRegisterModel,seller_id=seller_id)
        seller_name=request.POST['seller_name']
        state=request.POST['seller_state']
        seller_mobile=request.POST['seller_mobile']
        seller_city=request.POST['seller_city']
        seller_password=request.POST['seller_password']
        seller_state= state.replace('_',' ')
        if len(request.FILES) != 0:
            seller_profile = request.FILES['seller_profile']
            obj.seller_name = seller_name
            obj.seller_mobile = seller_mobile
            obj.seller_state = seller_state
            obj.seller_city =seller_city
            obj.seller_password=seller_password
            
            obj.seller_picture = seller_profile
            obj.save(update_fields=['seller_name','seller_mobile','seller_state','seller_city','seller_profile','seller_password'])
            
            obj.save()
        else:
            obj.seller_name = seller_name
            obj.seller_mobile = seller_mobile
            obj.seller_state = seller_state
            obj.seller_city =seller_city
            obj.seller_password=seller_password
            
            obj.save(update_fields=['seller_name','seller_mobile','seller_state','seller_city','seller_password'])
            obj.save()
        messages.success(request,"Profile Updated Successfully")
        return redirect('seller_my_profile')
    return render(request,'seller/seller-my-profile.html',{
        'seller':seller,
        'states':states
    })


def seller_dashboard(request):
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    registered_customers=CustomerRegisterModel.objects.all().count()
    registered_sellers=SellerRegisterModel.objects.filter(seller_status="Authorized").count()
    seller_products=seller.seller_products.all().count()
    seller_ordered_products=seller.seller_ordered_products.all().count()
    return render(request, 'seller/seller-dashboard.html',{
        'seller':seller,
        'registered_customers':registered_customers,
        'registered_sellers':registered_sellers,
        'seller_products':seller_products,
        'seller_ordered_products':seller_ordered_products
    })


def seller_add_products(request):
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    if request.method == "POST":
        name=request.POST["product_name"]
        category=request.POST["product_category"]
        size=request.POST["product_size"]
        color=request.POST["product_color"]
        price1=request.POST["product_price"]
        price=int(price1)
        picture1=request.FILES["picture1"]
        picture2=request.FILES["picture2"]
        picture3=request.FILES["picture3"]
        desc=request.POST["product_desc"]

        #size=request.POST.getlist("product_size")

        print(name,category,size,color,price,picture1,picture2,picture3,desc)
        obj = ProductsModel(product_name=name,product_size=size,product_category=category,
                            product_color=color,product_price=price,product_picture1=picture1,
                            product_picture2=picture2,product_picture3=picture3,
                            product_desc=desc,product_creator=seller)
        obj.save()
        messages.success(request,"Product Added Succesfully")
        return redirect('seller_manage_products')


    return render(request, 'seller/seller-add-products.html',{
        'seller':seller
    })


def seller_pending_orders(request):
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    orders=seller.seller_ordered_products.exclude(order_status='Delivered')
    return render(request, 'seller/seller-pending-orders.html',{
        'seller':seller,
        'orders':orders
    })


def seller_order_details(request,id):
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    order=OrdersModels.objects.get(order_id=id)
    if request.method=="POST":
        status=request.POST.get('order_status')
        obj=OrdersModels.objects.get(order_id=id)
        obj.order_status=status
        print(id)
        print(obj.order_status)
        print(status,'ssssss')
        obj.save()
        print(obj.order_status)
        messages.success(request,'Status Updated Successfully')
        return redirect('seller_pending_orders')
    return render(request,'seller/seller-order-details.html',{
        'seller':seller,
        'order':order
    })



def seller_completed_orders(request):
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    orders=seller.seller_ordered_products.filter(order_status='Delivered')
    return render(request, 'seller/seller-completed-orders.html',{
        'seller':seller,
        'orders':orders
    })


def seller_feedbacks_product(request):
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    feedbacks=seller.seller_feedbacks.all()
    products=seller.seller_products.all()
    for i in products:
        i.orders = i.orderd_products_list.all().count()
        i.feedbacks = i.product_feedbacks.all().count()
    return render(request, 'seller/seller-feedbacks-product.html',{
        'seller':seller,
        'feedbacks':feedbacks,
        'products':products
    })


def seller_feedback_product_filter(request,id):
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    product = ProductsModel.objects.get(product_id=id)
    feedbacks = FeedbackModel.objects.filter(feedback_product=product)
    if len(feedbacks) == 0:
        messages.error(request,"Product does not have any feedbacks")
        return redirect('seller_feedbacks_product')
    return render(request,'seller/seller-feedback-product-filter.html',{
        'seller':seller,
        'feedbacks':feedbacks,
        'product':product
    })


def seller_manage_products(request):
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    products=seller.seller_products.all()
    return render(request, 'seller/seller-manage-products.html',{
        'seller':seller,
        'products':products
    })


def seller_product_details(request,id):
    product=ProductsModel.objects.get(product_id=id)
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    if request.method == "POST":
        obj=get_object_or_404(ProductsModel,product_id=id)
        name=request.POST["product_name"]
        category=request.POST["product_category"]
        size=request.POST["product_size"]
        color=request.POST["product_color"]
        price1=request.POST["product_price"]
        desc=request.POST["product_desc"]
        price=int(price1)
        # picture1=request.FILES["picture1"]
        # picture2=request.FILES["picture2"]
        # picture3=request.FILES["picture3"]
        if request.FILES :
            picture1=request.FILES["picture1"]
            picture2=request.FILES["picture2"]
            picture3=request.FILES["picture3"]
            obj.product_picture1=picture1
            obj.product_picture2=picture2
            obj.product_picture3=picture3
            obj.product_name=name
            obj.product_category=category
            obj.product_size=size
            obj.product_color=color
            obj.product_desc=desc
            obj.product_price=price
            obj.save(update_fields=['product_picture1','product_picture2','product_picture3','product_name','product_category','product_size','product_color','product_desc','product_price'])
        else:
            obj.product_name=name
            obj.product_category=category
            obj.product_size=size
            obj.product_color=color
            obj.product_desc=desc
            obj.product_price=price
            obj.save(update_fields=['product_name','product_category','product_size','product_color','product_desc','product_price'])
            obj.product_name=name
        messages.success(request,'Product details updated successfully')
        return redirect('seller_manage_products')
    return render(request, 'seller/seller-product-details.html',{
        'product':product,
        'seller':seller
    })


def seller_feedbacks_location(request):
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    products=seller.seller_products.all()
    for i in products:
        i.orders = i.orderd_products_list.all().count()
        i.feedbacks = i.product_feedbacks.all().count()
    
    return render(request,'seller/seller-feedbacks-location.html',{
        'seller':seller,
        'products':products
    })


def seller_feedbacks_map(request,id):
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    product=ProductsModel.objects.get(product_id=id)
    feedbacks=product.product_feedbacks.all()
    if len(feedbacks) == 0:
        messages.error(request,"Product does not have any feedbacks")
        return redirect('seller_feedbacks_location')

    #Maps data for javascript
    places=set()
    for i in feedbacks:
        city = i.feedback_customer.customer_city
        places.add(city)
    print(places)
    feedback_data = []
    for i in places:
        coords={}
        
        api = GmapsClient()
        result = api.getcoords(i)
        print(result["lat"])
        coords["lat"] = result["lat"]
        coords["lng"] = result["lng"]
        count = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=i).count()
        coords["count"] = str(count) 
        coords["product_id"] = id
        coords["city"] = i
        coords["positive"] = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=i,feedback_sentiment="Positive").count()
        coords["negative"] = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=i,feedback_sentiment="Negative").count()
        coords["neutral"] = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=i,feedback_sentiment="Neutral").count()
        feedback_data.append(coords)

    print(feedback_data)
    json_data=json.dumps(feedback_data)
        
        
    return render(request,'seller/seller-feedbacks-map.html',{
        'seller':seller,
        'feedback_data':json_data,
        'api_key':settings.GMAPS_API_KEY
    })


def seller_feedback_location_filter(request,id,city):
    seller_id=request.session["seller_id"]
    seller=SellerRegisterModel.objects.get(seller_id=seller_id)
    product = ProductsModel.objects.get(product_id=id)
    feedbacks = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=city)
    positive = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=city,feedback_sentiment='Positive').count()
    negative = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=city,feedback_sentiment='Negative').count()
    neutral = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=city,feedback_sentiment='Neutral').count()
    
    return render(request, 'seller/seller-feedback-location-filter.html',{
        'seller':seller,
        'feedbacks':feedbacks,
        'city':city,
        'product':product,
        'positive':positive,
        'negative':negative,
        'neutral':neutral
    })


