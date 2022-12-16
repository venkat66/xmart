from django.shortcuts import redirect, render
from django.contrib import messages

from customerapp.models import CustomerRegisterModel, FeedbackModel, OrdersModels
from sellerapp.models import ProductsModel, SellerRegisterModel

# Create your views here.
def admin_login(request):
    fed1 = FeedbackModel.objects.all().order_by('-feedback_id')[0]
    fed2 = FeedbackModel.objects.all().order_by('-feedback_id')[1]
    fed3 = FeedbackModel.objects.all().order_by('-feedback_id')[2]
    fed4 = FeedbackModel.objects.all().order_by('-feedback_id')[3]
    if request.method=='POST':
        name=request.POST.get('admin_username')
        pwd=request.POST.get('admin_password')
        if name=='admin' and pwd=='admin':
            request.session["admin"]=name
            messages.success(request,"login successfull")
            return redirect('admin_dashboard')
        else:
            messages.error(request,'Something Wrong, Please try again.')
            return redirect('admin_login')
    return render(request, 'main/admin-login.html',{
        'fed1':fed1,
        'fed2':fed2,
        'fed3':fed3,
        'fed4':fed4
    })


def admin_logout(request):
    request.session["admin"]=None
    return redirect('index')


def admin_dashboard(request):
    if request.session["admin"]==None:
        return redirect('admin_login')
    registered_customers=CustomerRegisterModel.objects.all().count()
    registered_sellers=SellerRegisterModel.objects.filter(seller_status="Authorized").count()
    products_total=ProductsModel.objects.all().count()
    orders_total=OrdersModels.objects.all().count()
    return render(request, 'admin/admin-dashboard.html',{
        'registered_customers':registered_customers,
        'registered_sellers':registered_sellers,
        'products_total':products_total,
        'orders_total':orders_total
    })


def admin_feedbacks(request):
    if request.session["admin"]==None:
        return redirect('admin_login')
    feedbacks=FeedbackModel.objects.all()
    return render(request, 'admin/admin-feedbacks.html',{
        'feedbacks':feedbacks
    })


def admin_pending_sellers(request):
    if request.session["admin"]==None:
        return redirect('admin_login')
    sellers=SellerRegisterModel.objects.filter(seller_status='Pending')
    return render(request, 'admin/admin-pending-sellers.html',{
        'sellers':sellers
    })


def admin_manage_sellers(request):
    if request.session["admin"]==None:
        return redirect('admin_login')
    sellers=SellerRegisterModel.objects.exclude(seller_status='Pending').exclude(seller_status='Rejected')
    return render(request, 'admin/admin-manage-sellers.html',{
        'sellers':sellers
    })


def admin_view_customers(request):
    if request.session["admin"]==None:
        return redirect('admin_login')
    customers=CustomerRegisterModel.objects.all()
    return render(request, 'admin/admin-view-customers.html',{
        'customers':customers
    })
    

def admin_seller_accept(request,status,id):
    seller=SellerRegisterModel.objects.get(seller_id=id)
    if status == 'Accept':
        seller.seller_status = 'Authorized'
        seller.save(update_fields=['seller_status'])
    else:
        seller.seller_status = 'Rejected'
        seller.save(update_fields=['seller_status'])
    return redirect('admin_manage_sellers')


def admin_seller_status(request,id):
    seller=SellerRegisterModel.objects.get(seller_id=id)
    if seller.seller_status == 'Unauthorized':
        seller.seller_status = 'Authorized'
        seller.save(update_fields=['seller_status'])
    else:
        seller.seller_status = 'Unauthorized'
        seller.save(update_fields=['seller_status'])
    return redirect('admin_manage_sellers')
