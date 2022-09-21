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
from .models import Product
from .serializers import ProductSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

INVALID_DATA = status.HTTP_400_BAD_REQUEST
CREATED = status.HTTP_201_CREATED
SUCCEEDED_REQUEST = status.HTTP_200_OK


@api_view(['GET'])
def search(request, product_id):
    item_view_url = settings.BASE_URL + '/view/'
    if request.method == "GET":
        _output = get_obj(product_id)
        if _output == 0:
            return Response("Not Found", status=SUCCEEDED_REQUEST)

        context = {
            "name": _output.data['name'],
            "desc": _output.data['description'],
            "price": _output.data['price'],
        }
        return render(request, 'item.html', context)


def get_obj(product_id):
    try:
        output = Product.objects.get(name=int(product_id))
        _output = ProductSerializer(output)
        return _output
    except ObjectDoesNotExist:
        return 0


@api_view(['GET'])
def buy(request, product_id):
    if request.method == "GET":
        _output = get_obj(product_id)
        if _output == 0:
            return Response("Not Found", status=SUCCEEDED_REQUEST)

        print(_output.data['price'])
        pay_data = {
            "price_data": {
                "currency": "usd",
                "unit_amount": _output.data['price'],
                "product_data": {
                    "name": "item" + str(product_id),
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
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"

