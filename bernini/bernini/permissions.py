from rest_framework.permissions import BasePermission

class IsUserOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.id == request.user.pk

# el buen bug, hay PR por eso creamos el custom https://github.com/encode/django-rest-framework/issues/7117
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))
    
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))