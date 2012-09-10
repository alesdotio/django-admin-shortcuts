from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from importlib import import_module

register = template.Library()

CLASS_MAPPINGS = getattr(settings, 'ADMIN_SHORTCUTS_CLASS_MAPPINGS', [
    ['cms_page', 'pages'],
    ['product', 'product'],
    ['order', 'order'],
    ['category', 'category'],
    ['user', 'user'],
    ['folder', 'folder'],
    ['gallery', 'gallery'],
    ['blog', 'blog'],
    ['event', 'event'],
    ['mail', 'mail'],
    ['message', 'mail'],
    ['contact', 'mail'],
    ['location', 'location'],
    ['store', 'location'],
    ['add', 'add'],
    ['change', 'change'],
])


@register.inclusion_tag('admin_shortcuts/base.html')
def admin_shortcuts():
    admin_shortcuts = getattr(settings, 'ADMIN_SHORTCUTS', None)
    admin_shortcuts_settings = getattr(settings, 'ADMIN_SHORTCUTS_SETTINGS', None)

    if not admin_shortcuts:
        return ''

    for group in admin_shortcuts:
        if not group.get('shortcuts'):
            raise ImproperlyConfigured('settings.ADMIN_SHORTCUTS is improperly configured.')
        for shortcut in group.get('shortcuts'):
            if not shortcut.get('url'):
                try:
                    url_name = shortcut['url_name']
                except KeyError:
                    raise ImproperlyConfigured(_('settings.ADMIN_SHORTCUTS is improperly configured. '
                                                  'Please supply either a "url" or a "url_name" for each shortcut.'))
                if isinstance(url_name, list):
                    shortcut['url'] = reverse(url_name[0], args=url_name[1:])
                else:
                    shortcut['url'] = reverse(url_name)

                shortcut['url'] += shortcut.get('url_extra', '')

            if not shortcut.get('class'):
                shortcut['class'] = get_shortcut_class(shortcut.get('url_name', shortcut['url']))

            if shortcut.get('count'):
                shortcut['count'] = eval_func(shortcut['count'])

            if shortcut.get('count_new'):
                shortcut['count_new'] = eval_func(shortcut['count_new'])

    return {
        'admin_shortcuts': admin_shortcuts,
        'settings': admin_shortcuts_settings,
    }


@register.inclusion_tag('admin_shortcuts/style.css')
def admin_shortcuts_css():
    return {
        'classes': [value for key, value in CLASS_MAPPINGS],
    }


@register.inclusion_tag('admin_shortcuts/js.html')
def admin_shortcuts_js():
    admin_shortcuts_settings = getattr(settings, 'ADMIN_SHORTCUTS_SETTINGS', None)
    return {
        'settings': admin_shortcuts_settings,
    }


def eval_func(func_path):
    try:
        module_str = '.'.join(func_path.split('.')[:-1])
        func_str = func_path.split('.')[-1:][0]
        module = import_module(module_str)
        result = getattr(module, func_str)()
        return result
    except:
        return func_path


def get_shortcut_class(url):
    if url == '/':
        return 'home'
    for key, value in CLASS_MAPPINGS:
        if key in url:
            return value
    return ''


