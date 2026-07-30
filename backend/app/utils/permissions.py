from app.auth.models.user import User
from app.leave_management.models.leave_request import LeaveRequest

def is_hr_or_admin(
    user: User
):

    if user.role is None:
        return False


    return user.role.name in [
        "Super Admin",
        "HR Manager",
    ]

def is_manager_of_employee(
    user: User,
    leave_request: LeaveRequest
):

    if user.employee is None:
        return False


    employee = leave_request.employee


    if employee is None:
        return False


    return employee.manager_id == user.employee.id