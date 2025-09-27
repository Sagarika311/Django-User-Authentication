from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def make_activation_data(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uid, token

def decode_uid(uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        return uid
    except Exception:
        return None
