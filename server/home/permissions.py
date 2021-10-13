from rest_framework import permissions

class InvoiceHasOwnPermission(permissions.BasePermission):    
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj.user


class ItemHasOwnPermission(permissions.BasePermission):    
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj.invoice.user