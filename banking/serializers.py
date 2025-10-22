from rest_framework import serializers
from .models import InstitutionConnection, BankAccount, Transaction

# --- Plaid Flow Serializers ---

class LinkTokenRequestSerializer(serializers.Serializer):
    """
    Serializer for the initial request to generate a Link Token.
    """
    # This can be expanded if the user needs to specify language, products, etc.
    # For now, we'll keep it simple as the view handles defaults from settings.
    institution_id = serializers.CharField(required=False, allow_null=True)


class PublicTokenExchangeSerializer(serializers.Serializer):
    """
    Serializer for the public token received from the Plaid Link successful callback.
    """
    public_token = serializers.CharField(max_length=255)
    institution_name = serializers.CharField(max_length=255)
    institution_id = serializers.CharField(max_length=255)


# --- Model Serializers (for API responses) ---

class InstitutionConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionConnection
        fields = ['id', 'institution_name', 'created_at']
        read_only_fields = ['id', 'institution_name', 'created_at']

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        exclude = ['user', 'connection', 'created_at', 'updated_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ['bank_account', 'created_at', 'updated_at']
