"""Meal package definitions and their item bounds.

The three packages are fixed, so they live in code (single source of truth for
the counts) rather than in a database table (plan §Data model).
"Item" means one serving; the same dish chosen twice is two items.
"""

from django.db import models


class Package(models.TextChoices):
    """Meal package codes and human-readable names."""

    EXPRESS = "EXPRESS"
    STANDARD = "STANDARD"
    FULL_WEEK = "FULL_WEEK"


# Inclusive (min, max) total-item bounds per package.
# Exact packages have min == max.

PACKAGE_BOUNDS: dict[str, tuple[int, int]] = {
    Package.EXPRESS: (4, 5),
    Package.STANDARD: (7, 7),
    Package.FULL_WEEK: (11, 11),
}


def bounds_for(package: str) -> tuple[int, int]:
    """Return the inclusive (min, max) item bounds for a package code."""
    return PACKAGE_BOUNDS[package]
