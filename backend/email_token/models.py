
from django.db import models
import uuid

class EmailToken(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, null=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.email
