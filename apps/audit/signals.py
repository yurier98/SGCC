""" Audit signals """

import json
from uuid import UUID
from datetime import date, datetime

from django.db.models import ImageField
from django.db.models.fields.files import FieldFile
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile

from .middleware import TracingMiddleware
from .models import BaseModel, Rule, Trace

""" Util function """
# User = get_user_model()

def prepare(dict_object):
    for key in dict_object:
        value = dict_object[key]
        if isinstance(value, date):
            dict_object[key] = value.strftime("%m/%d/%Y")
        elif isinstance(value, datetime):
            dict_object[key] = value.strftime("%m/%d/%Y %H:%M:%S")
        elif isinstance(value, list):
            dict_object[key] = tuple(value)
        elif value and (isinstance(value, FieldFile) or isinstance(value, ImageField)):
            value = (
                value.url
                if hasattr(value, "url")
                else value.path
                if hasattr(value, "path")
                else ""
            )
            dict_object[key] = value
        elif not value:
            dict_object[key] = ""
    return dict_object


def get_diff(instance, created):
    presave = TracingMiddleware.get_data()
    postsave = prepare(model_to_dict(instance))
    diff = {key: value for key, value in postsave.items() - presave.items()}
    diff = postsave if created else diff

    # Convertir UUID a cadenas para poderlo pasar despues como un json
    for key, value in diff.items():
        if isinstance(value, UUID):
            diff[key] = str(value)

    # Devolver resultado como JSON
    return json.dumps(diff)


"""Signals for reload rules"""
@receiver(post_save, sender=Rule)
def save_rule(sender, **kwargs):
    TracingMiddleware.reload_rules()


@receiver(post_delete, sender=Rule)
def delete_rule(sender, **kwargs):
    TracingMiddleware.reload_rules()


""" Signal for presave instance """

@receiver(pre_save)
def presave_log(sender, instance, **kwargs):
    try:
        presave = sender.objects.get(pk=instance.pk)
        data = prepare(model_to_dict(presave))
    except sender.DoesNotExist:
        data = {}
    TracingMiddleware.set_data(data)


""" Signal for postsave instance """
@receiver(post_save)
def save_log(sender, instance, created, **kwargs):
    rule = TracingMiddleware.get_rule_by_classname(sender._meta.model_name)
    if not rule:
        return
    diff = get_diff(instance, created)
    if not diff:
        return
    info = TracingMiddleware.get_info()
    try:
        name = str(instance)
    except:
        name = "%s (%s)" % (instance._meta.verbose_name.capitalize(), instance.id)


    options = {
        "name": name,
        "message": diff,
        "content_object": instance,
        "user": info.get("user"),
        "ip": info.get("ip"),
        "os": info.get("os"),
    }
    if created and rule.get("check_create"):
        options["action"] = Trace.ActionChoices.CREATE
    elif not created and rule.get("check_edit"):
        options["action"] = Trace.ActionChoices.EDIT
    else:
        return
    Trace.objects.create(**options)


""" Signal for post_delete instance """
@receiver(post_delete)
def save_delete(sender, instance, **kwargs):
    rule = TracingMiddleware.get_rule_by_classname(sender._meta.model_name)
    if not rule:
        return
    if rule.get("check_delete"):
        try:
            name = str(instance)
        except:
            name = "%s (%s)" % (instance._meta.verbose_name.capitalize(), instance.id)
        message = prepare(model_to_dict(instance))
        info = TracingMiddleware.get_info()
        try:
            name = str(instance)
        except:
            name = "%s (%s)" % (instance._meta.verbose_name.capitalize(), instance.id)
        options = {
            "name": name,
            "action": Trace.ActionChoices.DELETE,
            "message": json.dumps(message),
            "content_object": instance,
            "user": info.get("user"),
            "ip": info.get("ip"),
            "os": info.get("os"),
        }
        Trace.objects.create(**options)


@receiver(post_save)
def save_user_in_base_model(sender, instance, created, **kwargs):
    """Save audit fields"""
    if not issubclass(sender, BaseModel):
        return

    # Disconect signals
    pre_save.disconnect(presave_log)
    post_save.disconnect(save_log)
    post_save.disconnect(save_user_in_base_model)

    # Update user
    user = TracingMiddleware.get_info().get("user", None)
    user = user.username if user else "root"
    if created:
        instance.created_user = user
    instance.modified_user = user
    instance.save()

    # Reconnect sigals
    post_save.connect(save_user_in_base_model)
    post_save.connect(save_log)
    pre_save.connect(presave_log)
