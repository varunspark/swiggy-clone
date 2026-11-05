from django.core.management.base import BaseCommand
from core.models import Restaurant, MenuItem

DATA = {
    ("Meghana Biryani", "Biryani", "4.5", "Koramangala, Bengaluru"): [
        ("Chicken Biryani", 280, False), ("Paneer Biryani", 240, True), ("Raita", 40, True)],
    ("Udupi Tiffins", "South Indian", "4.3", "Jayanagar, Bengaluru"): [
        ("Masala Dosa", 90, True), ("Idli Vada", 70, True), ("Filter Coffee", 30, True)],
    ("Pizza Corner", "Italian", "4.1", "Indiranagar, Bengaluru"): [
        ("Margherita", 250, True), ("Chicken Pizza", 330, False)],
}


class Command(BaseCommand):
    help = "Load sample restaurants (safe to run repeatedly)"

    def handle(self, *args, **opts):
        for (name, cuisine, rating, addr), items in DATA.items():
            r, _ = Restaurant.objects.get_or_create(
                name=name, defaults={"cuisine": cuisine, "rating": rating, "address": addr})
            for n, p, v in items:
                MenuItem.objects.get_or_create(restaurant=r, name=n, defaults={"price": p, "is_veg": v})
        self.stdout.write("Seeded.")
