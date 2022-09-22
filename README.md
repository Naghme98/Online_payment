# Online_payment
Using Django + Stripe to create an online payment application. I also Dockerized it

The structure of this project is:

![image](https://user-images.githubusercontent.com/45916098/191798228-280be5f5-5011-449c-afa1-ab87742954ad.png)

The project name is "Strip" that created an App named "purchase"

First of All I create 2 models for the database:
- Order
- Product

Order model can be consist of several Products (as items)

To register these two models in "/admin" I had to register them in purchase/admin.py file


```
admin.site.register(Product)
admin.site.register(Order)
```

![image](https://user-images.githubusercontent.com/45916098/191799225-63201c4f-e5e4-43e2-bb89-c9f1c55e9640.png)

After that, I changed Strip/settings.py to make this project use environment variables:

```

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
```
And then I have created ".env" file in the same folder as settings.py and add the variables(I have deleted this file from this repository .. so you need to create it for yourself if you are going to use it.)

![image](https://user-images.githubusercontent.com/45916098/191800321-93a6ba4e-2b3a-4b21-b756-56a89d19d627.png)

In settings.py I should replace all these variables in following style:

```
SECRET_KEY = env('SECRET_KEY')
```


This project consist of several APIs:

1. GET /buy/{id}: When someone sent a get request to "http://localhost:8000/buy/{id}, it will search to see if there is such a product avaiable in our database or not. If it was available it will create a "Stripe session" and redirect user to the payment page
2. GET /item/{id}: It will search for the item and if this product was available, it will create a simple "HTML" file and show information about this product "name", "price", "description". Then if the user click on the "checkout" button, it will send a "GET" request to "/buy/{id}.
3. POST /set_order/: For this one, a POST request will be sent to our server with additional information.
As an example "curl -d "userid=25&orderid=1&item1=3&item2=3&item3=3" -X POST http://localhost:8000/set_order/"
This API is used when we want to be able to select several products and create an Order for the user that will he can come to it and pay for it later.
4. GET /pay_order/{userid}/{orderid}: Its for user to pay for his order. He will be redirected to payment pay with the total cost of his order's items.

I also made a Dockerfile for this project and you can get the docker image from my dockerhup repository:

```
docker pull naghme98/online_payment
```
