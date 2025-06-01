import jwt
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from apps.users.models import User

JWT_SECRET = getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
JWT_ALGORITHM = 'HS256'


class JWTRoleMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        required_role = getattr(view_func, 'role_required', None)
        if required_role is None and hasattr(view_func, 'view_class'):
            view_class = view_func.view_class
            method = request.method.lower()
            view_method = getattr(view_class, method, None)
            if view_method:
                required_role = getattr(view_method, 'role_required', None)

        if not required_role:
            return None

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'detail': 'Token expired.'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'detail': 'Invalid token.'}, status=401)

        try:
            user = User.objects.get(id=payload['user_id'], is_active=True)
        except User.DoesNotExist:
            return JsonResponse({'detail': 'User not found or inactive.'}, status=404)

        if isinstance(required_role, (list, tuple)):
            if user.role not in required_role:
                return JsonResponse({'detail': 'Permission denied.'}, status=403)
        else:
            if user.role != required_role:
                return JsonResponse({'detail': 'Permission denied.'}, status=403)

        request.user = user
        return None


def role_required(role):
    def decorator(view_func):
        setattr(view_func, 'role_required', role)
        return view_func

    return decorator
