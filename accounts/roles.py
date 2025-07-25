from rolepermissions.roles import AbstractUserRole


class SuperAdmin(AbstractUserRole):
    """System Administrator Role with full privileges.

        Admins have unrestricted access to all platform features

        Permissions
        ----------
        all_access : bool
            Can control the entire system


        Example
        -------
        >>> from rolepermissions.roles import assign_role
        >>> assign_role(user, Admin)
        """

    available_permissions = {
        'all_access': True
    }


class Moderator(AbstractUserRole):
    available_permissions = {
        'all_access': True
    }


class Principal(AbstractUserRole):
    available_permissions = {
        'manage_school': True,
        'manage_school_dashboard': True,

        'view_all_grade': True,
        'view_grade': True,
        'create_grade': True,
        'edit_grade': True,
        'delete_grade': True,

        'create_section': True,
        'view_all_section': True,
        'view_section': True,
        'edit_section': True,
        'delete_section': True,

        'view_all_attendance': True,
        'view_attendance_reports': True,
        'export_attendance_data': True,
    }


class SchoolStaff(AbstractUserRole):
    available_permissions = {
        'view_all_routine': True,
        'view_routine': True,
        'create_routine': True,
        'edit_routine': True,
        'delete_routine': True,

        'view_all_result': True,
        'view_result': True,
        'create_result': True,
        'edit_result': True,
        'delete_result': True,

        'view_all_assignment': True,
        'view_assignment': True,
        'create_assignment': True,
        'edit_assignment': True,
        'delete_assignment': True,

        'view_all_fee': True,
        'view_fee': True,
        'create_fee': True,
        'edit_fee': True,
        'delete_fee': True,

        'view_all_salary': True,
        'view_salary': True,
        'create_salary': True,
        'edit_salary': True,
        'delete_salary': True,

        'manage_student': True,

        'manage_teacher': True,

        'view_all_grade': True,
        'view_grade': True,
        'view_all_section': True,
        'view_section': True,
        'view_resource': True,

        'view_all_attendance': True,
        'edit_attendance': True,  # For corrections
        'export_attendance_data': True,
    }


class Teacher(AbstractUserRole):
    available_permissions = {
        'view_all_assignment': True,
        'view_assignment': True,
        'create_assignment': True,
        'edit_assignment': True,
        'delete_assignment': True,

        'view_all_result': True,
        'view_result': True,
        'create_result': True,
        'edit_result': True,
        'delete_result': True,

        'view_all_resource': True,
        'view_resource': True,
        'create_resource': True,
        'edit_resource': True,
        'delete_resource': True,

        'view_routine': True,
        'view_salary': True,
        'view_grade': True,
        'view_section': True,

        'take_attendance': True,
        'view_class_attendance': True,
        'edit_own_attendance': True,  # Only for attendances they've taken
    }


class Student(AbstractUserRole):
    available_permissions = {
        'view_routine': True,
        'view_result': True,

        'view_assignment': True,
        'submit_assigment': True,

        'view_salary': True,
        'view_grade': True,
        'view_section': True,
        'view_resource': True,

        'view_own_attendance': True,
    }

