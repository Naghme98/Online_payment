from django.shortcuts import render

# Create your views here.
import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

INVALID_DATA = status.HTTP_400_BAD_REQUEST
CREATED = status.HTTP_201_CREATED
SUCCEEDED_REQUEST = status.HTTP_200_OK


@api_view(['GET'])
def search(request, product_id):
    item_view_url = settings.BASE_URL + '/view/'
    if request.method == "GET":
        output = get_product_obj(product_id)
        _output = ProductSerializer(output)
        if _output == 0:
            return Response("Not Found", status=SUCCEEDED_REQUEST)

        context = {
            "name": _output.data['name'],
            "desc": _output.data['description'],
            "price": _output.data['price'],
        }
        return render(request, 'item.html', context)


def get_product_obj(product_id):
    try:
        output = Product.objects.get(name=int(product_id))
        return output
    except ObjectDoesNotExist:
        return 0


@api_view(['GET'])
def buy(request, product_id):
    if request.method == "GET":
        output = get_product_obj(product_id)
        _output = ProductSerializer(output)
        if _output == 0:
            return Response("Not Found", status=SUCCEEDED_REQUEST)

        checkout_session = create_session(_output.data, "item " + str(_output.data['name']))
        return redirect(checkout_session.url)


def create_session(_output, name):
    pay_data = {
        "price_data": {
            "currency": "usd",
            "unit_amount": _output['price']*100,
            "product_data": {
                "name": name,
            }
        },
        "quantity": 1,
    }
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[

            pay_data
        ],
        mode='payment',
        success_url=settings.BASE_URL + '/success/',
        cancel_url=settings.BASE_URL + '/cancel/',
    )
    return checkout_session


@api_view(['POST'])
def set_order(request):
    if request.method == 'POST':
        order_items = request.data
        total_cost = 0

        order = Order.objects.create(userid=order_items['userid'], orderid=order_items['orderid'])

        for x in order_items:
            if "item" in x:
                item = get_product_obj(order_items[x])
                if item != 0:
                    order.items.add(item)
                    total_cost += item.price

        order.price = total_cost
        order.save()
        return Response("Order Created", status=SUCCEEDED_REQUEST)


def get_order_obj(userid, orderid):
    output = Order.objects.filter(userid=int(userid), orderid=int(orderid))
    if output.count() < 1:
        return 0

    _output = OrderSerializer(output, many=True)
    return _output


@api_view(['GET'])
def buy_order(request, userid, orderid):
    if request.method == "GET":
        _output = get_order_obj(userid, orderid)
        if _output == 0:
            return Response("Not Found", status=SUCCEEDED_REQUEST)
        checkout_session = create_session(_output.data[0], ("order " + str(_output.data[0]['orderid'])))
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
