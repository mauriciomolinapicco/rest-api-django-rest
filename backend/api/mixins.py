from . permissions import IsStaffEditorPermission
from rest_framework import permissions

class StaffEditorPermissionMixin():
    permission_classes = [
        IsStaffEditorPermission,
        permissions.IsAdminUser
        ]