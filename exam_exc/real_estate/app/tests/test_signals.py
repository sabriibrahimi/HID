from .base import RealEstateTestCase as TestCase
from .factories import assign_agent, assign_feature, make_agent, make_feature, make_property


class PropertySoldSignalTest(TestCase):
    def test_marking_property_sold_increments_all_assigned_agents(self):
        prop = make_property(sold=False)
        first = make_agent("first")
        second = make_agent("second")
        assign_agent(prop, first)
        assign_agent(prop, second)

        prop.sold = True
        prop.save()
        first.refresh_from_db()
        second.refresh_from_db()

        self.assertEqual(first.completed_sales, 1)
        self.assertEqual(second.completed_sales, 1)

    def test_saving_already_sold_property_does_not_increment_again(self):
        prop = make_property(sold=False)
        agent = make_agent("repeat")
        assign_agent(prop, agent)

        prop.sold = True
        prop.save()
        prop.description = "Changed description"
        prop.save()
        agent.refresh_from_db()

        self.assertEqual(agent.completed_sales, 1)


class PropertyFeatureSignalTest(TestCase):
    def test_property_feature_summary_updates_after_feature_changes(self):
        prop = make_property()
        assign_feature(prop, make_feature("Elevator", 10000))
        assign_feature(prop, make_feature("Pool", 25000))
        prop.refresh_from_db()

        self.assertIn("Elevator", prop.feature)
        self.assertIn("Pool", prop.feature)
        self.assertIn(",", prop.feature)
