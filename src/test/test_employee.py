import datetime
import os

from src.employee.employee import Employee
from src.employee.employeelist import EmployeeList
from src.shift.shift import Shift


def test_save_in_csv():
    employee = Employee("slim", "msb")
    employee.save_in_csv()
    assert os.listdir("../output/csv").__contains__("msb_slim.csv")


def test_update_total():
    employee = Employee("slim", "msb")
    date = datetime.datetime(2018, 12, 2)

    shift1 = Shift(date)
    shift1.add_start("18:00")
    shift1.add_end("19:30")
    shift1.add_title("cuisine")

    shift2 = Shift(date)
    shift2.add_start("10:00")
    shift2.add_end("12:30")
    shift2.add_title("cuisine")

    shift3 = Shift(date)
    shift3.add_start("19:00")
    shift3.add_end("00:30")
    shift3.add_title("cuisine")

    employee.add_shift(shift1)
    employee.add_shift(shift2)
    employee.add_shift(shift3)

    min = 30
    h = 8 + 1

    assert employee.total == datetime.timedelta(hours=h, minutes=min)


def test_get_hours_per_day():
    employee = Employee("slim", "msb")
    employee.contract_total = 78
    assert employee.get_hours_per_day() == datetime.timedelta(hours=2, minutes=34)


def test_number_of_day_until_date():
    employee = Employee("slim", "msb")
    employee.contract_start = datetime.datetime(2022, 5, 2)
    last_day = datetime.datetime(2022, 5, 20)
    assert employee.number_of_day_until_date(last_day) == 20 - 2


def test_update_balance():
    employee = Employee("slim", "msb")
    employee.contract_start = datetime.datetime(2022, 5, 16)
    employee.contract_total = 78
    last_day = datetime.datetime(2022, 5, 20)

    date = datetime.datetime(2018, 12, 2)

    shift1 = Shift(date)
    shift1.add_start("18:00")
    shift1.add_end("19:30")
    shift1.add_title("cuisine")

    shift2 = Shift(date)
    shift2.add_start("10:00")
    shift2.add_end("12:30")
    shift2.add_title("cuisine")

    shift3 = Shift(date)
    shift3.add_start("19:00")
    shift3.add_end("00:30")
    shift3.add_title("cuisine")

    employee.add_shift(shift1)
    employee.add_shift(shift2)
    employee.add_shift(shift3)

    print(employee.get_balance(last_day).total_seconds()/60/60)

    assert True


def test_get_absence():
    employees_load = EmployeeList()
    employees_load = employees_load.load_object()

    employees = EmployeeList()
    employees.set_last_day_skello(employees_load.last_day_skello)
    employees.set_employee_list(employees_load.employee_list)

    print(employees.employee_list[0].total)
    employees.employee_list[0].fix_absence()
    print(employees.employee_list[0].total)

    print(employees.employee_list[0])

    assert True
