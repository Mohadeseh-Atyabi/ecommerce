from .models import Product, Payment, Order, Category


def search_list(*, data: dict) -> list[Product]:
    name = data.get('name', '')
    user = data.get('user', '')
    filters = {}
    if name:
        filters['name__icontains'] = name
    if user:
        filters['seller'] = user
    products = Product.objects.filter(**filters)
    return products


def create_product(*, name, price, discount, category, user) -> Product:
    product = Product(
        name=name,
        price=price,
        category=category,
        discount=discount,
        seller=user
    )
    product.save()
    return product


def edit_product(*, name, price, category, discount, pk) -> Product:
    product = get_product(pk=pk)
    product.name = name
    product.price = price
    product.category = category
    product.discount = discount
    product.save()
    return product


def get_all_products() -> Product:
    products = Product.objects.all()
    return products


def get_product(*, pk) -> Product:
    product = Product.objects.get(id=pk)
    return product


def get_order(*, pk) -> Order:
    order = Order.objects.get(id=pk)
    return order


def get_payment(*, data: dict) -> list[Payment]:
    status = data.get('status', '')
    user = data.get('customer', '')
    filters = {}
    if 'status' in data.keys():
        filters['status'] = status
    if user:
        filters['customer'] = user
    payments = Payment.objects.filter(**filters)
    return payments


def get_category(*, pk) -> Category:
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        category = None
    return category


def delete_product(*, pk) -> None:
    product = Product.objects.get(id=pk)
    product.delete()


def buy_product(*, quantity, product_pk, user) -> Order:
    product = Product.objects.get(id=product_pk)
    try:
        payment = Payment.objects.get(customer=user, status=False)
    except Payment.DoesNotExist:
        payment = Payment(
            status=False,
            customer=user
        )
        payment.save()

    order = Order(
        product=product,
        quantity=quantity,
        payment=payment
    )
    order.save()
    return order


def get_payment_orders(*, payment) -> list[Order]:
    orders = Order.objects.filter(payment=payment)
    return orders


def pay_payment(*, user) -> tuple[Order | None, int | None]:
    try:
        payment = Payment.objects.get(customer=user, status=False)
        orders = Order.objects.filter(payment=payment)
        total_price = 0
        for order in orders:
            total_price += order.calculate_price()
    except Payment.DoesNotExist:
        orders = None
        total_price = None

    return orders, total_price


def edit_order(*, quantity, pk) -> Order:
    order = get_order(pk=pk)
    order.quantity = quantity
    order.save()
    return order


def delete_order(*, pk) -> None:
    order = get_order(pk=pk)
    order.delete()


def complete_payment(*, user) -> Payment:
    payment = Payment.objects.get(customer=user, status=False)
    payment.status = True
    payment.save()
    return payment
