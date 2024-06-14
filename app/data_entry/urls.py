from django.urls import path

from data_entry.views import DataEntry, FormatDataEntry


urlpatterns = [
    path('', DataEntry.as_view(), name='data_entry'),
    path('create_format/', FormatDataEntry.as_view(), name='create_format'),
]
