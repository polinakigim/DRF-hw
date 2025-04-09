import os

import stripe
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_stripe_product(payment):
    """Функция создания продукта в Stripe."""
    product_name = (
        payment.paid_course.name if payment.paid_course else payment.paid_lesson.name
    )

    products = stripe.Product.list(limit=100)
    for product in products:
        if product.name == product_name:
            return product["id"]

    stripe_product = stripe.Product.create(name=product_name)
    return stripe_product["id"]


def create_stripe_price(product_id, amount):
    """Создает цену в Stripe."""
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product=product_id,
    )


def create_stripe_session(price):
    """Создает сессию на оплату в Stripe."""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
