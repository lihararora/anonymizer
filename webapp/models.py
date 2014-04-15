from django.db import models

# Create your models here.

class User(models.Model):
    ROLE_CHOICES = (
                    ('Doctor','Doctor'),
                    ('Staff','Staff'),
                    ('Management','Management'),
                    ('Researcher','Researcher'),
                    )
    user_name = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=50)
    author_id = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    contents = models.TextField()