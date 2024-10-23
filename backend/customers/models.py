from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    password = models.CharField(max_length=100, null=True)
    email_confirmed = models.BooleanField(default=False, null=True)
    password_reset_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)

    def __str__(self):
        return self.name
    
    def set_password(self, raw_password):
        if self.email_confirmed:
            self.password = make_password(raw_password)
            self.save()
        else:
            raise Exception("Email no confirmado")

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    

    
