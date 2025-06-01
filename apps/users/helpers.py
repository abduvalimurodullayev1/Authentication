
from apps.users.models import AuthLog

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def get_user_agent(request):
    return request.META.get("HTTP_USER_AGENT", "")


def log_auth_action(user, action, request, metadata=None):
    AuthLog.objects.create(
        user=user,
        action=action,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
        metadata=metadata or {}
    )
