from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from kitchen.models import DishType, Cook, Dish

class BaseTestCase(TestCase):
    def setUp(self):
        self.cook = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
            years_of_experience = 10)
        self.dish_type = DishType.objects.create(name="test_name",)
        self.dish = Dish.objects.create(name="test", price=10, dish_type=self.dish_type)


class CookTestCase(BaseTestCase):

    def test_cook_str(self):
        self.assertEqual(str(self.cook), f"{self.cook.username} ({self.cook.first_name} {self.cook.last_name})")

    def test_cook_verbose_name(self):
        self.assertEqual(self.cook._meta.verbose_name, "cook")

    def test_cook_verbose_name_plural(self):
        self.assertEqual(self.cook._meta.verbose_name_plural, "cooks")

    def test_cook_years_of_experience_label(self):
        self.assertEqual(self.cook._meta.get_field("years_of_experience").verbose_name, "years of experience")

    def test_cook_get_absolute_url(self):
        self.assertEqual(self.cook.get_absolute_url(), f"/cooks/{self.cook.id}/")

    def test_cook_years_of_experience_default(self):
        cook = get_user_model().objects.create_user(username="user2", password="pass")
        self.assertEqual(cook.years_of_experience, 0)

    def test_cook_password_set_correctly(self):
        password = "securepassword1"
        cook = get_user_model().objects.create_user(username="user3", password=password)
        self.assertTrue(cook.check_password(password))

    def test_cook_ordering_by_username(self):
        cook2 = get_user_model().objects.create_user(username="zzz", password="pass")
        cooks = list(get_user_model().objects.all())
        self.assertEqual(cooks, sorted(cooks, key=lambda x: x.username))

    def test_cook_dishes_relationship(self):
        self.dish.cooks.add(self.cook)
        self.assertIn(self.cook, self.dish.cooks.all())
        self.assertIn(self.dish, self.cook.cooked_dishes.all())


class DishTestCase(BaseTestCase):

    def test_dish_str(self):
        self.assertEqual(str(self.dish), f"name: {self.dish.name}, price: {self.dish.price}")

    def test_dish_verbose_name(self):
        self.assertEqual(self.dish._meta.verbose_name, "dish")

    def test_dish_verbose_name_plural(self):
        self.assertEqual(self.dish._meta.verbose_name_plural, "dishes")

    def test_dish_ordering_by_name(self):
        dish2 = Dish.objects.create(name="zzz", price=20, dish_type=self.dish_type)
        dishes = list(Dish.objects.all())
        self.assertEqual(dishes, sorted(dishes, key=lambda x: x.name))

    def test_dish_max_length_name(self):
        max_length = self.dish._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_dish_max_digits_price(self):
        field = self.dish._meta.get_field("price")
        self.assertEqual(field.max_digits, 7)
        self.assertEqual(field.decimal_places, 2)

    def test_dish_get_absolute_url(self):
        self.assertEqual(self.dish.get_absolute_url(), f"/dishes/{self.dish.id}/")

    def test_dish_cooks_relationship(self):
        self.dish.cooks.add(self.cook)
        self.assertIn(self.cook, self.dish.cooks.all())
        self.assertIn(self.dish, self.cook.cooked_dishes.all())


class DishTypeTestCase(BaseTestCase):

    def test_dishtype_str(self):
        self.assertEqual(str(self.dish_type), self.dish_type.name)

    def test_dishtype_ordering_by_name(self):
        dt2 = DishType.objects.create(name="zzz")
        dish_types = list(DishType.objects.all())
        self.assertEqual(dish_types, sorted(dish_types, key=lambda x: x.name))

    def test_dishtype_related_dishes(self):
        dish = Dish.objects.create(name="New Dish", price=15, dish_type=self.dish_type)
        self.assertIn(dish, self.dish_type.dishes.all())

    def test_dish_type_name_unique(self):
        DishType.objects.create(name="Hot Soup")
        with self.assertRaises(IntegrityError):
            DishType.objects.create(name="Hot Soup")

    def test_dishtype_name_max_length(self):
        max_length = self.dish_type._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)
