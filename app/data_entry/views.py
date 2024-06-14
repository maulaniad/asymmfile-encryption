from datetime import datetime
from json import loads
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from database.models import Data, FormatData
from helpers.types import FormatDataEntryPayload

# Create your views here.

class DataEntry(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        format_data_query = FormatData.objects.filter(end_date__gte=datetime.now())
        data_query = Data.objects.filter(
            end_date__gte=datetime.now(),
            format__in=format_data_query
        )

        data_format_list: list[dict[str, Any]] = []

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

            data_format_list.append(format_dict)

        data_list = [
            {
                'id': data.id,
                'name': data.name,
                'format': data.format.id,
                'begin_date': data.begin_date.strftime('%Y-%m-%d'),
                'end_date': data.end_date.strftime('%Y-%m-%d'),
                'data': loads(data.data)
            } for data in data_query
        ]

        context = {
            'data_formats': data_format_list,
            'data': data_list
        }
        return render(request, 'data_entry.html', context=context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        post_data = request.POST.copy()
        post_data.pop('csrfmiddlewaretoken')

        format_id = post_data.pop('format')
        format_data = FormatData.objects.get(id=format_id[0])

        Data.objects.create(
            format=format_data,
            data=[post_data],
        )

        return redirect(to="data_entry:data_entry")


class FormatDataEntry(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'data_entry_format.html')

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        data: FormatDataEntryPayload = loads(request.body)

        FormatData.objects.create(
            format_name=data['format_name'],
            fields=data['fields']
        )

        return redirect(to="data_entry:data_entry")
