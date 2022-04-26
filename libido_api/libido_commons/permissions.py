from rest_framework import permissions

ALLOWED_IP_ADDRESSES = ["127.0.0.1"]


class AllowRetriveList(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve"]:
            return True

        return False


class AllowCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["create"]:
            return True
        return False


class NoRetrive(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["retrieve"]:
            return False
        return True


class NoCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["create"]:
            return False
        return True


class NoDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["create"]:
            return False
        return True


class NotAllowList(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list"]:
            return False
        return True


class SuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IPBasedPermission(permissions.BasePermission):
    # IP base permissions
    def has_permission(self, request, view):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0]
        else:
            ip_address = request.META.get("REMOTE_ADDR")

        return ip_address in ALLOWED_IP_ADDRESSES


#
#     def has_object_permission(self, request, view):
#         x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
#         if x_forwarded_for:
#             ip_address = x_forwarded_for.split(",")[0]
#         else:
#             ip_address = request.META.get("REMOTE_ADDR")
#
#         return ip_address in ALLOWED_IP_ADDRESSES
#
