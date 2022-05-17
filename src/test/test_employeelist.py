from src.employee.employee import Employee
from src.employee.employeelist import EmployeeList


def test_load_shifts_from_csv():
    employees = EmployeeList()
    employees.load_shifts_from_csv()

    assert False


def test_load_object():
    employees = EmployeeList()
    employees = employees.load_object()
    assert employees is not None


def test_save_object():
    employees = EmployeeList()
    employee = Employee("slim","msb")
    employees.add_employee(employee)
    employees.save_object()
    assert True
