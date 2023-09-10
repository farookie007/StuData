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


@register.filter
def resolve_nan(field, replace):
    """Replaces `nan` in the fields with `replace` string."""
    return replace if ((str(field) == 'nan') or (field is None)) else field


@register.filter
def show_if_editable(course):
    """Adds the 'no-show' id attr to the element if it is editable."""
    return 'no-show' if 'nan' not in [str(x) for x in [course.ca, course.exam, course.total, course.grade]] else ''
