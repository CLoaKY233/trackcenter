import setuptools
from setuptools import setup, find_packages

setup(
    name='trackcenters',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django',
        'gunicorn',
        'dj-database-url',
        'psycopg2',
        'whitenoise',
        'django-heroku',
        'django-crispy-forms',
        'django-bootstrap4',
        'django-allauth',
        'django-countries',
    ],
    entry_points={
        'console_scripts': [
            'trackcenter = trackcenter.manage:main',
        ],
    },
)