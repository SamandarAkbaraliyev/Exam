from rest_framework.permissions import BasePermission
from .models import Course


class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        buyers = Course.objects.values('is_bought')
        user_id = request.user.id
        for buyer in buyers:
            if user_id == buyer['is_bought']:
                return True
        return False
