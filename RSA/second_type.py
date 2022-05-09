import random
import sympy
import ast


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


def check_prime(p):
    if p < 2:
        raise ValueError(p, 'is not a prime number')

    for i in range(2, p):
        if p % i == 0:
            raise ValueError(p, 'is not a prime number')
        else:
            return p


def generate_keypair(p, q):
    n = p * q
    phi = ((p - 1) * (q - 1))

    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher


def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)


def save(filename, msg):
    with open(filename, 'w') as f:
        f.write(msg)


def read(filename):
    with open(filename, 'r') as f:
        r = f.readlines()
    x = ast.literal_eval(r[0])
    x = [int(i) for i in x]
    return x


qs = input('Do you want to enter p and q, if no they will be randomly generated? (y/n) ')

if qs == 'y':
    n1 = input('Enter p: ')
    p = check_prime(int(n1))
    n2 = input('Enter q: ')
    q = check_prime(int(n2))
else:
    p = sympy.randprime(1, 100)
    q = sympy.randprime(1, 100)

public, private = generate_keypair(p, q)
print('Public key:', public, '\nPrivate key:', private)
x = input("Type message: ")

encrypted_msg = encrypt(public, x)
save('encrypted_msg.txt', str(encrypted_msg))

r = read('encrypted_msg.txt')
quest = 'Do you want to decrypt message? (y/n)'
if input(quest) == 'y':
    print(f"decrypting {r}")

print(f"Decrypted Message is : {decrypt(private, r)}")
