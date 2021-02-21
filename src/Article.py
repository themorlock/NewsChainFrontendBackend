import hashlib

class Article:
    def __init__(self, text, signature, e, n):
        self.text = text
        self.signature = signature
        self.e = e
        self.n = n

    def verify(self):
        text_hash = int.from_bytes(hashlib.sha512(str.encode(self.text)).digest(), byteorder='big')
        hash_signature = pow(self.signature, self.e, self.n)
        return text_hash == hash_signature

    def get_hash(self):
        article_string = "{}{}{}{}".format(self.text, self.signature, self.e, self.n)
        return hashlib.sha512(str.encode(article_string)).hexdigest()
