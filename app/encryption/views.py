from django.shortcuts import render
import random
import math
# Create your views here.


def generate_keypair():
    # memilih bilangan prima acak
    p = generate_prime()
    q = generate_prime()
    print("p:" ,p)
    print("q:" ,q)
    n = p * q
    print("n:", n)
    # menghitung totient, phi(n) = (p-1)(q-1)
    phi = (p - 1) * (q - 1)
    print("phi", phi)
    
    # pilih kunci publik e yang saling prima dengan phi
    e = choose_public_key(phi)
    print("e:", e)

    # hitung kunci privat d > e * d = 1 (mod phi)
    d = mod_inverse(e, phi)
    print("d :", d)

    # kunci publik (e, n) kunci privat: (d, n)
    return((e, n), (d, n))

def generate_prime():
     # Fungsi ini dapat diperluas untuk menghasilkan bilangan prima yang lebih besar secara efisien
    return random.choice([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97])


def choose_public_key(phi):
    # Pilih bilangan acak yang saling prima dengan phi
    e = random.randrange(1, phi)
    while math.gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    print("e bil acak:", e)
    return e

def mod_inverse(a, m):
    # Hitung invers modulo menggunakan Algoritma Extended Euclidean
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def encrypt(message, public_key):
    e, n = public_key
    print("publick key:", public_key)
    # Enkripsi menggunakan kunci publik
    print("message", message)
    return [pow(ord(char), e, n) for char in message]


def decrypt(ciphertext, private_key):
    d, n = private_key
    print("private key:", private_key)
    # Dekripsi menggunakan kunci privat
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])


public_key, private_key = generate_keypair()
message = "armanda.surya97@gmail.com"

user = "adrian.maulani@sigma.co.id"
# user = "armanda.surya97@gmail.com"


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


