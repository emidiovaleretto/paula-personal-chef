"""factory_boy factories for tests (constitution §3 — factories over static fixtures)."""

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import Client
from accounts.packages import Package
from menu.models import Dish, WeeklyMenu
from orders.models import Order, OrderItem

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    user = factory.SubFactory(UserFactory)
    package = Package.STANDARD


class WeeklyMenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WeeklyMenu

    week_start = factory.LazyFunction(lambda: timezone.localdate())
    is_published = True
    published_at = factory.LazyFunction(timezone.now)
    is_active = True


class DishFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dish

    weekly_menu = factory.SubFactory(WeeklyMenuFactory)
    name = factory.Sequence(lambda n: f"Dish {n}")
    description = factory.LazyAttribute(lambda o: f"Description of {o.name}")


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    client = factory.SubFactory(ClientFactory)
    weekly_menu = factory.SubFactory(WeeklyMenuFactory)
    status = Order.Status.SUBMITTED


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    dish = factory.SubFactory(
        DishFactory,
        weekly_menu=factory.SelfAttribute("..order.weekly_menu"),
    )
    quantity = 1
