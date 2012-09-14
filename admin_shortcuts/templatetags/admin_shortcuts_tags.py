import copy
from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from importlib import import_module

register = template.Library()


@register.inclusion_tag('admin_shortcuts/base.html')
def admin_shortcuts():
    admin_shortcuts = copy.deepcopy(getattr(settings, 'ADMIN_SHORTCUTS', None))
    admin_shortcuts_settings = copy.deepcopy(getattr(settings, 'ADMIN_SHORTCUTS_SETTINGS', None))

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


@register.simple_tag
def admin_static_url():
    """
    If set, returns the string contained in the setting ADMIN_MEDIA_PREFIX, otherwise returns STATIC_URL + 'admin/'.
    """
    return getattr(settings, 'ADMIN_MEDIA_PREFIX', None) or ''.join([settings.STATIC_URL, 'admin/'])


def get_shortcut_class(url):
    if url == '/':
        return 'home'
    for key, value in CLASS_MAPPINGS:
        if key is not None and key in url:
            return value
    return 'config' # default icon


CLASS_MAPPINGS = getattr(settings, 'ADMIN_SHORTCUTS_CLASS_MAPPINGS', [
    ['cms_page', 'file2'],
    ['product', 'basket'],
    ['order', 'cash'],
    ['category', 'archive'],
    ['user', 'user'],
    ['account', 'user'],
    ['address', 'letter'],
    ['folder', 'folder'],
    ['gallery', 'picture'],
    ['blog', 'blog'],
    ['event', 'date'],
    ['mail', 'openmail'],
    ['message', 'openmail'],
    ['contact', 'openmail'],
    ['location', 'pin'],
    ['store', 'pin'],
    ['delivery', 'delivery2'],
    ['shipping', 'delivery2'],
    ['add', 'plus'],
    ['change', 'pencil'],
    ['home', 'home'],

    # extra classes
    [None, 'archive'],
    [None, 'back'],
    [None, 'camera'],
    [None, 'card'],
    [None, 'cd'],
    [None, 'certificate'],
    [None, 'clock'],
    [None, 'cloud1'],
    [None, 'cloud2'],
    [None, 'cloud3'],
    [None, 'cloud4'],
    [None, 'config'],
    [None, 'config2'],
    [None, 'date'],
    [None, 'delivery1'],
    [None, 'diskette'],
    [None, 'file1'],
    [None, 'file3'],
    [None, 'file4'],
    [None, 'film'],
    [None, 'flag'],
    [None, 'gamepad'],
    [None, 'garbage'],
    [None, 'gift'],
    [None, 'help'],
    [None, 'key'],
    [None, 'less'],
    [None, 'letters'],
    [None, 'light'],
    [None, 'lock'],
    [None, 'love'],
    [None, 'mail'],
    [None, 'monitor'],
    [None, 'music'],
    [None, 'note'],
    [None, 'notepad'],
    [None, 'ok'],
    [None, 'package'],
    [None, 'phone'],
    [None, 'pin'],
    [None, 'print'],
    [None, 'sound'],
    [None, 'suitcase'],
    [None, 'tag'],
    [None, 'ticket'],
    [None, 'tool'],
    [None, 'unlock'],
    [None, 'wallet'],
    [None, 'warning'],
    [None, 'way'],
    [None, 'zoom'],
])
