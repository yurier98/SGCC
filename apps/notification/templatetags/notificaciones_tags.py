from django import template

register = template.Library()


@register.filter()
def cantNotify(context):
    user = user_context(context)

    if not user:
        return ''

    return user.notifications.unread().count()


notifications = register.simple_tag(takes_context=True)(cantNotify)


def user_context(context):
    if 'user' not in context:
        return None

    request = context['request']
    user = request.user

    try:

        user_is_anonymous = user.is_anonymous()
    except TypeError:
        user_is_anonymous = user.is_anonymous

    if user_is_anonymous:
        return None

    return user


@register.filter()
def Notify(context):
    user = user_context(context)

    if not user:
        return ''

    return user.notifications.unread()[0:5]


Notify = register.simple_tag(takes_context=True)(Notify)
