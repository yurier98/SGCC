import os
import typing
from datetime import datetime, date

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


def conform_trace_value(trace):
    trace = trace.replace("File", "<br><b>Archivo</b>")
    trace = trace.replace("line", "<b>Línea</b>")
    trace = trace.replace(" in ", " <b>específicamente en:</b> ")
    if os.environ.get("XIPAC_ENV", "DEV") == "PROD":
        splitted_by_br = trace.split("<br>")
        last = splitted_by_br[-1]
        splitted_by_colon = last.split(",")
        file = splitted_by_colon[0]
        line = splitted_by_colon[1]
        specific_in_line = splitted_by_colon[2]
        trace = "%s<br>%s, %s" % (file, line, specific_in_line)
    return trace


def get_remote_ip(request_info):
    """
    :param request_info:
    :return:
    """
    import socket

    return request_info.get(
        "HTTP_X_FORWARDED_FOR",
        request_info.get("HTTP_X_REAL_IP", socket.gethostbyname(socket.gethostname())),
    )


def extract_params_from_post_put_request(request):
    meta = request.META
    request_method = meta["REQUEST_METHOD"]
    params = None
    if request_method in ["POST", "PUT"]:
        if request.body:
            params = request.body.decode()
    return params


def m2m_or_related_value_treatment(instance, field_name, lookup_name="name"):
    meta = instance._meta
    for m2m_or_related in meta.many_to_many + meta.related_objects:
        if m2m_or_related.name == field_name:
            return list(
                getattr(instance, field_name).all().values_list(lookup_name, flat=True)
            )
    return ""


"""
Convert django.db.models.Model instance and all related ForeignKey, ManyToManyField and @property function fields into dict.
Usage:
    class MyDjangoModel(... PrintableModel):
        to_dict_fields = (...)
        to_dict_exclude = (...)
        ...
    a_dict = [inst.to_dict(fields=..., exclude=...) for inst in MyDjangoModel.objects.all()]
"""


class PrintableModel(models.Model):
    class Meta:
        abstract = True

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(
        self,
        fields: typing.Optional[typing.Iterable] = None,
        exclude: typing.Optional[typing.Iterable] = None,
    ):
        opts = self._meta
        data = {}

        # support fields filters and excludes
        if not fields:
            fields = set()
        else:
            fields = set(fields)
        default_fields = getattr(self, "to_dict_fields", set())
        fields = fields.union(default_fields)

        if not exclude:
            exclude = set()
        else:
            exclude = set(exclude)
        default_exclude = getattr(self, "to_dict_exclude", set())
        exclude = exclude.union(default_exclude)

        # support syntax "field__childField__..."
        self_fields = set()
        child_fields = dict()
        if fields:
            for i in fields:
                splits = i.split("__")
                if len(splits) == 1:
                    self_fields.add(splits[0])
                else:
                    self_fields.add(splits[0])

                    field_name = splits[0]
                    child_fields.setdefault(field_name, set())
                    child_fields[field_name].add("__".join(splits[1:]))

        self_exclude = set()
        child_exclude = dict()
        if exclude:
            for i in exclude:
                splits = i.split("__")
                if len(splits) == 1:
                    self_exclude.add(splits[0])
                else:
                    field_name = splits[0]
                    if field_name not in child_exclude:
                        child_exclude[field_name] = set()
                    child_exclude[field_name].add("__".join(splits[1:]))

        for f in opts.concrete_fields + opts.many_to_many:
            if self_fields and f.name not in self_fields:
                continue
            if self_exclude and f.name in self_exclude:
                continue

            # Este cambio es nuestro (sipac team) para poder tener un nombre de campo más descriptivo...
            field_name = opts.get_field(f.name).verbose_name or f.name
            humanized_value = self.get_humanized_values().get(f.name, None)

            if humanized_value:
                # Este cambio es nuestro (sipac team). Priorizando el valor "humanized"...
                data[field_name] = humanized_value
            elif isinstance(f, models.ManyToManyField):
                if self.pk is None:
                    data[field_name] = []
                else:
                    result = []
                    m2m_inst = f.value_from_object(self)
                    for obj in m2m_inst:
                        if isinstance(obj, PrintableModel) and hasattr(obj, "to_dict"):
                            # d = obj.to_dict(
                            #     fields=child_fields.get(f.name),
                            #     exclude=child_exclude.get(f.name),
                            # )

                            # Este cambio es nuestro (sipac team). Solo necesitamos la descripción...
                            d = str(obj)
                        else:
                            # d = django.forms.models.model_to_dict(
                            #     obj,
                            #     fields=child_fields.get(f.name),
                            #     exclude=child_exclude.get(f.name)
                            # )

                            # Este cambio es nuestro (sipac team). Solo necesitamos la descripción...
                            d = str(obj)
                        result.append(d)
                    data[field_name] = result
            elif isinstance(f, models.ForeignKey):
                if self.pk is None:
                    data[field_name] = []
                else:
                    data[field_name] = None
                    try:
                        foreign_inst = getattr(self, f.name)
                    except ObjectDoesNotExist:
                        pass
                    else:
                        if isinstance(foreign_inst, PrintableModel) and hasattr(
                            foreign_inst, "to_dict"
                        ):
                            # data[field_name] = foreign_inst.to_dict(
                            #     fields=child_fields.get(f.name),
                            #     exclude=child_exclude.get(f.name)
                            # )

                            # Este cambio es nuestro (sipac team). Solo necesitamos la descripción...
                            data[field_name] = str(foreign_inst)
                        elif foreign_inst is not None:
                            # data[field_name] = django.forms.models.model_to_dict(
                            #     foreign_inst,
                            #     fields=child_fields.get(f.name),
                            #     exclude=child_exclude.get(f.name),
                            # )

                            # Este cambio es nuestro (sipac team). Solo necesitamos la descripción...
                            data[field_name] = str(foreign_inst)

            elif isinstance(f, (models.DateTimeField, models.DateField)):
                v = f.value_from_object(self)
                if v is not None:
                    # Este cambio es nuestro (sipac team). Convirtiendo los valores de tipo fecha en texto...
                    data[field_name] = value_treatment(v)  # .isoformat()
                else:
                    data[field_name] = None
            else:
                data[field_name] = f.value_from_object(self)

        # support @property decorator functions
        #
        # Este cambio es nuestro (sipac team). Por ahora no nos interesa llevar una traza de los campos "decorados"...
        #
        # decorator_names = get_decorators_dir(self.__class__)
        # for name in decorator_names:
        #     if self_fields and name not in self_fields:
        #         continue
        #     if self_exclude and name in self_exclude:
        #         continue
        #
        #     value = getattr(self, name)
        #     if isinstance(value, PrintableModel) and hasattr(value, "to_dict"):
        #         data[name] = value.to_dict(
        #             fields=child_fields.get(name), exclude=child_exclude.get(name)
        #         )
        #     elif hasattr(value, "_meta"):
        #         # make sure it is a instance of django.db.models.fields.Field
        #         data[name] = model_to_dict(
        #             value,
        #             fields=child_fields.get(name),
        #             exclude=child_exclude.get(name),
        #         )
        #     elif isinstance(value, (set,)):
        #         data[name] = list(value)
        #     else:
        #         data[name] = value

        return data

    def get_humanized_values(self):
        return {}
