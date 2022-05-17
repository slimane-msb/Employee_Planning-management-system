import os
import pickle
from datetime import datetime

from src.employee.employee import Employee


class EmployeeList:

    def __init__(self):
        self.employee_list = []
        self.last_day_skello = None



    def __str__(self) -> str:
        res = ""
        for employee in self.employee_list:
            res += str(employee) + "\n"
        return res

    def add_employee(self, employee):
        self.employee_list.append(employee)


    def add_employee_by_name(self, name, last_name):
        self.employee_list.append(Employee(name, last_name))

    def add_employee_from_file_name(self, file_name):
        file_name_list = file_name.split("_")
        last_name = file_name_list[0]
        name = file_name_list[1].split(".")[0]
        self.add_employee_by_name(name, last_name)

    def save_shifts_in_csv(self):
        for employee in self.employee_list:
            employee.save_in_csv()

    def load_shifts_from_csv(self):
        for file_name in os.listdir("../output/"):
            self.add_employee_from_file_name(file_name)
            for employee in self.employee_list:
                employee.init_from_repr(repr)


    def save_object(self):
        with open('../output/objects/employee_list_object.EmployeeList', 'wb') as employee_list_object:
            pickle.dump(self, employee_list_object)

    def load_object(self):
        with open('../output/objects/employee_list_object.EmployeeList', 'rb') as employee_list_object:
            return pickle.load(employee_list_object)

    def get_employee_by_name(self, name):
        for employee in self.employee_list:
            if employee.name == name:
                return employee
        return None

    def set_last_day_skello(self, last_day):
        if self.last_day_skello is None:
            self.last_day_skello = last_day

    def set_employee_list(self, employee_list):
        self.employee_list = employee_list
