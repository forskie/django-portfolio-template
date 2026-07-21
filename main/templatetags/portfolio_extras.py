from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_STROKE = 'fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"'

_ICONS = {
    "github": f'<svg viewBox="0 0 24 24" {_STROKE}><path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.7 2.8 5.6 3.1 5.6 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4.2 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.1-.5 2V21"/></svg>',
    "linkedin": f'<svg viewBox="0 0 24 24" {_STROKE}><path d="M6.5 8.5v9M6.5 5.5v.01M11 17.5v-5c0-1.7 1-3 2.8-3 1.8 0 2.7 1.3 2.7 3v5"/><path d="M11 12.5v5"/></svg>',
    "telegram": f'<svg viewBox="0 0 24 24" {_STROKE}><path d="M21 4 3 11.5l6 2m12-9.5-3.5 16L9 15m12-11L9 15m0 0-.5 5.5L11 17"/></svg>',
    "email": f'<svg viewBox="0 0 24 24" {_STROKE}><path d="M4 6h16v12H4z"/><path d="m4 7 8 6 8-6"/></svg>',
    "phone": f'<svg viewBox="0 0 24 24" {_STROKE}><path d="M6 3h3l1.5 5-2.3 1.5a11 11 0 0 0 5.3 5.3L15 12.5l5 1.5v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4 5.2 2 2 0 0 1 6 3Z"/></svg>',
    "whatsapp": f'<svg viewBox="0 0 24 24" {_STROKE}><path d="M4 20l1.4-4A8 8 0 1 1 9 18.6L4 20Z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5"/></svg>',
    "website": f'<svg viewBox="0 0 24 24" {_STROKE}><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18Z"/></svg>',
    "resume": f'<svg viewBox="0 0 24 24" {_STROKE}><path d="M12 4v11m0 0-3.5-3.5M12 15l3.5-3.5"/><path d="M5 16v3a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-3"/></svg>',
    "external": f'<svg viewBox="0 0 24 24" {_STROKE}><path d="M9 6H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-3"/><path d="M14 4h6v6M20 4l-9 9"/></svg>',
    "link": f'<svg viewBox="0 0 24 24" {_STROKE}><path d="M9 15l6-6M8 13l-2 2a3.5 3.5 0 0 0 5 5l2-2M16 11l2-2a3.5 3.5 0 0 0-5-5l-2 2"/></svg>',
}


@register.filter
def icon_svg(key):
    return mark_safe(_ICONS.get(key, _ICONS["link"]))