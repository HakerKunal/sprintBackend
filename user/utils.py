import jwt
from django.core.mail import send_mail
from sprintvotingapp import settings


class EncodeDecodeToken:
    """
    for Encoding and decoding the userid into token
    """

    @staticmethod
    def encode_token(payload):

        encoded_token = jwt.encode({"user_id": payload},
                                   "secret",
                                   algorithm="HS256"
                                   )
        return encoded_token

    @staticmethod
    def decode_token(token):
        decoded_token = jwt.decode(token,
                                   "secret",
                                   algorithms="HS256"
                                   )
        return decoded_token


class EmailService:
    """
    Used for sending Email bor verification purpose

    """

    @staticmethod
    def send_mail_for_verification(to, token, name):
        send_mail(
            subject='Welcome to Sprint Run Voting Application ',
            message='Hy {}\n Welcome to Sprint Run Voting Application please click on below URL for Verification\n '
                    'Your Activation link = http://127.0.0.1:8000/user/validate/{}'.format(
                name,
                token),
            from_email=settings.EMAIL_HOST, recipient_list=[to]
        )
