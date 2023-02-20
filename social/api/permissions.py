from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):  
    message = "You must be the owner of this object."
    my_safe_method = ["GET", "PUT"]

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
        ) 