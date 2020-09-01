from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class EmptyStringToNoneField(models.CharField):
    def get_prep_value(self, value):
        if value == '':
            return None  
        return value
    def from_db_value(self, value, expression, connection):
        if value is None:
            return ''
        return value

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = EmptyStringToNoneField(max_length=11, blank=True, null=True, unique=True )
    def account_verified(self): 
        if self.user.is_authenticated:
            verified = self.user.emailaddress_set.filter(primary=True, verified=True).count() > 0
            return verified
        return False
    def __str__(self):
        return f'{self.user} profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

