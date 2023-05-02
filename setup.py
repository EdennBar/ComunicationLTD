from setuptools import setup

setup(
    name='secure-ltd',
    version='0.0.1',
    install_requires=[
        "django",
        "django-rest-framework",
        "python-dotenv",
        "mysqlclient",
        "drf_yasg",
        "django-cors-headers",
        "django-password-validators",
        "django-sslserver",
        "django-rest-passwordreset~=1.3.0",
    ],
)
