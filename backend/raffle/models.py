from django.db import models

class Raffle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    winner = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
