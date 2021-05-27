from rest_framework.permissions import BasePermission

class IsCartOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.user == request.user