import json
from django.shortcuts import get_object_or_404, redirect, render
# from indian_cities.dj_city import cities
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator
from textblob import TextBlob
from mart.GmapsApi import GmapsClient

from mart.RazorpayApi import RazorpayClient
from customerapp.models import CartModel, CustomerAddress, CustomerRegisterModel, FeedbackModel, OrdersModels
from mart.settings import BASE_DIR
from sellerapp.models import ProductsModel

states = settings.STATES_LIST
# Create your views here.
def customer_register(request):
    fed1 = FeedbackModel.objects.all().order_by('-feedback_id')[0]
    fed2 = FeedbackModel.objects.all().order_by('-feedback_id')[1]
    fed3 = FeedbackModel.objects.all().order_by('-feedback_id')[2]
    fed4 = FeedbackModel.objects.all().order_by('-feedback_id')[3]
    if request.method == "POST":
        name=request.POST["customer_name"]
        email=request.POST["customer_email"]
        mobile=request.POST["customer_mobile"]
        password=request.POST["customer_password"]
        state=request.POST["customer_state"]
        city=request.POST["customer_city"]
        dob=request.POST["customer_dob"]
        #replacing '_' with a space
        state2= state.replace('_',' ')
        picture=request.FILES["customer_picture"]
        obj = CustomerRegisterModel(customer_name=name,customer_email=email,customer_mobile=mobile,
                                    customer_state=state2,customer_city=city,customer_password=password,
                                    customer_picture=picture,customer_dob=dob)
        obj.save()
        messages.success(request, "Registration sucessful")
        return redirect('customer_login')


    return render(request, 'customer/customer-register.html', {
        'states':states,
        'fed1':fed1,
        'fed2':fed2,
        'fed3':fed3,
        'fed4':fed4
    })


def customer_login(request):
    fed1 = FeedbackModel.objects.all().order_by('-feedback_id')[0]
    fed2 = FeedbackModel.objects.all().order_by('-feedback_id')[1]
    fed3 = FeedbackModel.objects.all().order_by('-feedback_id')[2]
    fed4 = FeedbackModel.objects.all().order_by('-feedback_id')[3]
    if request.method == "POST":
        email=request.POST["customer_email"]
        password=request.POST["customer_password"]
        # print(email,password)
        try:
            check = CustomerRegisterModel.objects.get(customer_email=email,customer_password=password)
            request.session["customer_id"] = check.customer_id
            # print(request.session["customer_id"])
            messages.success(request, "Login Successful")
            return redirect("customer_index")
        except:
            messages.error(request,"Invalid Credentials Please Try Again")
            return redirect("customer_login")
    return render(request, 'customer/customer-login.html',{
        'fed1':fed1,
        'fed2':fed2,
        'fed3':fed3,
        'fed4':fed4
    })


def customer_logout(request):
    request.session["customer_id"]=None
    messages.success(request, "Logged Out successfully")
    return redirect("index")


def customer_index(request):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()
    return render(request, 'customer/customer-index.html',{
        'items':items,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
    })


def customer_my_account(request):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()
    address_count=CustomerAddress.objects.filter(customer=customer).count()
    address=CustomerAddress.objects.filter(customer=customer)
    if request.method=='POST':
        obj = get_object_or_404(CustomerRegisterModel,customer_id=customer_id)
        customer_name=request.POST['customer_name']
        state=request.POST['customer_state']
        customer_mobile=request.POST['customer_mobile']
        customer_city=request.POST['customer_city']
        customer_password=request.POST['customer_password']
        customer_state= state.replace('_',' ')
        if len(request.FILES) != 0:
            customer_profile = request.FILES['customer_profile']
            obj.customer_name = customer_name
            obj.customer_mobile = customer_mobile
            obj.customer_state = customer_state
            obj.customer_city =customer_city
            obj.customer_password=customer_password
            
            obj.customer_picture = customer_profile
            obj.save(update_fields=['customer_name','customer_mobile','customer_state','customer_city','customer_profile','customer_password'])
            
            obj.save()
        else:
            obj.customer_name = customer_name
            obj.customer_mobile = customer_mobile
            obj.customer_state = customer_state
            obj.customer_city =customer_city
            obj.customer_password=customer_password
            
            obj.save(update_fields=['customer_name','customer_mobile','customer_state','customer_city','customer_password'])
            obj.save()
        messages.success(request,"Profile Updated Successfully")
        return redirect('customer_my_account')
    return render(request, 'customer/customer-my-account.html',{
        'customer':customer,
        'states':states,
        'address_count':address_count,
        'address':address,
        'items':items,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
    })


def customer_cart(request):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()
    items=CartModel.objects.filter(cart_owner=customer)
    total_items=CartModel.objects.filter(cart_owner=customer).count()
    total_qty1=CartModel.objects.filter(cart_owner=customer).aggregate(Sum('cart_product_qty'))
    total_qty=total_qty1["cart_product_qty__sum"]
    total2=CartModel.objects.filter(cart_owner=customer).aggregate(Sum('cart_product_price'))
    total=total2["cart_product_price__sum"]
    # context = {}
    # context['razorpay_order_id'] = razorpay_order_id
    # context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    # context['razorpay_amount'] = amount
    # context['currency'] = currency
    # context['callback_url'] = callback_url
    return render(request, 'customer/customer-cart.html',{
        'items':items,
        'total':total,
        'states':states,
        'total_items':total_items,
        'total_qty':total_qty,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
    })


def customer_checkout(request):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()
    items=CartModel.objects.filter(cart_owner=customer)
    total2=CartModel.objects.filter(cart_owner=customer).aggregate(Sum('cart_product_price'))
    total=total2["cart_product_price__sum"]
    address=CustomerAddress.objects.get(address_id=customer.customer_cart_address)

    amount=total*100 #20Rs(20*100paisa)
    currency='INR'
    api = RazorpayClient()
    # Create a Razorpay Order
    razorpay_order = api.create_order(amount)

    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
    # print(razorpay_order_id)
    return render(request,'customer/customer-checkout.html',{
        'total':total,
        'razorpay_order_id':razorpay_order_id,
        'razorpay_merchant_key':settings.RAZOR_KEY_ID,
        'amount':amount,
        'currency':currency,
        'callback_url':callback_url,
        'states':states,
        'items':items,
        'address':address,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
    })



@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            # print(payment_id,razorpay_order_id,signature,)
            api=RazorpayClient()
            # verify the payment signature.
            result = api.client.utility.verify_payment_signature(
                params_dict)
            # print(result)
            if result:
                customer_id=request.session['customer_id']
                customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
                
                total2=CartModel.objects.filter(cart_owner=customer).aggregate(Sum('cart_product_price'))
                total=total2["cart_product_price__sum"]

                amount=total*100 #(1Rs*100=100paisa)
                # amount=2000
                try:
 
                    # capture the payemt
                    api.client.payment.capture(payment_id, amount)
                    
                    
                    return redirect('make_order', order_id=razorpay_order_id,payment_id=payment_id)
                except:
                    
                    # if there is an error while capturing payment.
                    messages.error(request,'Payment Failed!! Please Try Again')
                    return redirect('customer_cart')
            else:
 
                # if signature verification fails.
                messages.error(request,'Signature verification Failed!! Please Try Again')
                return redirect('customer_cart')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()


def make_order(request,order_id,payment_id):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    address=CustomerAddress.objects.get(address_id=customer.customer_cart_address)
    for i in items:
        order_unique_id=order_id
        order_product=i.cart_product
        order_product_price=i.cart_product.product_price
        order_product_qty=i.cart_product_qty
        order_product_amount=i.cart_product_price
        order_product_seller=i.cart_product.product_creator
        order_payment_status='Succesful'
        order_status='Order confirmed'
        order_payment_id=payment_id
        
        obj=OrdersModels(order_unique_id=order_unique_id,order_product=order_product,
                        order_product_price=order_product_price,order_product_qty=order_product_qty,
                        order_product_amount=order_product_amount,order_product_seller=order_product_seller,
                        order_payment_status=order_payment_status,order_status=order_status,
                        order_customer=customer,order_address=address,order_payment_id=order_payment_id
                        )
        obj.save()
    for i in items:
        i.delete()
    messages.success(request,'Payment Succesful')
    return redirect('customer_orders')


def customer_address_form(request):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()
    if request.method=="POST":
        state1=request.POST.get('state')
        city=request.POST.get('city')
        postcode=request.POST.get('postcode')
        flat_number=request.POST.get('flat_number')
        contact_no=request.POST.get('contact_no')
        address_name=request.POST.get('address_name')
        state= state1.replace('_',' ')
        # print(state,city,postcode,flat_number,contact_no,address_name)
        obj= CustomerAddress(state=state,city=city,zip_code=postcode,flat_no=flat_number,
                                contact_no=contact_no,address_name=address_name,
                                customer=customer)
        obj.save()
        messages.success(request,'Address added succesfully')
        return redirect('customer_my_account')
    return render(request, 'customer/customer-address-form.html',{
        'states':states,
        'items':items,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
    })


def customer_address(request):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    if items_count == 0:
        messages.error(request,'Please add some prouducts to cart')
        return redirect('customer_products',category='all')
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()
    address=CustomerAddress.objects.filter(customer=customer)
    address_count=CustomerAddress.objects.filter(customer=customer).count()
    if request.method=="POST":
        address_id=request.POST.get('address')
        if not address_id:
            messages.error(request,'Please Select delivery address')
            return redirect('customer_address')
        obj=CustomerAddress.objects.get(address_id=address_id)
        obj2=CustomerRegisterModel.objects.get(customer_id=customer_id)
        obj2.customer_cart_address = obj.address_id
        obj2.save()
        return redirect('customer_checkout')
    return render(request, 'customer/customer-address.html',{
        'address':address,
        'address_count':address_count,
        'items':items,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
    })


def customer_edit_address(request,id):
    address=CustomerAddress.objects.get(address_id=id)
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()
    if request.method=="POST":
        state=request.POST.get('state')
        city=request.POST.get('city')
        postcode=request.POST.get('postcode')
        flat_number=request.POST.get('flat_number')
        contact_no=request.POST.get('contact_no')
        address_name=request.POST.get('address_name')
        # print(state,city,postcode,flat_number,contact_no,address_name)
        obj=get_object_or_404(CustomerAddress,address_id=id)
        obj.state=state
        obj.city = city
        obj.zip_code=postcode
        obj.flat_no=flat_number
        obj.contact_no=contact_no
        obj.address_name=address_name
        obj.save()
        messages.success(request,'Address has been updated successfully')
        return redirect('customer_my_account')
    return render(request,'customer/customer-edit-address.html',{
        'address':address,
        'states':states,
        'items':items,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
    })


def customer_orders(request):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()
    orders=OrdersModels.objects.filter(order_customer=customer).order_by('-order_id')
    return render(request,'customer/customer-orders.html',{
        'orders':orders,
        'items':items,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
    })


def customer_order_details(request,id):
    order=OrdersModels.objects.get(order_id=id)
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()
    return render(request,'customer/customer-order-details.html',{
        'order':order,
        'items':items,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
    })


def customer_products(request,category):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()
    if category=='all':
        products=ProductsModel.objects.all().order_by('-product_id')
    else:
        products=ProductsModel.objects.filter(product_category=category).order_by('-product_id')
    paginator = Paginator(products, 8)

    page_number =request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    pages = page_obj.paginator.num_pages

    for i in page_obj:
        if customer in i.product_watchlist.all():
            i.is_watched = True
        else:
            i.is_watched = False
    
    return render(request, 'customer/customer-products.html',{
        'products':page_obj,
        'items':items,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
        'pages':pages,
        'category_name':category
    })


def customer_product_details(request,id):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()
    items=CartModel.objects.filter(cart_owner=customer)
    product=ProductsModel.objects.get(product_id=id)

    seller=product.product_creator
    seller_products=ProductsModel.objects.filter(product_creator=seller).count()
    delivered_products=OrdersModels.objects.filter(order_product_seller=seller,order_status='Delivered').count()
    feedbacks=product.product_feedbacks.all()
    feedbacks_count=product.product_feedbacks.all().count()

    
    order=OrdersModels.objects.filter(order_product=product,order_customer=customer,order_status="Delivered").count()
    print(order)
    if order == 0:
        eligible=False
    else:
        eligible=True

   

    

    return render(request, 'customer/customer-product-details.html',{
        'product':product,
        'items':items,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
        'seller_products':seller_products,
        'delivered_products':delivered_products,
        'feedbacks':feedbacks,
        'feedbacks_count':feedbacks_count,
        'eligible':eligible
    })


def customer_feedbacks_map(request,id):
    #Page Data
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()

    #Map Data
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
        
        
    return render(request,'customer/customer-feedbacks-map.html',{
        'feedback_data':json_data,
        'api_key':settings.GMAPS_API_KEY,
        'items':items,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
    })


def customer_feedbacks_filter(request,id,city):
    #Page Data
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()

    #feedbacks
    product = ProductsModel.objects.get(product_id=id)
    feedbacks = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=city)
    feedbacks_count = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=city).count()
    positive = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=city,feedback_sentiment='Positive').count()
    negative = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=city,feedback_sentiment='Negative').count()
    neutral = FeedbackModel.objects.filter(feedback_product=product,feedback_customer__customer_city__contains=city,feedback_sentiment='Neutral').count()
    posperc= round((positive/feedbacks_count)*100)
    negperc = round((negative/feedbacks_count)*100)
    neuperc = 100 - posperc - negperc
    print(posperc,negperc,neuperc,feedbacks_count)
    

    return render(request, 'customer/customer-feedbacks-filter.html',{
        'feedbacks':feedbacks,
        'city':city,
        'product':product,
        'positive':positive,
        'negative':negative,
        'neutral':neutral,
        'items':items,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
        'posperc':posperc,
        'negperc':negperc,
        'neuperc':neuperc
    })


def customer_wishlist(request):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    items=CartModel.objects.filter(cart_owner=customer)
    items_count=CartModel.objects.filter(cart_owner=customer).count()
    wishlist=ProductsModel.objects.filter(product_watchlist=customer)[0:4]
    watchlist_count=ProductsModel.objects.filter(product_watchlist=customer).count()
    wishlist_all=customer.my_watchlist.all()
    return render(request,'customer/customer-wishlist.html',{
        'wishlist_all':wishlist_all,
        'items':items,
        'wishlist':wishlist,
        'watchlist_count':watchlist_count,
        'items_count':items_count,
    })


def customer_feedback(request,id):
    if request.method=='POST':
        feedback_message=request.POST['review']

        #classifier to decide sentimet of user from text data
        analysis = TextBlob(feedback_message)
        
        sentiment=''
        if analysis.polarity>0.2:
            sentiment='Positive'
        elif analysis.polarity<-0.2: 
            sentiment='Negative'
        else:
            sentiment='Neutral'

        
        customer_id=request.session['customer_id']
        customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
        product=ProductsModel.objects.get(product_id=id)

        print(feedback_message,sentiment)
        obj=FeedbackModel(feedback_message=feedback_message,feedback_sentiment=sentiment,feedback_customer=customer,
                            feedback_product=product,feedback_seller=product.product_creator)
        obj.save()
        messages.success(request,'Review Submitted Successfully')
        return redirect('customer_product_details', id=id)


def add_to_cart(request,id,redirect_page):
    if request.method=="POST":
        customer_id=request.session['customer_id']
        customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
        product=ProductsModel.objects.get(product_id=id)
        product_qty=int(request.POST['product_qty'])
        if product_qty <=0:
            messages.error(request,'Quantity must be at least 1')
            if redirect_page == 'wishlist':
                return redirect('customer_wishlist')
            elif redirect_page == "products":
                return redirect('customer_products',category='all')
            else:
                return redirect('customer_product_details',id=id)
        try:
            item=CartModel.objects.get(cart_product=product,cart_owner=customer)
            item.cart_product_qty = product_qty+item.cart_product_qty
            # print(item.cart_product_price)
            price=item.cart_product_qty*product.product_price
            item.cart_product_price=price
            item.save()
            messages.success(request,'Quantitiy for the Product added to Cart')
            if redirect_page == 'wishlist':
                return redirect('customer_wishlist')
            elif redirect_page == "products":
                return redirect('customer_products',category='all')
            else:
                return redirect('customer_product_details',id=id)
        except:
            pass
        
        product_price=product.product_price
        price=(product_qty)*(product_price)
        # print(price)

        # print(product_qty)
        obj=CartModel(cart_owner=customer,cart_product=product,cart_product_qty=product_qty,
                        cart_product_price=price)
        obj.save()
        messages.success(request,'Product added to cart')
        return redirect('customer_products',category="all")


def update_cart(request,id):
    if request.method=="POST":
        customer_id=request.session['customer_id']
        customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
        product=ProductsModel.objects.get(product_id=id)
        product_qty=int(request.POST['product_qty'])
        if product_qty <=0:
            messages.error(request,'Quantity must be at least 1')
            return redirect('customer_cart')
        try:
            item=CartModel.objects.get(cart_product=product,cart_owner=customer)
            item.cart_product_qty = product_qty
            price=item.cart_product_qty*product.product_price
            item.cart_product_price=price
            item.save()
            messages.success(request,'Quantitiy for the Product updated')
            return redirect('customer_cart')
        except:
            pass
        
    return redirect('customer_cart')


def delete_cart_item(request,id):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    product=ProductsModel.objects.get(product_id=id)
    item=CartModel.objects.filter(cart_product=product,cart_owner=customer)
    for i in item:
        i.delete()
    messages.info(request,'Product Removed from cart')
    return redirect('customer_cart')


def change_watchlist(request, product_id,redirect_method):
    customer_id=request.session['customer_id']
    customer=CustomerRegisterModel.objects.get(customer_id=customer_id)
    product_object = ProductsModel.objects.get(product_id=product_id)
    if customer in product_object.product_watchlist.all():
        product_object.product_watchlist.remove(customer)
        # messages.info(request,'Product removed from watchlist')
    else:
        product_object.product_watchlist.add(customer)
        # messages.success(request,'Product Added to watchlist')
    
    if redirect_method == "customer_details":
        return redirect('customer_product_details', id=product_id)
    elif redirect_method=='customer_wishlist':
        return redirect(redirect_method)
    else:
        return redirect(redirect_method, category='all')