import tempfile

from django.test import TestCase, override_settings


_TEST_MEDIA_ROOT = tempfile.mkdtemp(prefix="real_estate_test_media_")


@override_settings(MEDIA_ROOT=_TEST_MEDIA_ROOT)
class RealEstateTestCase(TestCase):
    pass
