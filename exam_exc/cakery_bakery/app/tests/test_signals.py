from app.models import Cake

from .base import CakeryTestCase as TestCase
from .factories import make_baker, make_cake


class BakerDeletionRedistributionTest(TestCase):
    def test_deleted_bakers_cakes_are_redistributed(self):
        departing = make_baker("departing")
        remaining_a = make_baker("remaining_a")
        remaining_b = make_baker("remaining_b")
        cake_ids = [
            make_cake(departing, name="Departing 1").id,
            make_cake(departing, name="Departing 2").id,
        ]
        departing.delete()
        redistributed = Cake.objects.filter(id__in=cake_ids)
        self.assertEqual(redistributed.count(), 2)
        self.assertTrue(
            all(cake.baker_id in {remaining_a.id, remaining_b.id} for cake in redistributed)
        )
