

import time

from src.main.Selnuim_utils import *


def update_employees_from_skello():
    login()
    employees = init_employees()
    print(employees)
    go_future()
    print("done")
    set_all_employee_shift_list(employees)
    print(employees.employee_list[0])
    employees.save_shifts_in_csv()
    employees.save_object()






if __name__ == '__main__':
    update_employees_from_skello()


