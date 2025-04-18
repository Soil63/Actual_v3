from django.test import TestCase

from .models import Benevole

class BenevoleModelTest(TestCase):
    def test_benevole_creation(self):
        benevole = Benevole.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean.dupont@example.com",
            date_naiss="1990-01-01",
            phone_number="0123456789",
            address="123 Rue Exemple",
            volontaire_plus=True,
        )
        self.assertEqual(benevole.nom, "Dupont")
        self.assertTrue(benevole.volontaire_plus)


# Create your tests here.
