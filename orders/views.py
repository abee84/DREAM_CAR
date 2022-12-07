from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment ,OrderCar
from cars.models import Car
import datetime
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number = body['orderID'])
    # store transaction details inside payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # move the cart items to order cars table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        # breakpoint()
        ordercar=OrderCar.objects.create(
            order=order,
            payment = payment,
            user= request.user,
            car= item.car,
            color=item.car.color,
            quantity=item.quantity,
            car_price= item.car.price,
            ordered = True,
        )
        ordercar.save()

    #clear cart
    CartItem.objects.filter(user=request.user).delete()

    # send order recieved email to customer
    current_user = request.user
    mail_subject = "Thank you for your order!"
    message = render_to_string('orders/order_received_email.html', {
        'user': current_user,
        'order': order,
    })
    to_email = current_user.email
    send_mail = EmailMessage(mail_subject, message, to=[to_email])
    send_mail.send()

    #send order number and transaction id back to send data method via json response
    # data ={
    #     "order_id": order.order_number,
    #     "payment_id": payment.payment_id,
    # }  

    # return JsonResponse(data)

    return render(request, 'orders/payments.html')


def place_order(request, total=0, quantity=0,):

    current_user = request.user

    #if the cart count is less than or equal to zero then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('cars')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.car.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    # form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # store all the billing information inside order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pincode = form.cleaned_data['pincode']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered = False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)

    else:
        print(form.errors)
        return redirect('checkout')

def order_complete(request):
    order_number= request.GET.get('order_number')
    trans_id = request.GET.get('payment_id')

    try:
        order= Order.objects.get(order_number=order_number)
        order_product= OrderCar.objects.filter(order_id=order.id)
        
        subtotal = 0
        for i in order_product:
            subtotal += i.product_price 

        tax_added=order.tax+subtotal


        context={'order_number':order_number,
                  'order_product':order_product,
                  'trans_id': trans_id,
                  'order': order,
                  'order_products': order_product,
                  'sub_total':subtotal,
                  'tax_added':tax_added}

        return render(request, 'Orders/order_complete.html',context)
    except(Order.DoesNotExist,Payment.DoesNotExist):
        return redirect('store-page')