# views.py
from django.http import JsonResponse
from django.views import View

from apps.users.middleware import role_required


class AdminOnlyView(View):
    @role_required('admin')
    def get(self, request):
        return JsonResponse({'msg': f'Xush kelibsiz, {request.user.username} (Admin)!'})


class ManagerOrAdminView(View):
    @role_required(['manager', 'admin'])
    def get(self, request):
        return JsonResponse({'msg': f'Assalomu alaykum, {request.user.username} (Manager/Admin)!'})
