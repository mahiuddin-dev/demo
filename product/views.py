from django.shortcuts import redirect, render
from django.urls import reverse_lazy 
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from product.models import OrderItem, Product, Order
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order_id = self.request.POST.get('order_id')
            product = Product.objects.get(pk=order_id)
            user = self.request.user
            order_item = OrderItem.objects.create(user=user, product=product)
            order_item.save()
            return redirect('product:index')
        else:
            return redirect('account:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context
    

class addView(LoginRequiredMixin,CreateView):
    model  = Product
    fields = ['name', 'price', 'image']
    success_url = reverse_lazy('product:index')


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'


class ProductEdit(LoginRequiredMixin,UpdateView):
    model = Product
    fields = ['name', 'price', 'image']
    
    def get_success_url(self):
        return reverse_lazy('product:detail', kwargs={'pk': self.object.pk})


class CardView(LoginRequiredMixin,TemplateView):
    template_name = 'card.html'
    model = Order

    def product(self, *args, **kwargs):
        products = OrderItem.objects.filter(user=self.request.user).filter(is_order=False)
        total = sum([item.get_total for item in products])
        return total
    

    def post(self, request, *args, **kwargs):
        user = self.request.user
        order = Order.objects.create(customer=user)
        order.save()
        products = OrderItem.objects.filter(user=self.request.user).filter(is_order=False)
        products.update(is_order=True)
        return redirect("product:order", pk=order.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = OrderItem.objects.filter(user=self.request.user).filter(is_order=False)
        return context

# class PlaceOrder(LoginRequiredMixin,TemplateView):
    
class OrderView(LoginRequiredMixin,DetailView):
    template_name = 'order.html'
    model = Order
    context_object_name = 'order'

    
def permission_denied_view(request, exception):
    return render(request, 'permission_denied.html', status=403)