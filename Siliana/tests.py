import os
from decimal import Decimal

from django.test import TestCase, override_settings

from .models import Order, Produit


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class PublicOrderTests(TestCase):
    def setUp(self):
        self.produit = Produit.objects.create(
            nom="Test Produit",
            quantite=10,
            prix_achat=Decimal("5.00"),
            prix_vente=Decimal("7.50"),
        )

    def _set_env(self, **vars):
        previous = {}
        for key, value in vars.items():
            previous[key] = os.environ.get(key)
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = str(value)

        def restore():
            for key, old in previous.items():
                if old is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = old

        self.addCleanup(restore)

    def test_catalog_page_renders(self):
        resp = self.client.get("/product/")
        self.assertEqual(resp.status_code, 200)

    def test_cart_page_renders(self):
        resp = self.client.get("/cart/")
        self.assertEqual(resp.status_code, 200)

    def test_product_detail_page_renders(self):
        resp = self.client.get(f"/product/{self.produit.id}/")
        self.assertEqual(resp.status_code, 200)

    def test_order_page_renders_in_firebase_mode(self):
        self._set_env(PHONE_VERIFICATION_MODE="firebase")
        resp = self.client.get("/order/")
        self.assertEqual(resp.status_code, 200)

    def test_order_page_renders_in_static_code_mode(self):
        self._set_env(PHONE_VERIFICATION_MODE="static_code", PHONE_VERIFICATION_CODE="20707272")
        resp = self.client.get("/order/")
        self.assertEqual(resp.status_code, 200)

    def test_post_static_code_wrong_code_does_not_create_order(self):
        self._set_env(PHONE_VERIFICATION_MODE="static_code", PHONE_VERIFICATION_CODE="20707272")

        resp = self.client.post(
            "/order/",
            data={
                "nom": "Client",
                "wilaya": "تونس",
                "ville": "Tunis",
                "telephone": "+21620123456",
                "manual_verification_code": "0000",
                f"product_{self.produit.id}": "1",
            },
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)

    def test_post_static_code_correct_code_creates_order_and_decrements_stock(self):
        self._set_env(PHONE_VERIFICATION_MODE="static_code", PHONE_VERIFICATION_CODE="20707272")

        resp = self.client.post(
            "/order/",
            data={
                "nom": "Client",
                "wilaya": "تونس",
                "ville": "Tunis",
                "telephone": "+21620123456",
                "manual_verification_code": "20707272",
                f"product_{self.produit.id}": "2",
            },
            follow=True,
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)

        self.assertIn('/order/sent/', resp.request.get('PATH_INFO', ''))
        self.assertContains(resp, '#')

        self.produit.refresh_from_db()
        self.assertEqual(self.produit.quantite, 8)

    def test_post_firebase_mode_missing_token_does_not_create_order(self):
        self._set_env(PHONE_VERIFICATION_MODE="firebase")

        resp = self.client.post(
            "/order/",
            data={
                "nom": "Client",
                "wilaya": "تونس",
                "ville": "Tunis",
                "telephone": "+21620123456",
                f"product_{self.produit.id}": "1",
            },
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)
