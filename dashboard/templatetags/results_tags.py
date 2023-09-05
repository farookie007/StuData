from django import template


register = template.Library()


@register.filter
def get_level(result_id):
    l_limit = (result_id.endswith('E') and -1) or 0     # -1 if result_id endswith 'E', otherwise 0
    return result_id[-4:l_limit]


@register.filter
def get_sem_repr(code):
    """Gets the semester representation using its `code`"""
    return {
        '1': 'First',
        '2': 'Second',
        '3': 'Third',
    }.get(code)