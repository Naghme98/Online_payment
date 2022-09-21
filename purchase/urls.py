from django.urls import path, include
from django.conf.urls import url

from . import views


urlpatterns = [
    path('item/<int:product_id>/', views.search),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('buy/<int:product_id>/', views.buy, name='buy'),

]