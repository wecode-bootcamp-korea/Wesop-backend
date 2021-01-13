from django.db import models

class User(models.Model):
    email      = models.CharField (max_length = 45)
    password   = models.CharField (max_length = 200)
    last_name  = models.CharField (max_length = 45)
    first_name = models.CharField (max_length = 45)

    class Meta:
        db_table = 'users'

class Address(models.Model):
    user     = models.ForeignKey ('User', on_delete=models.CASCADE)
    country  = models.CharField (max_length = 45)
    address  = models.CharField (max_length = 200)
    zip_code = models.IntegerField
    phone    = models.CharField (max_length = 45)

    class Meta:
        db_table = 'addresses'