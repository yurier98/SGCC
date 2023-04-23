from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

#
# @register.filter()
# def cantNotify(context):
#     user = user_context(context)
#
#     if not user:
#         return ''
#
#     return user.notificaciones.no_leido().count()
#
# notificaciones = register.simple_tag(takes_context=True)(cantNotify)
#
