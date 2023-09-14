import datetime
import xlwt
from django.core.exceptions import ObjectDoesNotExist
import xlrd
from django.conf import settings
import os
from main import models

HEADER_STYLE = xlwt.easyxf('font:bold on')
DEFAULT_STYLE = xlwt.easyxf()
CELL_STYLE_MAP = (
    (datetime.datetime, xlwt.easyxf(num_format_str="YYYY/MM/DD HH:MM")),
    (datetime.date, xlwt.easyxf(num_format_str='DD/MM/YYYY')),
    (datetime.time, xlwt.easyxf(num_format_str="HH:MM")),
)


def multi_getattr(obj, attr, default=None):
    attributes = attr.split(".")

    for i in attributes:
        try:
            if obj._meta.get_field(i).choices:
                obj = getattr(obj, f"get_{i}_display")()
            else:
                obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise

    return obj


def get_column_cell(obj, name):
    try:
        attr = multi_getattr(obj, name)
    except ObjectDoesNotExist:
        return None

    if hasattr(attr, '_meta'):
        return str(attr).strip()
    elif hasattr(attr, 'all'):
        return ', '.join(str(x).strip() for x in attr.all())

    if isinstance(attr, datetime.datetime):
        from django.utils.timezone import localtime
        attr = localtime(attr)
        attr = attr.replace(tzinfo=None)

    return attr


def queryset_to_workbook(queryset,
                         columns,
                         header_style=HEADER_STYLE,
                         default_style=DEFAULT_STYLE,
                         cell_style_map=CELL_STYLE_MAP):
    workbook = xlwt.Workbook()
    report_date = datetime.date.today()
    sheet_name = f"Export {report_date.strftime('%Y-%m-%d')}"
    sheet = workbook.add_sheet(sheet_name)

    for num, column in enumerate(columns.keys()):
        value = columns[column]
        sheet.write(0, num, value, header_style)

    for x, obj in enumerate(queryset, start=1):
        for y, column in enumerate(columns.keys()):
            value = get_column_cell(obj, column)
            style = default_style

            for value_type, cell_style in cell_style_map:
                if isinstance(value, value_type):
                    style = cell_style
                    break
            sheet.write(x, y, value, style)

    return workbook


def import_data():
    # data = request.FILES.get('data')
    book = xlrd.open_workbook(os.path.join(settings.BASE_DIR, "data.xls"))
    sheet = book.sheets()[0]
    for rx in range(1,sheet.nrows):
        row = sheet.row(rx)

        user = models.BaseUser.objects.create(
            first_name=row[1].value,
            last_name=row[2].value,
            middle_name=row[3].value,
            u_group=models.UserGroup.objects.get_or_create(name=str(row[4].value).strip())[0],
            username=row[6].value,
            is_student=True
        )
        user.set_password(row[7].value)
        user.save()

