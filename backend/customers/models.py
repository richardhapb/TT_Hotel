from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    password = models.CharField(max_length=100, null=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    
