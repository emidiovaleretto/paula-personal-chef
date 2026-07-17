from django.db import models


class WeeklyMenu(models.Model):
    """A weekly menu the chef publishes.

    The "current" menu is the most recently published, still-active one
    (see `menu.services.current_weekly_menu`). `week_start` is set by the chef at
    publish time (interpreted in Europe/Dublin). Authoring/publishing is out of scope
    for this feature; records are created via admin/factory.
    """

    week_start = models.DateField()
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        # nulls_last pins NULL placement explicitly: Postgres defaults NULLs
        # first on DESC, SQLite defaults them last, which would otherwise
        # flip whether a draft outranks the latest published menu by environment.
        ordering = [models.F("published_at").desc(nulls_last=True)]
        constraints = [
            # is_published and published_at are two separate fields per plan
            # §Data model; this stops them drifting apart in the direction
            # that matters (marked published with no timestamp).
            models.CheckConstraint(
                condition=models.Q(is_published=False) | models.Q(published_at__isnull=False),
                name="weeklymenu_published_at_set_when_published",
            )
        ]

    def __str__(self) -> str:
        return f"WeeklyMenu(week_start={self.week_start})"


class Dish(models.Model):
    """A dish available on a specific weekly menu.

    Availability is unlimited within the week (cook-to-order) — there is no stock field.
    """

    weekly_menu = models.ForeignKey(
        WeeklyMenu,
        on_delete=models.CASCADE,
        related_name="dishes",
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name
