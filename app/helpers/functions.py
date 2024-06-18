import math
import os
import random
import string

from django.core.files.base import File, ContentFile

from helpers.aes import AES

# Declare functions to be used throughout the apps.

def is_prime(n: int) -> bool:
    """
    Check if a number is prime.

    Args:
        n (int): The number to check.

    Returns:
        bool: True if the number is prime, False otherwise.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def generate_prime(lower: int = 2, upper: int = 50_000) -> int:
    """
    Generates a random prime number from a predefined list.

    Note:
        This function can be extended to efficiently generate larger prime numbers.

    Returns:
        int: A randomly chosen prime number.
    """
    if lower > upper:
        raise ValueError("Lower bound must be less than or equal to upper bound.")

    prime_candidate = random.randint(lower, upper)
    while not is_prime(prime_candidate):
        prime_candidate = random.randint(lower, upper)

    return prime_candidate


def generate_keypair(p: int | None = None, q: int | None = None) -> tuple:
    """
    Generates a key pair for RSA encryption and decryption. If no params provided, generates random prime numbers.
    If the provided params are not prime, generates new random prime numbers.

    Args:
        p (int, optional): A prime number. Defaults to None.
        q (int, optional): A prime number. Defaults to None.

    Returns:
        tuple: A tuple containing the public key (e, n) and the private key (d, n).
    """

    if p is None or q is None:
        p = 1
        q = 1

    if not is_prime(p) or not is_prime(q):
        p = generate_prime()
        q = generate_prime()

    n = p * q

    # Menghitung totient, phi(n) = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Pilih kunci publik e yang saling prima dengan phi
    e = choose_public_key(phi)

    # Hitung kunci privat d > e * d = 1 (mod phi)
    d = mod_inverse(e, phi)

    # Kunci publik (e, n) kunci privat: (d, n)
    return ((e, n), (d, n))


def choose_public_key(phi: int) -> int:
    """
    Chooses a random integer 'e' that is coprime with 'phi'.

    Args:
        phi (int): Euler's totient function value for the modulus 'n'.

    Returns:
        int: The chosen public key 'e'.
    """

    # Pilih bilangan acak yang saling prima dengan phi
    e = random.randrange(1, phi)

    while math.gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    return e


def mod_inverse(a: int, m: int) -> int:
    """
    Calculates the modular inverse of 'a' modulo 'm' using the Extended Euclidean Algorithm.

    Args:
        a (int): The integer for which the modular inverse is to be calculated.
        m (int): The modulus.

    Returns:
        int: The modular inverse of 'a' modulo 'm'.
    """

    # Hitung invers modulo menggunakan Algoritma Extended Euclidean
    m0, x0, x1 = m, 0, 1

    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0

    return x1 + m0 if x1 < 0 else x1


def rsa_encrypt(message: str | list, public_key: tuple) -> list:
    """
    Encrypts the given message using the provided public key.

    Args:
        message (str): The plaintext message to be encrypted.
        public_key (Tuple[int, int]): The public key tuple (e, n) used for encryption.

    Returns:
        List[int]: A list of encrypted values representing the ciphertext.
    """

    e, n = public_key

    # Enkripsi menggunakan kunci publik
    return [pow(ord(char), e, n) for char in message]


def rsa_decrypt(ciphertext: str | list, private_key: tuple) -> str:
    """
    Decrypts the given ciphertext using the provided private key.

    Args:
        ciphertext (str): The encrypted text to be decrypted.
        private_key (Tuple[int, int]): The private key tuple (d, n) used for decryption.

    Returns:
        str: The decrypted text.
    """

    d, n = private_key

    # Dekripsi menggunakan kunci privat
    decrypted_characters = [pow(int(char), d, n) for char in ciphertext]
    decrypted_text = ''.join([chr(char) for char in decrypted_characters])

    return decrypted_text


def generate_random_chars(type: object = str, length: int = 8) -> str | bytes:
    if type == str:
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(length)
        )

    return os.urandom(length)


def open_file(file: File | str | bytes, size: int | None = None) -> bytes:
    """
    Opens and reads a file, returning its contents as bytes.

    Args:
        file (File | str | bytes): The file to be opened and read. It can be a file-like object, a file path, or bytes.
        size (int | None): The maximum number of bytes. Defaults to None, which means the entire file will be read.

    Returns:
        bytes: The contents of the file as bytes.

    Raises:
        FileNotFoundError: If the file specified by `file` does not exist.
        TypeError: If `file` is not a file-like object, a file path, or bytes.

    Example:
        >>> with open('example.txt', 'rb') as f:
        ...     contents = open_file(f)
        ...     print(contents)
        b"This is an example file."
    """
    if isinstance(file, File):
        f = file.open(mode="rb")

        if size:
            file_content = f.read(size)
        else:
            file_content = f.read()

        f.close()
        return file_content

    with open(file, 'rb') as f:
        if size:
            return f.read(size)
        return f.read()


def write_bytes_to_file(data: bytes, file_path: str):
    with open(file_path, 'wb') as f:
        f.write(data)

    return ContentFile(data, name=file_path.split("/")[-1])


def encrypt_file(file: File | str | bytes, key: bytes, initial_vector: bytes) -> bytes:
    """
    Encrypts a file using AES encryption with CBC mode.

    Args:
        file (File | str | bytes): The file to encrypt. It can be a file-like object, a file path, or raw bytes.
        key (bytes): The encryption key.
        initial_vector (bytes): The initial vector for encryption.

    Returns:
        bytes: The encrypted ciphertext.

    Raises:
        None

    Examples:
        >>> encrypt_file('path/to/file.txt', b'secret_key', b'initial_vector')
        b'encrypted_data'
    """
    if isinstance(file, bytes):
        plaintext = file
    else:
        plaintext = open_file(file)

    aes = AES(key)

    ciphertext = aes.encrypt_cbc(plaintext, initial_vector)
    return ciphertext


def decrypt_file(file: File | str | bytes, key: bytes, initial_vector: bytes):
    """
    Decrypts a file using AES encryption with CBC mode and returns the plaintext data.

    Args:
        file (File | str | bytes): The file to decrypt.
        key (bytes): The encryption key.
        initial_vector (bytes): The initial vector for decryption.

    Returns:
        The decrypted plaintext data.
    """

    if isinstance(file, bytes):
        ciphertext = file
    else:
        ciphertext = open_file(file)

    aes = AES(key)

    plaintext = aes.decrypt_cbc(ciphertext, initial_vector)
    return plaintext


if __name__ == '__main__':
    public_key, private_key = generate_keypair()
    message = "hello_world"

    user = "hello_world"

    # Enkripsi pesan RSA
    encrypted_message = rsa_encrypt(message, public_key)
    print(f"Pesan terenkripsi: {encrypted_message}")
    print(type(encrypted_message))

    # Dekripsi pesan RSA
    decrypted_message = rsa_decrypt(encrypted_message, private_key)
    print(f"Pesan terdekripsi: {decrypted_message}")

    if decrypted_message == user:
        print("Pesan sesuai text")
    else:
        print("pesan tidak sesuai")
