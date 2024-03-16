from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from .create_product import CreateProductForm
from django.contrib.auth.decorators import login_required
from .models import Product
from .services import (search_list, create_product, edit_product, delete_product, buy_product,
                       get_product, get_order, edit_order, delete_order, get_payment, complete_payment,
                       get_payment_orders)
from .buy_product import BuyProductFrom


class CreateProduct(View):
    post_template = 'product_seller'
    get_template = 'create_product.html'

    @method_decorator(login_required)
    def post(self, req):
        form = CreateProductForm(req.POST)
        if form.is_valid():
            create_product(name=form.cleaned_data.get('name'), price=form.cleaned_data.get('price'),
                           discount=form.cleaned_data.get('discount'), category=form.cleaned_data.get('category'),
                           user=req.user)
            return redirect(self.post_template)

    @method_decorator(login_required)
    def get(self, req):
        form = CreateProductForm()
        return render(req, self.get_template, {'form': form})


class ProductSeller(View):
    template = 'product_seller.html'

    @method_decorator(login_required)
    def get(self, req):
        products = Product.objects.filter(seller=req.user)
        return render(req, self.template, {'products': products})


class EditProduct(View):
    post_template = 'product_seller'
    get_template = 'edit_product.html'

    @method_decorator(login_required)
    def post(self, req, pk):
        form = CreateProductForm(req.POST)
        if form.is_valid():
            edit_product(name=form.cleaned_data.get('name'), category=form.cleaned_data.get('category'),
                         price=form.cleaned_data.get('price'), discount=form.cleaned_data.get('discount'), pk=pk)
            return redirect(self.post_template)

    @method_decorator(login_required)
    def get(self, req, pk):
        product = get_product(pk=pk)
        form = CreateProductForm(initial={'name': product.name, 'price': product.price, 'category': product.category,
                                          'discount': product.discount})
        return render(req, self.get_template, {'form': form})


class DeleteProduct(View):
    template = 'product_seller'

    @method_decorator(login_required)
    def get(self, req, pk):
        delete_product(pk=pk)
        return redirect('product_seller')


class ViewProduct(View):
    template = 'view_product.html'

    @method_decorator(login_required)
    def get(self, req, pk):
        product = get_product(pk=pk)
        return render(req, self.template, {'product': product})


class ProductCustomer(View):
    template = 'product_customer.html'

    @method_decorator(login_required)
    def get(self, req):
        products = search_list(data={'name': req.GET.get('name')})
        searched = req.GET.get('name', '')
        return render(req, self.template, {'searched': searched, 'products': products})


class Buy(View):
    post_template = 'product_customer'
    get_template = 'buy_product.html'

    @method_decorator(login_required)
    def post(self, req, pk):
        form = BuyProductFrom(req.POST)
        if form.is_valid():
            buy_product(quantity=form.cleaned_data.get('quantity'), product_pk=pk, user=req.user)
            return redirect(self.post_template)

    @method_decorator(login_required)
    def get(self, req, pk):
        product = get_product(pk=pk)
        form = BuyProductFrom()
        return render(req, self.get_template, {'product': product, 'form': form})


class PayPayment(View):
    template = 'pay_payment.html'

    @method_decorator(login_required)
    def get(self, req):
        payment = get_payment(data={'customer': req.user, 'status': False})[0]
        orders = get_payment_orders(payment=payment)
        total_price = 0
        if orders is not None:
            for order in orders:
                total_price += order.calculate_price()
            return render(req, self.template, {'orders': orders, 'total_price': total_price})
        else:
            return render(req, self.template)


class EditOrder(View):
    success_template = 'pay_payment'
    fail_template = 'edit_order.html'

    @method_decorator(login_required)
    def get(self, req, pk):
        order = get_order(pk=pk)
        form = BuyProductFrom(initial={'quantity': order.quantity})
        return render(req, self.fail_template, {'form': form, 'order': order})

    def post(self, req, pk):
        form = BuyProductFrom(req.POST)
        if form.is_valid():
            edit_order(quantity=form.cleaned_data.get('quantity'), pk=pk)
            return redirect(self.success_template)


class DeleteOrder(View):
    template = 'pay_payment'

    @method_decorator(login_required)
    def get(self, req, pk):
        delete_order(pk=pk)
        return redirect(self.template)


class CompletePayment(View):
    template = 'show_payments'

    @method_decorator(login_required)
    def get(self, req):
        complete_payment(user=req.user)
        return redirect(self.template)


class ShowPayments(View):
    template = 'show_payments.html'

    @method_decorator(login_required)
    def get(self, req):
        payments = get_payment(data={'customer': req.user})
        if payments is None:
            return render(req, self.template)
        else:
            return render(req, self.template, {'payments': payments})
