from ast import literal_eval

from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import render
from django.views import View

from helpers.types import FileStatus
from helpers.functions import rsa_decrypt, decrypt_file, write_bytes_to_file
from database.models import RSAKeyPair

# Create your views here.

class DataDecrypt(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'data_decrypt.html')

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse | FileResponse:
        file = request.POST.get('file_input', None)
        secret_key = request.POST.get('secret_key', None)
        key_list = request.POST.get('key', None)

        if not key_list or not file:
            return render(request, 'data_decrypt.html')

        key_sequences = key_list.split(',')
        key_stripped = tuple(int(key.strip()) for key in key_sequences)

        try:
            rsa = RSAKeyPair.objects.get(private_key=key_stripped)
        except RSAKeyPair.DoesNotExist:
            return render(request, 'data_decrypt.html', {'error': "Key does not match with any registered Key Pairs"})

        tupled_private_key: tuple = literal_eval(rsa.private_key)
        formed_secret_key = rsa.file.secret_key.strip().replace("[", "").replace("]", "")
        formed_secret_key = [int(key) for key in formed_secret_key.split(",")]

        real_key = rsa_decrypt(formed_secret_key, tupled_private_key)  # type: ignore
        if real_key != secret_key:
            return render(request, 'data_decrypt.html', {'error': "Passphrase does not match the expected value"})

        if rsa.file.status == FileStatus.ENCRYPTED.value:
            aes_key_bytes = literal_eval(rsa.file.aes_key)
            initial_vector_bytes = literal_eval(rsa.file.vector)
            decrypted_file = decrypt_file(rsa.file.file.file, aes_key_bytes, initial_vector_bytes)  # type: ignore
            write_bytes_to_file(decrypted_file, rsa.file.file.path)
            rsa.file.status = FileStatus.DECRYPTED  # type: ignore
            rsa.file.save()

        my_decryption_attempts = request.session.get('decryption_attempts', 0)
        request.session['decryption_attempts'] = my_decryption_attempts + 1

        file_to_return = open(rsa.file.file.path, 'rb')
        return FileResponse(file_to_return, as_attachment=True, filename="decrypted_file.pdf")
