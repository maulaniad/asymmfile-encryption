from datetime import datetime, timedelta
from io import BytesIO
from json import loads, dumps
from os import listdir, path
from typing import Any

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View

from weasyprint import HTML

from database.forms import LoginForm, RegisterForm
from database.models import File, RSAKeyPair, User, FormatData, Data

from helpers.types import FileStatus
from helpers.functions import (generate_random_chars,
                               generate_keypair,
                               encrypt_file,
                               rsa_encrypt,
                               write_bytes_to_file)

# Create your views here.

class SessionCorrector(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            if request.session['is_loggedin']:
                request.session['user_id']

            return redirect(to="/dashboard/")
        except KeyError:
            return redirect(to="/login/")


class Login(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="login.html"
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = LoginForm(request.POST)

        if not form.is_valid():
            return redirect(to="/login/?login_status=BAD")

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user_data = User.objects.filter(
            Q(begin_date__lte=datetime.now()),
            Q(end_date__gte=datetime.now()),
            Q(username=username) | Q(email=username)
        ).first()

        if not user_data:
            return redirect(to="/login/?login_status=USER_DOES_NOT_EXIST")

        if not check_password(password=password, encoded=user_data.password):
            return redirect(to="/login/?login_status=WRONG_PASSWORD")

        request.session['user_id'] = user_data.id
        request.session['email'] = user_data.email
        request.session['fullname'] = user_data.fullname
        request.session['username'] = user_data.username
        request.session['is_loggedin'] = True

        return redirect(to="/dashboard/")


class Register(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="register.html"
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return redirect(to="/login/?register_status=BAD")

        email = form.cleaned_data['email']
        fullname = form.cleaned_data['fullname']
        username = form.cleaned_data['username']
        password = make_password(form.cleaned_data['password'])

        user_data = User(
            email=email,
            fullname=fullname,
            username=username,
            password=password
        )

        user_data.save()

        return redirect(to="/login/?register_status=OK")


class Logout(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        request.session.pop('user_id', None)
        request.session.pop('email', None)
        request.session.pop('username', None)
        request.session.pop('fullname', None)
        request.session.flush()

        return redirect(to="/login/")


class Dashboard(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        my_decryption_attempts = request.session.get('decryption_attempts', 0)
        registered_accounts = User.objects.all().count()
        data_formats = FormatData.objects.all()

        data_format_counts: list[dict[str, Any]] = []
        for data_format in data_formats:
            data_count = Data.objects.filter(
                format_id=data_format.id
            ).count()

            data_format_counts.append({
                'name': data_format.format_name,
                'count': data_count
            })

        current_month_files = []
        for file in listdir(settings.MEDIA_ROOT):
            file_date = path.getctime(path.join(settings.MEDIA_ROOT, file))
            readable_date = datetime.fromtimestamp(file_date).date()
            if readable_date.month == datetime.now().month:
                current_month_files.append(file)

        previous_month_files = []
        for file in listdir(settings.MEDIA_ROOT):
            file_date = path.getctime(path.join(settings.MEDIA_ROOT, file))
            readable_date = datetime.fromtimestamp(file_date).date()
            if readable_date.month == (datetime.now() - timedelta(days=30)).month:
                previous_month_files.append(file)

        previous_month_files_count = len(previous_month_files)
        current_month_files_count = len(current_month_files)

        if previous_month_files_count == 0:
            growth_percentage = 0.0
        else:
            growth_percentage = (
                (current_month_files_count - previous_month_files_count) / previous_month_files_count * 100
            )

        return render(
            request=request,
            template_name="dashboard.html",
            context={
                'my_decryption_attempts': my_decryption_attempts,
                'registered_accounts': registered_accounts,
                'data_format_counts': data_format_counts,
                'prev_month_files_count': previous_month_files_count,
                'curr_month_files_count': current_month_files_count,
                'growth_percentage': float(f"{growth_percentage:.2f}")
            }
        )


class MasterData(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        format_id = request.GET.get('format', None)

        data_formats = FormatData.objects.filter(
            end_date__gte=datetime.now()
        )

        if not format_id:
            context = {'data_formats': data_formats}
            return render(request=request, template_name="master_data.html", context=context)

        data = Data.objects.filter(
            end_date__gte=datetime.now(),
            format=data_formats.get(id=format_id)
        )

        selected_format = {
            key: value for key, value in
            data_formats.get(id=format_id).__dict__.items()
            if key not in ['_state']
        }

        fields_json: list[dict[str, Any]] = loads(selected_format['fields'])
        selected_format['fields'] = []
        for field in fields_json:
            for key, _ in field.items():
                selected_format['fields'].append(key)

        data_list = []
        for x in data:
            x_json: list[dict[str, Any]] = loads(x.data)
            for y in x_json:
                data_list.append(y)

        context = {
            'format_id': format_id,
            'data_formats': data_formats,
            'selected_format': selected_format,
            'data': data_list
        }
        return render(request=request, template_name="master_data.html", context=context)


class GeneratePDF(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        format_id = kwargs.get('format_id', None)
        secret_key = kwargs.get('key', None)

        data_formats = FormatData.objects.filter(end_date__gte=datetime.now())
        data = Data.objects.filter(
            end_date__gte=datetime.now(),
            format=data_formats.get(id=format_id)
        )

        selected_format = {
            key: value for key, value in
            data_formats.get(id=format_id).__dict__.items()
            if key not in ['_state']
        }

        fields_json: list[dict[str, Any]] = loads(selected_format['fields'])
        selected_format['fields'] = []
        for field in fields_json:
            for key, _ in field.items():
                selected_format['fields'].append(key)

        data_list = []
        for x in data:
            x_json: list[dict[str, Any]] = loads(x.data)
            for y in x_json:
                data_list.append(y)

        context = {
            'format_id': format_id,
            'data_formats': data_formats,
            'selected_format': selected_format,
            'data': data_list,
            'date': datetime.now()
        }
        html = render_to_string(template_name="pdf/download.html", context=context)
        pdf = HTML(string=html).write_pdf(resolution=300)

        if not pdf:
            return HttpResponse('Error generating PDF')

        pdf_file = BytesIO(pdf)

        memory_pdf_file = InMemoryUploadedFile(
            file=pdf_file,
            field_name=None,
            name=f"{selected_format['format_name']}_encrypted.pdf",
            content_type="application/pdf",
            size=int(pdf_file.getbuffer().nbytes / 1024),
            charset=None
        )

        public_key, private_key = generate_keypair()
        aes_key = generate_random_chars(type=bytes, length=16)
        initial_vector = generate_random_chars(type=bytes, length=16)

        file = File.objects.create(
            file=memory_pdf_file,
            filename=f"{selected_format['format_name']}_encrypted.pdf",
            aes_key=aes_key,
            vector=initial_vector,
            secret_key=rsa_encrypt(secret_key, public_key),
            format=data_formats.get(id=format_id),
            status=FileStatus.ENCRYPTED
        )

        RSAKeyPair.objects.create(
            private_key=private_key,
            public_key=public_key,
            file=file
        )

        file_encrypted = encrypt_file(
            file.file.file,
            key=file.aes_key,                   # type: ignore
            initial_vector=initial_vector       # type: ignore
        )

        write_bytes_to_file(file_encrypted, file.file.path)
        response = HttpResponse(
            content=dumps({
                'private_key': private_key,
                'public_key': public_key,
                'filename': file.file.name
            }),
            content_type="application/json",
            status=200
        )
        return response


class DownloadFile(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        filename = kwargs.get('filename', None)
        file = File.objects.get(file=filename)

        return FileResponse(file.file, as_attachment=True)
