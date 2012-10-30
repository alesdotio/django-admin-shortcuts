======================
django Admin Shortcuts
======================

.. image:: http://alesdotio.github.com/django-admin-shortcuts/images/django-admin-shortcuts.png



What is this?
=============

It's a simple dashboard app that adds shortcuts to your django admin homepage. The keyword here is SIMPLE!


Why does it exist?
==================

Because some people noted that it's sometimes hard to find the app you are looking for on the admin homepage.

"So why don't we customize the admin site a bit?"

"Nah, I don't want to go through all the hassle of editing templates or setting up a complex dashboard app ..."

Well, good thing django-admin-shortcuts is here, because it only takes five minutes of your time to go from the old
dreadfully boring admin to the marvelous engineering excellence that is this app.


How do i use it?
================

1) ``pip install django-admin-shortcuts``

2) add ``'admin_shortcuts'`` to your ``INSTALLED_APPS``, just before ``'django.contrib.admin'`` <-- IMPORTANT

3) add ``ADMIN_SHORTCUTS`` to your settings

    For example:
::

    ADMIN_SHORTCUTS = [
        {
            'title': 'Shop',
            'shortcuts': [
                {
                    'url_name': 'admin:shop_order_changelist',
                    'title': 'Products',
                    'count_new': 'project.utils.count_new_orders',
                },
            ]
        },
    ]

Where ...

    * ``url_name`` is a name that will be resolved using django's reverse url method (see https://docs.djangoproject.com/en/1.4/ref/contrib/admin/#reversing-admin-urls)
    * optional ``app_name`` is the name of the admin app that will be used for URL reversal. You can safely ignore this if you have only one admin site in your ``urls.py``
    * optional ``url`` is a direct link that will override ``url_name``
    * optional ``url_extra`` is extra stuff to be attached at the end of the url (like GET data for pre-filtering admin views)
    * optional ``title`` is the title of the shortcut
    * optional ``count`` and ``count_new`` are paths to a function inside your project that returns something interesting (like a count of all products or a count of all pending orders).
      The function can optionally take one argument, ``request``, which is the current Django ``HttpRequest`` object.
    * optional ``open_new_window`` sets whether the link should open in a new window (default is False)
    * optional ``class`` is the CSS class to be added to the anchor element (if you don't specify one, magical ponies will do it for you)

4) profit!!

5) optionally, also add ``ADMIN_SHORTCUTS_SETTINGS`` to your settings

::

    ADMIN_SHORTCUTS_SETTINGS = {
        'hide_app_list': False,
        'open_new_window': False,
    }


Where ...

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
                    'url_name': 'admin:cms_page_changelist',
                    'title': _('Pages'),
                },
                {
                    'url_name': 'admin:filer_folder_changelist',
                    'title': _('Files'),
                },
                {
                    'url_name': 'admin:auth_user_changelist',
                    'title': _('Users'),
                },
                {
                    'url_name': 'admin:contactform_contactformsubmission_changelist',
                    'title': _('Contact forms'),
                    'count_new': 'project.utils.count_new_contactforms',
                },
            ]
        },
        {
            'title': _('Shop'),
            'shortcuts': [
                {
                    'url_name': 'admin:shop_product_changelist',
                    'title': _('Products'),
                    'count': 'project.utils.count_products',
                },
                {
                    'url_name': 'admin:shop_category_changelist',
                    'title': _('Categories'),
                },
                {
                    'url_name': 'admin:shop_order_changelist',
                    'title': _('Orders'),
                    'count_new': 'project.utils.count_new_orders',
                },
            ]
        },
    ]
    ADMIN_SHORTCUTS_SETTINGS = {
        'hide_app_list': True,
        'open_new_window': False,
    }



I want to change how stuff looks
================================

* to change the css overwrite the ``templates/admin_shortcuts/base.css`` template
* to change the icons specify desired ``url_name`` to ``class`` mappings in ``ADMIN_SHORTCUTS_CLASS_MAPPINGS``


Notes
-----

* Icons grabbed from Pixeden.com

