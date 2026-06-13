from datetime import date, timedelta

from django.apps import apps
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


_SMALLEST_GIF = (
    b"GIF87a\x01\x00\x01\x00\x80\x01\x00\xff\xff\xff\x00\x00\x00,"
    b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;"
)


def model(name):
    return apps.get_model("app", name)


def make_image(name="property.gif"):
    return SimpleUploadedFile(name, _SMALLEST_GIF, content_type="image/gif")


def make_user(username="agent", is_superuser=False, is_staff=True):
    return User.objects.create_user(
        username=username,
        password="pw12345!",
        is_staff=is_staff,
        is_superuser=is_superuser,
    )


def make_agent(username="agent", name="Test", surname="Agent", user=None):
    Agent = model("Agent")
    if user is None:
        user = make_user(username)
    return Agent.objects.create(
        user=user,
        name=name,
        surname=surname,
        contact_phone="070000000",
        linked_in_profile=f"https://linkedin.com/in/{username}",
        completed_sales=0,
        email=f"{username}@example.com",
    )


def make_feature(name="Elevator", value=10000):
    Feature = model("Feature")
    return Feature.objects.create(name=name, value=value)


def make_property(
    name="Modern Villa",
    area=150,
    listed_date=None,
    sold=False,
    reserved=False,
    description="Quiet residential location",
    with_image=True,
):
    Property = model("Property")
    kwargs = {
        "name": name,
        "description": description,
        "area": area,
        "date": listed_date or date.today(),
        "reserved": reserved,
        "sold": sold,
    }
    if with_image:
        kwargs["image"] = make_image(f"{name.replace(' ', '_')}.gif")
    return Property.objects.create(**kwargs)


def make_old_property(**kwargs):
    kwargs.setdefault("listed_date", date.today() - timedelta(days=1))
    return make_property(**kwargs)


def assign_agent(prop, agent):
    PropertyAgent = model("PropertyAgent")
    return PropertyAgent.objects.create(property=prop, agent=agent)


def assign_feature(prop, feature):
    PropertyFeature = model("PropertyFeature")
    return PropertyFeature.objects.create(property=prop, feature=feature)
