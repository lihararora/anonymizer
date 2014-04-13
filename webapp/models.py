from django.db import models

# Create your models here.

class User(models.Model):
    ROLE_CHOICES = (
                    ('Doctor','Doctor'),
                    ('Nurse','Nurse'),
                    ('Management','Management'),
                    ('Researcher','Researcher'),
                    )
    user_name = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)