from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# from django.contrib.gis.db import models
# from django.contrib.gis.geos import Point


class AccountType(models.Model):
    type = models.CharField(null= True,max_length=40,default="")
    class Meta:
        app_label = 'tracker'

class CountryList(models.Model):
    code = models.CharField(null=True,max_length = 5,default="")
    name = models.CharField(null=True,max_length = 250,default="")

    class Meta:
        app_label = 'tracker'

class EmployeeJourney(models.Model):
    user_from = models.CharField(max_length=200)
    user_to = models.CharField(max_length=200)
    journey_date = models.DateField(default='')
    boarding_point = models.CharField(max_length=200)
    dropping_point = models.CharField(max_length=200)
    
    class Meta:
        app_label = 'tracker'

class Employee(models.Model):
    workspace = models.CharField(max_length=100,default="")
    company_name = models.CharField(null=True,max_length = 100,default="")
    mobile = models.CharField(null=True,max_length=30,default="")
    designation = models.CharField(null=True, max_length=100, default="")
    address = models.CharField(null=True, max_length=200,default="")
    created_date = models.DateField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    class Meta:
        app_label = 'tracker'


class BaseProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True)
    name = models.CharField(null= True,max_length=100,default="")
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10)
    email_id = models.CharField(max_length=350)
    picture = models.ImageField('Profile picture',
                                upload_to='profile_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)
    employee = models.ForeignKey(Employee,null=True)
    company_name = models.CharField(null=True,max_length = 1000,default="")
    company_website = models.CharField(null=True,max_length = 1000,default="")
    telephone = models.CharField(null=True,max_length = 10,default="")
    account_type = models.ForeignKey(AccountType,null=True)
    country_id = models.ForeignKey(CountryList,null=True)
    journey  = models.ForeignKey(EmployeeJourney, null=True)

    class Meta:
        abstract = True        

@python_2_unicode_compatible
class Profile(BaseProfile):
    class Meta:
        app_label = 'tracker'

    def __str__(self):
        return "{}'s profile".format(self.user)

# class City(models.Model):
#     name = models.CharField(max_length=255)
#     geometry = models.MultiPolygonField()

#     objects = models.GeoManager()

# class GeoModel(models.Model):

#     latitude = models.FloatField(blank=True, null=True, verbose_name='Latitude')
#     longitude = models.FloatField(blank=True, null=True, verbose_name='Longitude')
#     location = models.PointField(blank=True, null=True)

#     class Meta:
#         abstract = True

#     def save(self, *args, **kwargs):
#         if self.latitude and self.longitude:
#             self.location = Point(float(self.latitude), float(self.longitude))
#         super(GeoModel, self).save(*args, **kwargs)

