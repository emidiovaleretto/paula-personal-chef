from django.conf import settings
from django.db import models

from accounts.packages import Package


class Client(models.Model):
    """A customer who can order from weekly menus.

    Links to an auth user and carries the meal `package`. `package` is nullable to
    model the safety-rule case of a client with no package (blocked from ordering);
    in practice the chef always assigns one at client creation (out of scope here).
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client",
    )
    package = models.CharField(
        max_length=20,
        choices=Package.choices,
        blank=True,
        default="",
    )

    def __str__(self) -> str:
        return f"Client<{self.user}>"
