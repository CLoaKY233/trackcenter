import setuptools
from setuptools import setup, find_packages

setup(
    name='trackcenters',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django-crispy-forms',
        'django-bootstrap4',
        'django-allauth',
        'django-countries',
        'asgiref'
        'dj-database-url'
        'Django'
        'django-heroku'
        'et-xmlfile'
        'gunicorn'
        'openpyxl'
        'packaging'
        'psycopg2'
        'setuptools'
        'sqlparse'
        'typing_extensions'
        'tzdata'
        'whitenoise'      
    ],
    entry_points={
        'console_scripts': [
            'trackcenter = trackcenter.manage:main',
        ],
    },
)