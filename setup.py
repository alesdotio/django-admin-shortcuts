from setuptools import setup, find_packages
import os

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Framework :: Django",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Topic :: Software Development",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
]

setup(
    author="Ales Kocjancic",
    author_email="alesdotio@gmail.com",
    name='django-admin-shortcuts',
    version='1.0',
    description='Add simple and pretty shortcuts to the django admin homepage.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://github.com/alesdotio/django-admin-shortcuts',
    packages=find_packages(),
    include_package_data = True,
    zip_safe = False,
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.2',
    ],
)

