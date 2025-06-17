import base64
import hashlib


def digest(msg: str):

    my_hash = hashlib.sha3_224(msg.encode("UTF-8"))
    dgst = str(base64.urlsafe_b64encode(my_hash.digest())).replace("b'","").replace("'","")
    return dgst