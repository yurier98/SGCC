import os

from django.db import models
from django.utils import timezone
from django.conf import settings

now = timezone.now()


def read_json_file(file_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(base_dir, file_name)

    with open(file_path, "r") as file:
        data = file.read()
    return data

    # try:
    #     with open(file_path, "r") as file:
    #         data = file.read()
    #     return data
    # except FileNotFoundError as e:
    #     # Manejo de excepciones: archivo no encontrado
    #     print(f"Error al leer el archivo: {e}")
    #     return None  # o realiza alguna otra acción apropiada en caso de error


# Obtiene la ubicación del archivo de plantilla de reportes desde la configuración
default_report_template_path = getattr(settings, "DEFAULT_REPORT_TEMPLATE_PATH",
                                       "resources/default_report_template.json")
# Lee el contenido del archivo JSON utilizando la función de utilidad
default_report_content = read_json_file(default_report_template_path)


# store report requests for testing, used by ReportBro Designer
# for preview of pdf and xlsx
class ReportRequest(models.Model):
    key = models.CharField(max_length=36)
    report_definition = models.TextField()
    data = models.TextField()
    is_test_data = models.BooleanField()
    pdf_file = models.BinaryField(null=True)
    pdf_file_size = models.IntegerField(null=True)
    created_on = models.DateTimeField()

    class Meta:
        db_table = 'report_request'


# report definition for our album report which is used for printing
# the pdf with the album list. When the report is saved
# in ReportBro Designer it will be stored in this table.
class ReportDefinition(models.Model):
    report_definition = models.TextField(default=default_report_content)
    report_type = models.CharField(max_length=100, unique=True)
    remark = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    last_modified_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = 'report_definition'

    def __str__(self):
        return self.report_type

    @property
    def recently_created(self) -> bool:
        return (timezone.now() - self.created_at) <= timezone.timedelta(days=5)
