import hashlib
import os
import secrets

import MySQLdb
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from dotenv import load_dotenv
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Users
from .serializers import UsersSerializer, ChangePasswordSerializer, RegisterSerializer

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = os.getenv("MYSQL_PORT")


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "success",
            "code": 0
        })


class UsersViewset(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users.objects.all()

    def create(self, request, *args, **kwargs):
        print(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        headers = self.get_success_headers(serializer.validated_data)

        validated_data = serializer.validated_data
        print(validated_data)
        password = validated_data.get('password')  # get password from validated data
        print(password)

        try:
            validate_password(password)
        except ValidationError as e:
            # If the password is not valid, return a response with the error message
            return Response({'password': e.messages}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.save_data_to_db(serializer)
        headers = self.get_success_headers(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def save_data_to_db(self, serializer):
        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        print(first_name)
        print(last_name)
        print(email)
        try:
            print(MYSQL_USER)

            # Open a connection to the MySQL database
            conn = MySQLdb.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                port=int(MYSQL_PORT)
            )
            # Create a new cursor object to execute SQL statements
            cursor = conn.cursor()

            # Generate a random salt
            salt = secrets.token_hex(16)

            # Combine the salt and password and hash them using HMAC-SHA256
            hashed_password = hashlib.pbkdf2_hmac(
                'sha256',
                bytes(password, 'utf-8'),
                bytes(salt, 'utf-8'),
                100000
            ).hex()
            print(hashed_password)
            serializer.validated_data['password'] = hashed_password
            # Construct the SQL statement to insert the validated data into the register table
            sql = "INSERT INTO communication.users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
            params = (first_name, last_name, email, hashed_password)

            # Execute the SQL statement with the parameters
            cursor.execute(sql, params)

            # Commit the changes to the database
            conn.commit()

            # Close the database connection and cursor
            cursor.close()
            conn.close()
        except Exception as error:
            print(error)
        serializer.save()
