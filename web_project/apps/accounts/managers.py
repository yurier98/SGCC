from django.db.models import Manager, QuerySet


class UserProfileQuerySet(QuerySet):
    def prepare_ids_query_param(self):
        return f"ARRAY[{', '.join(map(str, self.values_list('pk', flat=True)))}]::INTEGER[]"


class UserProfileManager(Manager.from_queryset(UserProfileQuerySet)):
    pass
