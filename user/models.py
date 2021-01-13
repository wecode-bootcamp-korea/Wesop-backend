from django.db import models

class User(models.Model):
    email      = models.CharField(max_length = 45)
    password   = models.CharField(max_length = 200)
    last_name  = models.CharField(max_length = 45)
    first_name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'users'

class Address(models.Model):
    user     = models.ForeignKey('User', on_delete=models.CASCADE)
    address  = models.CharField(max_length = 200)
    zipcode = models.CharField(max_length = 45)
    phone    = models.CharField(max_length = 45)

    class Meta:
        db_table = 'addresses'

class Country(models.Model):
    adress = models.OneToOneField('Address', on_delete=models.CASCADE)
    name   = models.CharField(max_length=45)
    number = models.IntegerField()

    class Meta:
        db_table = 'countries'