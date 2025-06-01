import jwt
import datetime
from django.conf import settings

from apps.users.models import RefreshToken


def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        'iat': datetime.datetime.utcnow(),
        'type': 'access',
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token




def generate_refresh_token(user, ip_address=None, user_agent=None):
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': expires_at,
        'iat': datetime.datetime.utcnow(),
        'type': 'refresh',
        'ip': ip_address,
        'ua': user_agent,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    token_obj = RefreshToken.objects.create(
        user=user,
        token=token,
        is_valid=True,
        ip_address=ip_address,
        user_agent=user_agent,
        expires_at=expires_at
    )

    return token, token_obj
