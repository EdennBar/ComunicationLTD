import hashlib
import secrets
import os
import MySQLdb
from django.shortcuts import render,redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .forms import RegisterForm,CustomerForm
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages

@csrf_exempt
def index(request):
    return render(request, 'core/index.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
            MYSQL_USER = os.environ.get("MYSQL_USER", "root")
            MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
            MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "mydb")
            MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")

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

            # Check if the user exists
            cursor.execute("SELECT * FROM communication.users_users WHERE email=%s", (email,))
            user = cursor.fetchone()
            print("please print the user " + str(user))

            # If the user exists, check the password
            if user:
                salt = str(user[10])
                print(f"password: {password}")
                print(f"salt: {salt}")
                print("Reached password comparison block")
                hashed_password = hashlib.pbkdf2_hmac(
                    'sha256',
                    bytes(password, 'utf-8'),
                    bytes(salt, 'utf-8'),
                    100000
                ).hex()
                print(f"hashed password: {hashed_password}")
                print(f"stored password: {str(user[6])}")
                if hashed_password == user[6]:
                    # Close the database connection and cursor
                    cursor.close()
                    conn.close()
                    messages.success(request, 'Login successful!')
                    return redirect('login') # we can redirect to the home page after login,we see the message login... 
                    #return HttpResponse('Login successful!')// we have the option to get the respone 200
                else:
                    # Close the database connection and cursor
                    cursor.close()
                    conn.close()
                    messages.error(request, 'Incorrect password.')
                    #return redirect('login')
                    return HttpResponse('Incorrect password.', status=400)
            else:
                # Close the database connection and cursor
                cursor.close()
                conn.close()
                messages.error(request, 'User does not exist.')
                #return redirect('login') 
                return HttpResponse('User does not exist.', status=400)

        except Exception as error:
            print(error)
            return HttpResponseBadRequest("Error connecting to database")

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
                cursor.execute("INSERT INTO communication.users_users (first_name, last_name, email,password,salt ,is_superuser, is_staff, is_active, date_joined) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)",
                (first_name, last_name, email, hashed_password,salt ,False, False, True, now))





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



def password_change(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        new_password_again = request.POST.get('new_password_again')


        try:
            MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
            MYSQL_USER = os.environ.get("MYSQL_USER", "root")
            MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
            MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "mydb")
            MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")

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

            # Check if the user exists
            cursor.execute("SELECT * FROM communication.users_users WHERE email=%s", (email,))
            user = cursor.fetchone()
            print("please print the user " + str(user))

            # If the user exists, check the password
            if user:
                salt = str(user[10])
                print(f"password: {password}")
                print(f"salt: {salt}")
                print("Reached password comparison block")
                hashed_password = hashlib.pbkdf2_hmac(
                    'sha256',
                    bytes(password, 'utf-8'),
                    bytes(salt, 'utf-8'),
                    100000
                ).hex()
                print(f"hashed password: {hashed_password}")
                print(f"stored password: {str(user[6])}")
                if hashed_password == user[6]:
                    if new_password == new_password_again:
                        # Generate a random salt
                        salt = secrets.token_hex(16)
                        # Combine the salt and password and hash them using HMAC-SHA256
                        hashed_password = hashlib.pbkdf2_hmac(
                        'sha256',
                        bytes(new_password, 'utf-8'),
                        bytes(salt, 'utf-8'),
                        100000
                        ).hex()

                    
                        cursor.execute("UPDATE communication.users_users SET password=%s WHERE email=%s",(new_password,email))
                        # Close the database connection and cursor
                        cursor.close()
                        conn.close()
                        messages.success(request, 'Password changed successfully')
                        return redirect('password_change') # we can redirect to the home page after login,we see the message login... 
                        #return HttpResponse('Login successful!')// we have the option to get the respone 200
                    else:
                        # Close the database connection and cursor
                        cursor.close()
                        conn.close()
                        messages.error(request, 'Passwords do not match')
                        return HttpResponse('Passwords do not match', status=400)
                else:
                    # Close the database connection and cursor
                    cursor.close()
                    conn.close()
                    messages.error(request, 'Incorrect password.')
                    return HttpResponse('Incorrect password.', status=400)
            else:
                # Close the database connection and cursor
                cursor.close()
                conn.close()
                messages.error(request, 'User does not exist.')
                return HttpResponse('User does not exist.', status=400)

        except Exception as error:
            print(error)
            return HttpResponseBadRequest("Error connecting to database")

    return render(request, 'core/password_change.html')


def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')
            phone = form.cleaned_data.get('phone')


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
                # Execute the SQL statement with the parameters
                cursor.execute("INSERT INTO communication.customers_customers (name, address, phone) VALUES (%s,%s, %s)",
                (name,address,phone))

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
        form = CustomerForm()
    return render(request, 'core/customers.html', {'form': form})

def customers_list(request):
    if request.method == 'GET':
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
                # Execute the SQL statement with the parameters
                cursor.execute("SELECT * FROM communication.customers_customers;")
                customers = cursor.fetchall()
                cursor.close()
                conn.close()
                return render(request, 'core/customers_list.html', {'customers': customers})
        except Exception as error:
                print(error)
                return HttpResponseBadRequest("Error connecting to database")
