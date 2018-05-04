from setuptools import setup, find_packages
from codecs import open
import os

from admin_shortcuts import version


setup(
    name='django-admin-shortcuts',
    author='Ales Kocjancic',
    author_email='alesdotio@gmail.com',
    version=version,
    description='Add simple and pretty shortcuts to the django admin homepage.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://github.com/alesdotio/django-admin-shortcuts',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    install_requires=[
        'Django>=1.2',
    ],
    download_url='https://github.com/alesdotio/django-admin-shortcuts/tarball/' + version,
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='',
)
