from datetime import datetime
from json import loads
from typing import Any

from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from database.models import Data, FormatData
from helpers.types import FormatDataEntryPayload

# Create your views here.

class DataEntry(View):
    def get(self, request, *args, **kwargs):
        format_data_query = FormatData.objects.filter(end_date__gte=datetime.now())
        data_query = Data.objects.filter(
            end_date__gte=datetime.now(),
            format__in=format_data_query
        )

        data_formats: list[dict[str, Any]] = []

        for format in format_data_query:
            fields: list[dict[str, Any]] = loads(format.fields)
            format_dict: dict[str, Any] = {
                'id': format.id,
                'format_name': format.format_name,
                'fields': []
            }

            for field in fields:
                for key, value in field.items():
                    format_dict['fields'].append({
                        key: value
                    })

            data_formats.append(format_dict)

        context = {
            'data_formats': data_formats,
            'data': data_query
        }
        return render(request, 'data_entry.html', context=context)


class FormatDataEntry(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        return render(request, 'data_entry_format.html')

    def post(self, request: HttpRequest, *args, **kwargs):
        data: FormatDataEntryPayload = loads(request.body)

        FormatData.objects.create(
            format_name=data['format_name'],
            fields=data['fields']
        )

        return render(request, 'data_entry.html')
