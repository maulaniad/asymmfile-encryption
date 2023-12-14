import random
import math

# Declare functions to be used throughout the apps.

def generate_prime() -> int:
    """
    Generates a random prime number from a predefined list.

    Note:
        This function can be extended to efficiently generate larger prime numbers.

    Returns:
        int: A randomly chosen prime number.
    """

    # Fungsi ini dapat diperluas untuk menghasilkan bilangan prima yang lebih besar secara efisien
    return random.choice([
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
        43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
    ])


def generate_keypair(p: int = generate_prime(),
                     q: int = generate_prime()) -> tuple:
    """
    Generates a key pair for RSA encryption and decryption.

    Args:
        p (int): A prime number (optional, default is generated randomly).
        q (int): A prime number (optional, default is generated randomly).

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]: A tuple containing the public key (e, n)
        and the private key (d, n).
    """

    # Memilih bilangan prima acak
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


def encrypt(message: str | list, public_key: tuple) -> list:
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


def decrypt(ciphertext: str | list, private_key: tuple) -> str:
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


if __name__ == '__main__':
    public_key, private_key = generate_keypair()
    message = "armanda.surya97@gmail.com"

    user = "armanda.surya97@gmail.com"

    # Enkripsi pesan
    encrypted_message = encrypt(message, public_key)
    print(f"Pesan terenkripsi: {encrypted_message}")
    print(type(encrypted_message))

    # Dekripsi pesan
    decrypted_message = decrypt(encrypted_message, private_key)
    print(f"Pesan terdekripsi: {decrypted_message}")

    if decrypted_message == user:
        print("Pesan sesuai text")
    else:
        print("pesan tidak sesuai")
