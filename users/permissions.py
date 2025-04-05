from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # 'obj' уже получен, используем его напрямую
        return request.user == obj.owner

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="Модераторы").exists()