import hashlib
import secrets
import os
import MySQLdb
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .forms import RegisterForm
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

@csrf_exempt
def index(request):
    return render(request, 'core/index.html')
def login(request):
    return render(request, 'core/login.html')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            # Validate the password
            try:
                validate_password(password)
            except ValidationError as e:
                form.add_error('password1', e)
                return HttpResponseBadRequest("Invalid Password")

            try:
                MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
                MYSQL_USER = os.environ.get("MYSQL_USER", "root")
                MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
                MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "mydb")
                MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")
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

                # Get the current time
                now = timezone.now()

                # Execute the SQL statement with the parameters
                cursor.execute("INSERT INTO communication.users_users (first_name, last_name, email, password, is_superuser, is_staff, is_active, date_joined) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (first_name, last_name, email, hashed_password, False, False, True, now))





                # Commit the changes to the database
                conn.commit()

                # Close the database connection and cursor
                cursor.close()
                conn.close()

                

                return HttpResponse("Success!")
            except Exception as error:
                print(error)
                return HttpResponseBadRequest("Error connecting to database")
        else:
            print(form.errors)
            return HttpResponseBadRequest("Invalid Form Data")
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})
