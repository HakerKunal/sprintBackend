import logging
from django.contrib import auth
from django.http import HttpResponse
from .models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer
from .utils import EncodeDecodeToken, EmailService

logging.basicConfig(filename="user.log", filemode="w")


class Registration(APIView):
    def post(self, request):
        """
        Will be Used to Create or Add the User into User Table
        :return:Response
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.create(validated_data=serializer.data)
            token = EncodeDecodeToken.encode_token(user.id)
            user.is_verified = True
            # EmailService.send_mail_for_verification(name=user, to=user.email, token=token)

            return Response({"message": "User Registration Successful"}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logging.error("Validation failed")
            return Response(
                {
                    "message": "validation failed",
                    "error": e.detail
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error("storing failed")
            return Response(
                {
                    "message": "User Registration Unsuccessful",
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = auth.authenticate(username=username, password=password)
            if not user:
                return Response(
                    {
                        "message": "Login Unsuccessful!!!"
                    },
                    status=status.HTTP_404_NOT_FOUND)

            if user.is_verified is False:
                return Response(
                    {
                        "message": "Login Unsuccessful!!! Please Verify yourself by clicking on the link sent to you"
                    },
                    status=status.HTTP_401_UNAUTHORIZED)
            token = EncodeDecodeToken.encode_token(payload=user.id)

            return Response(
                {
                    "message": "Login Successful",
                    "token": token,
                    "is_superuser": user.is_superuser,

                },
                status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(
                {
                    "message": "Authentication Fail",
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)


class ValidateToken(APIView):
    def get(self, request, token):

        """
         use to validate the user and verify the user
            :param request:
            :param token:
            :return:Response

        """
        try:

            decoded_token = EncodeDecodeToken.decode_token(token=token)
            user = User.objects.get(id=decoded_token.get('user_id'))
            user.is_verified = True
            user.save()

            return HttpResponse("User Verified")
        except Exception as e:
            logging.error(e)
            return HttpResponse(e)
