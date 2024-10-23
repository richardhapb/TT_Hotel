
from django.db import models

class EmailToken(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.email
