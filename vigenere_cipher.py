class Vigenere:
    def __init__(self):
        self.alphabet = [c for c in (chr(i) for i in range(32, 127))]
        self.letter_to_index = dict(zip(self.alphabet, range(len(self.alphabet))))
        self.index_to_letter = dict(zip(range(len(self.alphabet)), self.alphabet))
        self.encrypted = ''
        self.decrypted = ''

    def encrypt(self, message, key):
        encrypted = ""
        split_message = [
            message[i: i + len(key)] for i in range(0, len(message), len(key))
        ]

        for each_split in split_message:
            i = 0
            for letter in each_split:
                number = (self.letter_to_index[letter] + self.letter_to_index[key[i]]) % len(self.alphabet)
                encrypted += self.index_to_letter[number]
                i += 1

        return encrypted

    def decrypt(self, cipher, key):
        decrypted = ""
        split_encrypted = [
            cipher[i: i + len(key)] for i in range(0, len(cipher), len(key))
        ]

        for each_split in split_encrypted:
            i = 0
            for letter in each_split:
                number = (self.letter_to_index[letter] - self.letter_to_index[key[i]]) % len(self.alphabet)
                decrypted += self.index_to_letter[number]
                i += 1

        return decrypted


v = Vigenere()
print('Leave empty to use pre-defined values\n')
message = input('Please enter a message to encrypt: ') or "Liwaa Audi, 17-02-2022"
key = input('Please enter your key: ') or "InformationSecurity"


def main():
    encrypted_message = v.encrypt(message, key)
    decrypted_message = v.decrypt(encrypted_message, key)

    print("Original message: " + message)
    print("Encrypted message: " + encrypted_message)
    print("Decrypted message: " + decrypted_message)


main()
