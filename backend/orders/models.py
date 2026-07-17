from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    """A client's single order against one weekly menu.

    Exactly one order may exist per (client, weekly_menu) — enforced by the DB
    constraint below. This slice only ever creates orders in status SUBMITTED; the
    status field is sized for the future CONFIRMED transition (separate feature).
    """

    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", _("Submitted")
        CONFIRMED = "CONFIRMED", _("Confirmed")
        COMPLETED = "COMPLETED", _("Completed")
        CANCELED = "CANCELED", _("Canceled")

    client = models.ForeignKey(
        "accounts.Client",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    weekly_menu = models.ForeignKey(
        "menu.WeeklyMenu",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED,
    )
    notes = models.TextField(
        blank=True, help_text="Allergies, restrictions or preferences for this specific order."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["client", "weekly_menu"],
                name="one_order_per_client_per_menu",
            )
        ]

    def __str__(self) -> str:
        return f"Order<{self.client_id} / menu {self.weekly_menu_id} / {self.status}>"

    @property
    def total_items(self) -> int:
        """Total servings across all items (sum of quantities)."""
        if "items" in getattr(self, "_prefetched_objects_cache", {}):
            return sum(item.quantity for item in self.items.all())
        return self.items.aggregate(total=Sum("quantity"))["total"] or 0


class OrderItem(models.Model):
    """One line of an order: a dish and how many servings of it.

    A dish appears at most once per order; repeats are expressed via `quantity`.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    dish = models.ForeignKey(
        "menu.Dish",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "dish"],
                name="unique_dish_per_order",
            ),
            # MinValueValidator only runs via full_clean()/serializer validation;
            # this backs the same >=1 rule with a DB-level guarantee.
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name="orderitem_quantity_gte_1",
            ),
        ]

    def __str__(self) -> str:
        return f"OrderItem<{self.dish_id} x{self.quantity}>"
