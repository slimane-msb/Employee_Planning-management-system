import datetime

from src.employee.employeelist import EmployeeList
from src.employee.employee import  Employee


def main_employees():

    employees_load = EmployeeList()
    employees_load = employees_load.load_object()

    employees = EmployeeList()
    employees.set_last_day_skello(employees_load.last_day_skello)
    employees.set_employee_list(employees_load.employee_list)
    print(employees.last_day_skello)

    employees.employee_list[0].contract_start = datetime.datetime(2021, 11, 7)
    employees.employee_list[0].contract_total = 35*4.33
    print(employees.employee_list[0].name)
    employees.employee_list[0].fix_absence()
    print(employees.employee_list[0].get_balance(employees.last_day_skello).total_seconds() / 60 / 60)
    print(employees.employee_list[0].number_of_day_until_date(employees.last_day_skello))
    print(employees.employee_list[0].total)

    print("-----------------------------------------------------------------------------")

    employees.employee_list[19].contract_start = datetime.datetime(2021, 10, 27)
    employees.employee_list[19].contract_total = 18 * 4.33
    print(employees.employee_list[19].name)
    employees.employee_list[0].fix_absence()
    print(employees.employee_list[19].get_balance(employees.last_day_skello).total_seconds() / 60 / 60)
    print(employees.employee_list[19].number_of_day_until_date(employees.last_day_skello))
    print(employees.employee_list[19].total)


if __name__ == '__main__':
    main_employees()