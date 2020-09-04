from django.db import models
from django.dispatch import receiver

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, validate_image_file_extension, MinValueValidator,  MaxValueValidator
from smart_selects.db_fields import ChainedForeignKey

import os
import datetime
User = get_user_model()

# Helper Functions


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def normalize(string):
    return string.replace(' ', '_').lower()


# the models
class Governorate(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Destrict(models.Model):
    governorate = models.ForeignKey(
        Governorate, related_name='destricts', on_delete=models.PROTECT)
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Listing(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='listings')
    favorites = models.ManyToManyField(User,
                                       through='Fav', related_name='favorite_listings', blank=True)
    governorate = models.ForeignKey(Governorate, on_delete=models.PROTECT)
    destrict = ChainedForeignKey(
        Destrict,
        chained_field="governorate",
        chained_model_field="governorate",
        show_all=False,
        auto_choose=True,
        sort=True)

    class Status(models.IntegerChoices):
        FOR_RENT = 1
        FOR_SALE = 2
        FOR_TIMESHARE = 3

    prop_status = models.IntegerField(choices=Status.choices)

    class Type(models.IntegerChoices):
        APARTMENT = 1
        CHALET = 2
        HOUSE = 3
        STUDIO = 4
        VILLA = 5

    prop_type = models.IntegerField(choices=Type.choices)
    price = models.DecimalField(max_digits=9, decimal_places=0, validators=[
                                MinValueValidator(1, "Price must be greater than 0")])
    number_of_bedrooms = models.PositiveSmallIntegerField()
    number_of_baths = models.PositiveSmallIntegerField()
    square_metre = models.PositiveSmallIntegerField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.get_prop_type_display()} {self.get_prop_status_display()} in {self.destrict.name}, #{self.pk}'

    @classmethod
    def get_value_from_name(self, class_name, var_name):
        return self.__dict__[class_name].__dict__[var_name].value

    def get_absolute_url(self):
        return reverse("listings:listing_detail", kwargs={"pk": self.pk, "status": normalize(self.get_prop_status_display()),
                                                          "type": normalize(self.get_prop_type_display()),
                                                          "governorate": self.governorate.name,
                                                          "destrict": self.destrict.name})


class Picture(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='pictures')
    description = models.CharField(
        max_length=20,
        blank=True)
    url = models.ImageField(upload_to='uploads/%Y/%m/%d',
                            validators=[validate_image_file_extension])

    def __str__(self):
        return f'Picture of listing #{self.listing.id}'


class Fav(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('listing', 'user')

    #def save(self, *args, **kwargs):
        #    if not self.user:
        #        self.user = self.created_by
        #self.user = self.created_by
        #super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} likes listing #{self.listing.id}'


class Propty(models.Model):
    listing = models.OneToOneField(
        Listing, on_delete=models.CASCADE, related_name='propty')

    class View(models.IntegerChoices):
        CORNER = 1
        WATER = 2
        MAIN_STREET = 3
        SIDE_STREET = 4
        GARDEN = 5
        YARD = 6

    class Storeys(models.IntegerChoices):
        SINGLE = 1
        DUPLEX = 2
        TRIPLEX = 3

    class Flooring(models.IntegerChoices):
        MARBLE = 1
        HARDWOOD = 2
        CERAMIC_TILE = 3
        STONE = 4
        PARQUET = 5
        SOFTWOOD = 6
        NON_CERAMIC_TILE = 7
        LAMINATE = 8
        LINOLEUM = 9

    class FinshType(models.IntegerChoices):
        UNFINISHED = 1
        SEMI_FINISHED = 2
        FULLY_FINISHED = 3
        LUX = 4
        SUPER_LUX = 5
        ULTRA_LUX = 6
        DELUXE = 7

    class PaymentMethod(models.IntegerChoices):
        CASH = 1
        INSTALLMENTS = 2

    finish_type = models.IntegerField(
        choices=FinshType.choices, null=True, blank=True)
    payment_method = models.IntegerField(
        choices=PaymentMethod.choices, null=True, blank=True)

    view = models.IntegerField(choices=View.choices, null=True, blank=True)
    storeys = models.IntegerField(
        choices=Storeys.choices, null=True, blank=True)
    flooring = models.IntegerField(
        choices=Flooring.choices, null=True, blank=True)
    address = models.CharField(max_length=100, blank=True)
    level = models.PositiveSmallIntegerField(null=True, blank=True)
    number_of_balconies = models.PositiveSmallIntegerField(
        null=True, blank=True)
    year_built = models.IntegerField(validators=[MinValueValidator(
        1900), max_value_current_year], null=True, blank=True)
    available_on = models.DateField(default=datetime.date.today, null=True)

    description = models.TextField(validators=[MinLengthValidator(
        100, "ad must be greater than 99 characters")], blank=True)

    has_garage_parking = models.BooleanField(null=True)
    has_central_air_conditioning = models.BooleanField(null=True)
    has_wall_air_conditioning = models.BooleanField(null=True)
    has_security_system = models.BooleanField(null=True)
    has_elevator = models.BooleanField(null=True)
    in_compound = models.BooleanField(null=True)
    has_intercom_system = models.BooleanField(null=True)
    has_bool = models.BooleanField(null=True)
    is_furnished = models.BooleanField(null=True)

    def __str__(self):
        return f'property facts, listing #{self.listing.id}'


# signals

@receiver(models.signals.post_delete, sender=Picture)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.url:
        if os.path.isfile(instance.url.path):
            os.remove(instance.url.path)


@receiver(models.signals.pre_save, sender=Picture)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).url
    except sender.DoesNotExist:
        return False

    new_file = instance.url
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
