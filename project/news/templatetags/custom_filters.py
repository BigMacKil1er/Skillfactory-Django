from django import template

register = template.Library()

stop_words = [
    'словоисключение1',
    'словоисключение2',
    'словоисключение3',
]

@register.filter(name='censor')


def censor(value):

    for sw in stop_words:
        value = value.lower().replace(sw.lower(), '...')
    return value



@register.filter(name='preview')
def preview(value):
    if len(value) > 50:
        return value[:51] + '...'
    else:
        return value
