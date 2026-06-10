from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from app.models import Baker, Cake


_SMALLEST_GIF = (
    b"GIF87a\x01\x00\x01\x00\x80\x01\x00\xff\xff\xff\x00\x00\x00,"
    b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;"
)


def make_image(name="cake.gif"):
    return SimpleUploadedFile(name, _SMALLEST_GIF, content_type="image/gif")


def make_user(username="user", is_superuser=False, is_staff=True):
    user = User.objects.create_user(
        username=username,
        password="pw12345!",
        is_staff=is_staff,
        is_superuser=is_superuser,
    )
    return user


def make_baker(username="baker", name="Test", surname="Baker", user=None):
    if user is None:
        user = make_user(username)
    return Baker.objects.create(
        user=user,
        name=name,
        surname=surname,
        contact_phone="070000000",
        email=f"{username}@example.com",
    )


def make_cake(
    baker,
    name="Chocolate Cake",
    price=100,
    weight=1.5,
    description="Fresh cake",
    with_picture=True,
):
    kwargs = {
        "baker": baker,
        "name": name,
        "price": price,
        "weight": weight,
        "description": description,
    }
    if with_picture:
        kwargs["picture"] = make_image(f"{name.replace(' ', '_')}.gif")
    return Cake.objects.create(**kwargs)
