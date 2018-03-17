import copy
import inspect

from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

try:
    from django.utils.module_loading import import_module
except ImportError:
    from django.utils.importlib import import_module

register = template.Library()


@register.inclusion_tag('admin_shortcuts/base.html', takes_context=True)
def admin_shortcuts(context):
    if 'ADMIN_SHORTCUTS' in context:
        admin_shortcuts = copy.deepcopy(context['ADMIN_SHORTCUTS'])
    else:
        admin_shortcuts = copy.deepcopy(getattr(settings, 'ADMIN_SHORTCUTS', None))
    admin_shortcuts_settings = copy.deepcopy(getattr(settings, 'ADMIN_SHORTCUTS_SETTINGS', None))
    request = context.get('request', None)
    if not admin_shortcuts:
        return {}

    for group in admin_shortcuts:
        if not group.get('shortcuts'):
            raise ImproperlyConfigured('settings.ADMIN_SHORTCUTS is improperly configured.')

        if group.get('title'):
            group['title'] = ugettext(group['title'])

        enabled_shortcuts = []
        for shortcut in group.get('shortcuts'):
            if shortcut.get('has_perms'):
                if not eval_func(shortcut['has_perms'], request):
                    continue

            if not shortcut.get('url'):
                try:
                    url_name = shortcut['url_name']
                except KeyError:
                    raise ImproperlyConfigured(_('settings.ADMIN_SHORTCUTS is improperly configured. '
                                                 'Please supply either a "url" or a "url_name" for each shortcut.'))
                current_app = shortcut.get('app_name')
                if isinstance(url_name, list):
                    shortcut['url'] = reverse(url_name[0], args=url_name[1:], current_app=current_app)
                else:
                    shortcut['url'] = reverse(url_name, current_app=current_app)

                shortcut['url'] += shortcut.get('url_extra', '')

            if not shortcut.get('icon'):
                shortcut['icon'] = get_shortcut_class(shortcut.get('url_name', shortcut.get('url', ''))+shortcut.get('title', ''))

            if shortcut.get('count'):
                shortcut['count'] = eval_func(shortcut['count'], request)

            if shortcut.get('count_new'):
                shortcut['count_new'] = eval_func(shortcut['count_new'], request)

            if shortcut.get('title'):
                shortcut['title'] = ugettext(shortcut['title'])

            enabled_shortcuts.append(shortcut)

        group['shortcuts'] = enabled_shortcuts

    return {
        'admin_shortcuts': admin_shortcuts,
        'settings': admin_shortcuts_settings,
    }


@register.inclusion_tag('admin_shortcuts/style.css')
def admin_shortcuts_css():
    return {}


@register.inclusion_tag('admin_shortcuts/js.html')
def admin_shortcuts_js():
    admin_shortcuts_settings = getattr(settings, 'ADMIN_SHORTCUTS_SETTINGS', None)
    return {
        'settings': admin_shortcuts_settings,
    }


def eval_func(func_path, request):
    try:
        module_str = '.'.join(func_path.split('.')[:-1])
        func_str = func_path.split('.')[-1:][0]
        module = import_module(module_str)
        result = getattr(module, func_str)
        if callable(result):
            args, varargs, keywords, defaults = inspect.getargspec(result)
            if 'request' in args:
                result = result(request)
            else:
                result = result()
        return result
    except:
        return func_path


@register.simple_tag
def admin_static_url():
    """
    If set, returns the string contained in the setting ADMIN_MEDIA_PREFIX, otherwise returns STATIC_URL + 'admin/'.
    """
    return getattr(settings, 'ADMIN_MEDIA_PREFIX', None) or ''.join([settings.STATIC_URL, 'admin/'])


DEFAULT_ICON = getattr(settings, 'ADMIN_SHORTCUTS_DEFAULT_ICON', 'cog')


def get_shortcut_class(text=''):
    text = text.lower()
    icon_weights = {}
    max_weight = 0
    for keywords, icon in CLASS_MAPPINGS:
        weight = sum([1 if k in text else 0 for k in keywords])
        icon_weights[icon] = weight
        if weight > max_weight:
            max_weight = weight
    best_icon_matches = []
    for icon, weight in icon_weights.items():
        if weight == max_weight:
            best_icon_matches.append(icon)
    if len(best_icon_matches):
        return best_icon_matches[0]
    return DEFAULT_ICON


CLASS_MAPPINGS = getattr(settings, 'ADMIN_SHORTCUTS_CLASS_MAPPINGS', [
    [['home'], 'home'],
    [['add'], 'plus'],
    [['logout', 'login'], 'lock'],
    [['file'], 'file'],
    [['page', 'text'], 'file-alt'],
    [['image', 'picture', 'photo', 'gallery'], 'image'],
    [['product', 'store'], 'shopping-cart'],
    [['order', 'pay', 'sale', 'income', 'revenue'], 'money-bill-alt'],
    [['category'], 'archive'],
    [['user', 'account'], 'user'],
    [['group', 'team'], 'users'],
    [['address', 'contacts'], 'address-book'],
    [['message', 'contact', 'mail'], 'envelope'],
    [['folder', 'directory', 'path'], 'folder'],
    [['blog', 'book'], 'book'],
    [['event', 'calendar'], 'calendar'],
    [['delivery', 'shipping'], 'truck'],
    [['add'], 'plus'],
    [['change', 'edit'], 'edit'],
    [['home'], 'home'],
])
