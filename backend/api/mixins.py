from . permissions import IsStaffEditorPermission
from rest_framework import permissions

class StaffEditorPermissionMixin():
    permission_classes = [
        IsStaffEditorPermission,
        permissions.IsAdminUser
        ]
    
class UserQuerySetMixin():
    user_field =  'field'
    def get_queryset(self, *args, **kwargs):
        lookup_data = {}
        lookup_data[self.user_field] = self.request.user
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(**lookup_data)
    """
    i am doing the same as in def get_queryset in views.py. Not implementing it rn but it would just 
    be importing it and 

    def get_queryset(self, *args, **kwargs):
        request = self.request
        user = self.request.user
        qs = super().get_queryset(*args, **kwargs)
        if not user.is_authenticated:
            return Product.objects.none()
        return qs.filter(user=request.user)

    """