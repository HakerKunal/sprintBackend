import pytest, json
from rest_framework.reverse import reverse
from ..models import User


@pytest.mark.django_db
class TestUser:
    def test_user_registration(self, client):
        # test case create their own database to test the views
        url = reverse("registration")
        user = {
            "username": "kunal123",
            "password": "kunal123",
            "email": "kunalbatham15@gmail.com",
            "first_name": "kunal",
            "last_name": "batham",
        }


        response = client.post(url, user)

        assert response.status_code == 201

    def test_user_registration_wrong_username(self, client):
        # test username with wrong regex
        url = reverse("registration")
        user = {
            "username": "kun",
            "password": "kuanl123",
            "email": "kunalbatham15@gmail.com",
            "first_name": "kunal",
            "last_name": "batham",
        }
        response = client.post(url, user)
        assert response.status_code == 400

    def test_user_registration_blank_username(self, client):
        # test case for blank username
        url = reverse("registration")
        user = {
            "username": "",
            "password": "root",
            "email": "kunalbatham15@gmail.com",
            "first_name": "kunal",
            "last_name": "batham",
        }
        response = client.post(url, user)
        assert response.status_code == 400

    def test_user_login_is_verified(self, client):
        user = User.objects.create_user(username="root123",
                                        password="root123",
                                        email="kunalbatham15@gmail.com",
                                        first_name="kunal",
                                        last_name="batham",
                                        is_verified="True"
                                        )
        user.save()
        data = {
            "username": "root123",
            "password": "root123",
        }
        url = reverse("login")
        response = client.post(url, data)
        assert response.status_code == 200

    def test_user_login_is_not_verified(self, client):
        user = User.objects.create_user(username="root123",
                                        password="root123",
                                        email="kunalbatham15@gmail.com",
                                        first_name="kunal",
                                        last_name="batham",

                                        )
        user.save()
        data = {
            "username": "root123",
            "password": "root123",
        }
        url = reverse("login")
        response = client.post(url, data)
        assert response.status_code == 401

    def test_user_login_wrong_user_id(self, client):
        user = User.objects.create_user(username="root123",
                                        password="root123",
                                        email="kunalbatham15@gmail.com",
                                        first_name="kunal",
                                        last_name="batham",
                                        )
        user.save()
        data = {
            "username": "root",
            "password": "root123",
        }
        url = reverse("login")
        response = client.post(url, data)
        assert response.status_code == 404

    def test_user_login_wrong_password(self, client):
        user = User.objects.create_user(username="root123",
                                        password="root123",
                                        email="kunalbatham15@gmail.com",
                                        first_name="kunal",
                                        last_name="batham",
                                        )
        user.save()
        data = {
            "username": "root123",
            "password": "adwd",
        }
        url = reverse("login")
        response = client.post(url, data)
        assert response.status_code == 404
