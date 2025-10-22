import time

import plaid
from django.conf import settings
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.payment_initiation_recipient_create_request import PaymentInitiationRecipientCreateRequest
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .client import client
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from .models import Institution


# Create your views here.


class PlaidBaseView(APIView):

    def get_plaid_client(self):
         if not client:
            return Response({"detail": "Plaid client is not configured"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
         return client



    def handle_plaid_error(self, e):
        error_type = getattr(e, 'type', 'API_ERROR')
        error_code = getattr(e, 'code', 'PLAID_ERROR')
        error_message = str(e)

        return Response(
            {"error_type": error_type, "error_code": error_code, "detail": error_message},
            status=status.HTTP_400_BAD_REQUEST
        )

class PublicTokenCreate(PlaidBaseView):

    def post(self, request):
        request = SandboxPublicTokenCreateRequest(
            institution_id='ins_109508',
            initial_products=[Products(x) for x in settings.BANKING_PRODUCTS],
        )
        try:
            response = client.sandbox_public_token_create(request)
            test_public_token = response.public_token
            print(f"generated public token: {test_public_token}")
        except plaid.ApiException as e:
            print(f"Error creating sandbox token: {e}")
        return request


class AccessTokenCreate(PlaidBaseView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        public_token = request.data.get('public_token')

        api_request = ItemPublicTokenExchangeRequest(public_token)

        api_response = client.item_public_token_exchange(api_request)

        print(api_response)

        access_token = api_response['access_token']
        institution_id = api_response['institution_id']
        institution = Institution.objects.create(user=self.request.user, item_id=institution_id, access_token=access_token)
        institution.save()

        data = {
            "access_token": access_token,
            "institution_id": institution.institution_id
        }

        return Response(data, status=status.HTTP_200_OK)
