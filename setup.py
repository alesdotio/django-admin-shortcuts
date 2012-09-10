from setuptools import setup, find_packages
import os

CLASSIFIERS = []

setup(
    author="Ales Kocjancic",
    author_email="alesdotio@gmail.com",
    name='django-admin-shortcuts',
    version='1.0',
    description='Add simple and pretty shortcuts to the django admin homepage.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='http://github.com/alesdotio',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.2',
    ],
    packages=find_packages(exclude=["example", "example.*"]),
    zip_safe = False
)

