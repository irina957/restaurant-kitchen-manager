from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.forms import (
    CookCreationForm,
    CookExperienceUpdateForm,
    DishForm,
    DishSearchForm,
    validate_experience,
)
from kitchen.models import DishType, Dish


class ValidateExperienceTest(TestCase):
    def test_valid_experience(self):
        self.assertEqual(validate_experience(5), 5)

    def test_negative_experience_raises_error(self):
        with self.assertRaises(forms.ValidationError):
            validate_experience(-1)


class CookCreationFormTest(TestCase):
    def test_valid_form_creates_user(self):
        form_data = {
            "username": "test",
            "password1": "Ppassword123",
            "password2": "Ppassword123",
            "first_name": "John",
            "last_name": "Green",
            "years_of_experience": 3,
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        cook = form.save()
        self.assertEqual(cook.username, "test")
        self.assertEqual(cook.years_of_experience, 3)

    def test_negative_experience_invalid(self):
        form_data = {
            "username": "test",
            "password1": "Ppassword123",
            "password2": "Ppassword123",
            "years_of_experience": -2,
        }
        form = CookCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)


class CookExperienceUpdateFormTest(TestCase):
    def setUp(self):
        self.cook = get_user_model().objects.create_user(
            username="test", password="test123", years_of_experience=5
        )

    def test_update_years_of_experience_valid(self):
        form = CookExperienceUpdateForm(
            data={"years_of_experience": 8}, instance=self.cook
        )
        self.assertTrue(form.is_valid())
        updated_cook = form.save()
        self.assertEqual(updated_cook.years_of_experience, 8)

    def test_update_negative_experience_invalid(self):
        form = CookExperienceUpdateForm(
            data={"years_of_experience": -1}, instance=self.cook
        )
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)


class DishFormTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Soup")
        self.cook = get_user_model().objects.create_user(
            username="cook", password="12345"
        )

    def test_valid_dish_form(self):
        form_data = {"name": "Borshch", "price": 12.50, "dish_type": self.dish_type.id, "cooks": [self.cook.id]}
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())
        dish = form.save()
        self.assertEqual(dish.name, "Borshch")

    def test_missing_required_field_invalid(self):
        form_data = {"price": 10.0}
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class DishSearchFormTest(TestCase):
    def test_valid_search_form(self):
        form = DishSearchForm(data={"name": "Borshch"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Borshch")

    def test_empty_search_valid(self):
        form = DishSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
