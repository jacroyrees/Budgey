from django.conf import settings
from django.db import models


class Institution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    institution_id = models.CharField(max_length=255, unique=True, db_index=True)
    access_token = models.CharField(max_length=255, unique=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Connection: {self.institution_id} for {self.user.get_username()}"

# Create your models here.
class BankAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    connection = models.ForeignKey(Institution, on_delete=models.CASCADE)
    plaid_account_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)  # e.g., "Main Checking"
    mask = models.CharField(max_length=10, null=True, blank=True)  # Last 4 digits
    type = models.CharField(max_length=50)  # e.g., "depository"
    subtype = models.CharField(max_length=50, null=True, blank=True)  # e.g., "checking"
    balance_available = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    balance_current = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    currency = models.CharField(max_length=10, default="GBP")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.mask})"

class Transaction(models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    plaid_transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    currency = models.CharField(max_length=10, default="GBP")
    name = models.TextField(null=True, blank=True)
    category = models.JSONField(null=True, blank=True)
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name} ({self.category})"