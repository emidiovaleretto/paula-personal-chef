"""Meal package definitions and their item bounds.

The three packages are fixed, so they live in code (single source of truth for
the counts) rather than in a database table (plan §Data model).
"Item" means one serving; the same dish chosen twice is two items.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Package(models.TextChoices):
    """Meal package codes and human-readable names."""

    EXPRESS = "EXPRESS", _("Express")
    STANDARD = "STANDARD", _("Standard")
    FULL_WEEK = "FULL_WEEK", _("Full week")


# Inclusive (min, max) total-item bounds per package.
# Exact packages have min == max.

PACKAGE_BOUNDS: dict[str, tuple[int, int]] = {
    Package.EXPRESS: (4, 5),
    Package.STANDARD: (7, 7),
    Package.FULL_WEEK: (11, 11),
}


def bounds_for(package: str) -> tuple[int, int] | None:
    """Return the inclusive (min, max) item bounds for a package code.

    Returns None for an unassigned or unrecognized package (e.g. the
    no-package safety-rule case), rather than raising, so callers can turn
    it into the blocked-from-ordering message instead of a 500.
    """
    return PACKAGE_BOUNDS.get(package)
