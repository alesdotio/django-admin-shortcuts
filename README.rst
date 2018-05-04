======================
Django Admin Shortcuts
======================

.. image:: https://raw.github.com/alesdotio/django-admin-shortcuts/gh-pages/images/django-admin-shortcuts.png



What is this?
=============

It's a simple dashboard app that adds shortcuts to your Django admin homepage. The keyword here is SIMPLE!


Why does it exist?
==================

Because some people noted that it's sometimes hard to find the app you are looking for on the admin homepage.

"So why don't we customize the admin site a bit?"

"Nah, I don't want to go through all the hassle of editing templates or setting up a complex dashboard app ..."

Well, good thing django-admin-shortcuts is here, because it only takes five minutes of your time to go from the old
dreadfully boring admin to the marvelous engineering excellence that is this app.


How do I use it?
================

1) ``pip install django-admin-shortcuts``

2) add ``'admin_shortcuts'`` to your ``INSTALLED_APPS``, just before ``'django.contrib.admin'`` **<-- IMPORTANT**

3) add ``ADMIN_SHORTCUTS`` to your settings

    For example:
::

    ADMIN_SHORTCUTS = [
        {
            'title': 'Authentication',
            'shortcuts': [
                {
                    'title': 'Groups',
                    'url_name': 'admin:auth_group_changelist',
                    'count': 'example.utils.count_groups',
                },
                {
                    'title': 'Add user',
                    'url_name': 'admin:auth_user_add',
                    'has_perms': 'example.utils.has_perms_to_users',
                },
            ]
        },
    ]

Where ...

* required ``url_name`` is a name that will be resolved using Django's reverse url method (see Django docs https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#admin-reverse-urls )
* optional ``app_name`` is the name of the admin app that will be used for URL reversal. You can safely ignore this if you have only one admin site in your ``urls.py``
* optional ``url`` is a direct link that will override ``url_name``
* optional ``url_extra`` is extra stuff to be attached at the end of the url (like GET data for pre-filtering admin views)
* optional ``title`` is the title of the shortcut
* optional ``count`` and ``count_new`` are paths to a function inside your project that returns something interesting (like a count of all products or a count of all pending orders).
  The function can optionally take one argument, ``request``, which is the current Django ``HttpRequest`` object.
* optional ``has_perms`` is a path to a function inside your project that returns information about shortcut visibility on the django admin homepage.
  Like above, this function can optionally take one argument ``request`` as well.
* optional ``open_new_window`` sets whether the link should open in a new window (default is False)
* optional ``icon`` is a Font Awesome Solid https://fontawesome.com/icons?d=gallery&s=solid icon class (if you don't specify one, magical ponies will do it for you)

4) profit!!

5) optionally, also add ``ADMIN_SHORTCUTS_SETTINGS`` to your settings

::

    ADMIN_SHORTCUTS_SETTINGS = {
        'show_on_all_pages': False,
        'hide_app_list': False,
        'open_new_window': False,
    }


Where ...

* optional ``show_on_all_pages`` shows the shortcuts on all admin pages
* optional ``hide_app_list`` collapses the app list
* optional ``open_new_window`` makes all shortcuts open in a new window


What are the settings used in the pretty image above?
=====================================================

::

    ADMIN_SHORTCUTS = [
        {
            'shortcuts': [
                {
                    'url': '/',
                    'open_new_window': True,
                },
                {
                    'url_name': 'admin:logout',
                },
                {
                    'title': 'Users',
                    'url_name': 'admin:auth_user_changelist',
                    'count': 'example.utils.count_users',
                },
                {
                    'title': 'Groups',
                    'url_name': 'admin:auth_group_changelist',
                    'count': 'example.utils.count_groups',
                },
                {
                    'title': 'Add user',
                    'url_name': 'admin:auth_user_add',
                    'has_perms': 'example.utils.has_perms_to_users',
                },
            ]
        },
        {
            'title': 'CMS',
            'shortcuts': [
                {
                    'title': 'Pages',
                    'url_name': 'admin:index',
                },
                {
                    'title': 'Files',
                    'url_name': 'admin:index',
                },
                {
                    'title': 'Contact forms',
                    'icon': 'columns',
                    'url_name': 'admin:index',
                    'count_new': '3',
                },
                {
                    'title': 'Products',
                    'url_name': 'admin:index',
                },
                {
                    'title': 'Orders',
                    'url_name': 'admin:index',
                    'count_new': '12',
                },
            ]
        },
    ]
    ADMIN_SHORTCUTS_SETTINGS = {
        'show_on_all_pages': True,
        'hide_app_list': True,
        'open_new_window': False,
    }



I want to change how stuff looks
================================

* to change the CSS overwrite the ``templates/admin_shortcuts/base.css`` template
* to change the which icons are magically selected specify the mappings in ``ADMIN_SHORTCUTS_CLASS_MAPPINGS``

