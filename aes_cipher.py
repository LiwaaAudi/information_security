import time

from Crypto.Cipher import AES
import hashlib
import sys
import binascii
import Padding

val = input('Enter Value: ') or 'hello'
password = input('Enter Pass: ') or 'hello'
ival = 15

MODE = input('choose block cipher mode of operation (ECB, CBC, CFB): ')

if len(sys.argv) > 1:
    val = sys.argv[1]

if len(sys.argv) > 2:
    password = str(sys.argv[2])

if len(sys.argv) > 3:
    ival = int(sys.argv[3])

plaintext = val


def encrypt(plaintext, key, mode):
    encobj = AES.new(key, mode)
    return encobj.encrypt(plaintext)


def decrypt(ciphertext, key, mode):
    encobj = AES.new(key, mode)
    return encobj.decrypt(ciphertext)


def encrypt2(plaintext, key, mode, iv):
    encobj = AES.new(key, mode, iv)
    return encobj.encrypt(plaintext)


def decrypt2(ciphertext, key, mode, iv):
    encobj = AES.new(key, mode, iv)
    return encobj.decrypt(ciphertext)


ENCR = open('encrypt.txt', 'w')
DECR = open('deccrypt.txt', 'w')


key = hashlib.sha256(password.encode()).digest()

iv = hex(ival)[2:8].zfill(16)

print("IV: " + iv)

plaintext = Padding.appendPadding(plaintext, blocksize=Padding.AES_blocksize, mode=0)
print("Input data (CMS): " + binascii.hexlify(plaintext.encode()).decode())

if MODE == 'ECB':
    ciphertext = encrypt(plaintext.encode(), key, AES.MODE_ECB)
    ENCR.write(binascii.hexlify(bytearray(ciphertext)).decode())

    a = input('Do you want to decrypt your saved cipher text in new file? y/n:')
    if a == 'y':
        READ = open('encrypt.txt', 'r').readlines()
        print('reading encrypt.txt and saving in decrypt.txt')
        time.sleep(2)
        plaintext = decrypt(READ, key, AES.MODE_ECB)
        plaintext = Padding.removePadding(plaintext.decode(), mode=0)
        DECR.write("  decrypt: " + plaintext)
        plaintext = val
        plaintext = Padding.appendPadding(plaintext, blocksize=Padding.AES_blocksize, mode=0)

elif MODE == 'CBC':
    ciphertext = encrypt2(plaintext.encode(), key, AES.MODE_CBC, iv.encode())
    ENCR.write(binascii.hexlify(bytearray(ciphertext)).decode())

    a = input('Do you want to decrypt your saved cipher text in new file? y/n:')
    if a == 'y':
        READ = open('encrypt.txt', 'r').readlines()
        print('reading encrypt.txt and saving in decrypt.txt')
        time.sleep(2)
        plaintext = decrypt2(READ, key, AES.MODE_CBC, iv.encode())
        plaintext = Padding.removePadding(plaintext.decode(), mode=0)
        DECR.write("  decrypt: " + plaintext)
        plaintext = val
        plaintext = Padding.appendPadding(plaintext, blocksize=Padding.AES_blocksize, mode=0)

elif MODE == 'CFB':
    ciphertext = encrypt2(plaintext.encode(), key, AES.MODE_CFB, iv.encode())
    ENCR.write('CFB Cipher: ' + binascii.hexlify(bytearray(ciphertext)).decode())

    a = input('Do you want to decrypt your saved cipher text in new file? y/n:')
    if a == 'y':
        READ = open('encrypt.txt', 'r').readlines()
        print('reading encrypt.txt and saving in decrypt.txt')
        time.sleep(2)
        plaintext = decrypt2(READ, key, AES.MODE_CFB, iv.encode())
        plaintext = Padding.removePadding(plaintext.decode(), mode=0)
        DECR.write("  decrypt: " + plaintext)

        plaintext = val
        plaintext = Padding.appendPadding(plaintext, blocksize=Padding.AES_blocksize, mode=0)

else:
    print('MODE not available please choose a value from CBC, ECB, CFB')
