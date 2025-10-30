from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen.models import DishType, Dish, Cook


class KitchenViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="test_user",
            password="password123",
            years_of_experience=5,
        )
        self.client.force_login(self.user)

        self.dish_type = DishType.objects.create(name="Hot Soup")
        self.dish = Dish.objects.create(
            name="Borshch",
            price=15,
            dish_type=self.dish_type
        )

    def test_index_view(self):
        response = self.client.get(reverse("kitchen:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/index.html")
        self.assertIn("num_cooks", response.context)
        self.assertIn("num_dishes", response.context)
        self.assertIn("num_dish_types", response.context)
        self.assertIn("num_visits", response.context)

    def test_unauthenticated_user_redirected(self):
        self.client.logout()
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_dish_list_view(self):
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_list.html")
        self.assertContains(response, self.dish.name)

    def test_dish_detail_view(self):
        response = self.client.get(reverse("kitchen:dish-detail", args=[self.dish.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_detail.html")
        self.assertEqual(response.context["dish"], self.dish)

    def test_dish_create_view(self):
        response = self.client.post(reverse("kitchen:dish-create"), {
            "name": "Salad",
            "price": 12,
            "dish_type": self.dish_type.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dish.objects.filter(name="Salad").exists())

    def test_dish_update_view(self):
        url = reverse("kitchen:dish-update", args=[self.dish.id])
        response = self.client.post(url, {
            "name": "Updated Borshch",
            "price": 20,
            "dish_type": self.dish_type.id
        })
        self.assertEqual(response.status_code, 302)
        self.dish.refresh_from_db()
        self.assertEqual(self.dish.name, "Updated Borshch")
        self.assertEqual(self.dish.price, 20)

    def test_dish_delete_view(self):
        url = reverse("kitchen:dish-delete", args=[self.dish.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Dish.objects.filter(id=self.dish.id).exists())

    def test_dishtype_list_view(self):
        response = self.client.get(reverse("kitchen:dish-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dish_type.name)

    def test_dishtype_create_view(self):
        response = self.client.post(reverse("kitchen:dish-type-create"), {"name": "Salads"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(DishType.objects.filter(name="Salads").exists())

    def test_dishtype_update_view(self):
        url = reverse("kitchen:dish-type-update", args=[self.dish_type.id])
        response = self.client.post(url, {"name": "Hot soups"})
        self.assertEqual(response.status_code, 302)
        self.dish_type.refresh_from_db()
        self.assertEqual(self.dish_type.name, "Hot soups")

    def test_dishtype_delete_view(self):
        url = reverse("kitchen:dish-type-delete", args=[self.dish_type.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DishType.objects.filter(id=self.dish_type.id).exists())

    def test_cook_list_view(self):
        response = self.client.get(reverse("kitchen:cook-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_list.html")
        self.assertContains(response, self.user.username)

    def test_cook_detail_view(self):
        response = self.client.get(reverse("kitchen:cook-detail", args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_detail.html")
        self.assertEqual(response.context["cook"], self.user)

    def test_cook_create_view(self):
        response = self.client.post(reverse("kitchen:cook-create"), {
            "username": "newcook",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "years_of_experience": 3,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="newcook").exists())

    def test_assign_me_view(self):
        url = reverse("kitchen:assign-me", args=[self.dish.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user, self.dish.cooks.all())

    def test_remove_me_view(self):
        self.dish.cooks.add(self.user)
        url = reverse("kitchen:remove-me", args=[self.dish.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.user, self.dish.cooks.all())
