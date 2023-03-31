from django.urls import path
from . import views


app_name = 'product'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('add/', views.addView.as_view(), name='add'),
    path('detail/<int:pk>/', views.ProductDetail.as_view(), name='detail'),
    path('update/<int:pk>/', views.ProductEdit.as_view(), name='update'),
    path('card/', views.CardView.as_view(), name='card'),
    path('order/<int:pk>', views.OrderView.as_view(), name='order'),
]

handler403 = views.permission_denied_view