import datetime
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver

from src.employee.employee import Employee
from src.employee.employeelist import EmployeeList
from src.main.ElemExistError import ElemExistError
from src.main.readWriteUtils import open_file, get_user_name
from src.shift.shift import Shift


res_string = open_file("../input/config.login")
config = get_user_name(res_string)
config = {
    'EMAIL': config[0],
    'PASSWORD': config[1]
}

login_url = 'https://app.skello.io/users/sign_in?lang=fr'

driver = webdriver.Chrome('../utils/chromedriver')


def enter(elem):
    elem.send_keys(Keys.ENTER)
    time.sleep(1)


def click(elem):
    elem.click()
    time.sleep(1)


def date_before_today(date):
    today = datetime.today()
    return date < today


def get_prev_week():
    prev_week = driver.find_element_by_xpath("//div[@id='calendar']/a/button")
    click(prev_week)


def get_next_week():
    next_week = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[1]/div/div/div/div/a[2]/button")
    click(next_week)


def check_date(date):
    """
    :date: in date_format
    :return: true if data > 2019-04-5,2019-07-10  the date is after the last employee stil working
    """
    beginning_date = datetime.datetime(2019, 7, 29)
    return date > beginning_date



def login():
    try:
        driver.get(login_url)
        # put username
        username = driver.find_element(By.XPATH, "//div[@class='col-12']/div/input")
        username.send_keys(config['EMAIL'])
        # put password
        password = driver.find_element(By.XPATH, "//div[@class='col-12']/div[2]/input")
        password.send_keys(config['PASSWORD'])
        # login enter
        connect = driver.find_element(By.XPATH, "//div[@class='col-12']/button")
        click(connect)
        # get all employees planning
        all_employee_planning = driver.find_element(By.XPATH,
                                                    "/html/body/div[1]/div[2]/div/div[2]/div/table/tbody/tr/td[1]/div/a")
        click(all_employee_planning)

    except Exception as e:
        print("can't login")
        pass


def init_employees():
    employess = EmployeeList()
    add_employess_from_skello(employess)
    return employess


def add_employess_from_skello(employess: EmployeeList):
    max_employess = 40
    for i in range(max_employess):
        try:
            name = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[" + str(
                i) + "]/td[1]/div/div[2]/span[1]")
            name = name.text
            lastname = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[" + str(
                i) + "]/td[1]/div/div[2]/span[2]")
            lastname = lastname.text
            employess.add_employee(Employee(name, lastname))
        except Exception as e:
            pass


def go_future():
    max_future = 4
    for i in range(max_future):  # replace 2 with max
        try:
            get_next_week()
        except Exception as e:
            pass


def set_all_employee_shift_list(employees: EmployeeList):
    try:
        date_cheked = check_date(get_week_days()[0])
    except Exception as e:
        date_cheked = True
    while date_cheked:
        try:
            week_days = get_week_days()
            set_all_employee_week_shifts(employees, week_days)
            date_cheked = check_date(get_week_days()[0])
            employees.set_last_day_skello(week_days[6])
        except Exception as e:
            print(e)
            print("empty week")
        get_prev_week()


def get_week_days():
    w_days = []
    for i in range(7):
        w_days.append(get_day_i_from_skello(i))
    return w_days


def get_day_i_from_skello(i):
    """
    :pre-cond: week_table_not_empty
    :param i: 0 for the first day
    :pre-cond:
        date_elem :
            /html/body/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]
            /html/body/div[1]/div[2]/div/div/table/tbody/tr[1]/td[4]
    """
    date_elem = driver.find_element(By.XPATH,
                                    "/html/body/div[1]/div[2]/div/div/table/tbody/tr[1]/td[" + str(i + 2) + "]")
    # date = 2022-01-17T00:00:00+00:00
    date = date_elem.get_attribute('data-date')
    date = date.split("T00")[0]
    date = date.split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    return datetime.datetime(year, month, day)


def set_all_employee_week_shifts(employees: EmployeeList, week_days):
    """
    :pre-cond: not empty week table
    :param employees:
    :param week_days:
    :return:
    for all employee on skello
        get corresponding employee on the list if it exists, else pass
        get all his shift and add them directly
    """

    max_employee = 40
    for employee_skello_index in range(max_employee):
        employee_skello_name = get_employee_skello(employee_skello_index)
        if employee_skello_name is not None:
            employee_real = employees.get_employee_by_name(employee_skello_name.text)
            if employee_real is not None:
                set_employee_week_shifts(employee_real, employee_skello_index, week_days)


def get_employee_skello(employee_skello_index):
    """
    :pre-cond:
        skello_name_elem =
            /html/body/div[1]/div[2]/div/div/table/tbody/tr[1]/td[1]/div/div[2]/span[1]
            /html/body/div[1]/div[2]/div/div/table/tbody/tr[11]/td[1]/div/div[2]/span[1]
        11,1 beeing employee_skello_index
    :param employee_skello_index:
    :return: employee_skello_name_elem, or None if does not exist
    """
    try:
        elem = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[" + str(
            employee_skello_index) + "]/td[1]/div/div[2]/span[1]")
        return elem
    except Exception as e:
        return None
    return driver


def set_employee_week_shifts(employee: Employee, employee_skello_index, week_days):
    # for each day from day 1 to day 7
    for day_index in range(7):
        set_all_day_i_shifts(employee, employee_skello_index, day_index + 2, week_days[day_index])



def set_all_day_i_shifts(employee: Employee, employee_skello_index, day_index, real_day):
    """
    :param day_index : 1 for day 1 and 7 for day 7
    :param i: day number, 1 for the first day, 7 for the last
    :return:
        get all shifts in that day
        append this list to employee shift list
    """
    all_day_i_shifts = day_shift_list(employee_skello_index, day_index, real_day)
    employee.add_list_shift(all_day_i_shifts)




def day_shift_list(employee_skello_index, day_index, real_day):
    """
    :pre-cond: we can have at max 8 shifts a day: we limit the number for time complexity  matters
    :param employee_skello_index:
    :param day_index:
    :return: list of shift from <employee>,  worked in during <day>
    :invarion:
        res = []
        for each shift index:
            if shift is not None:  shift<only worked shift not abscence..>  append to res
        return res
    """

    max_shift = 5
    res = []
    for shift_index in range(max_shift):
        shift = get_shift_from_index(employee_skello_index, day_index, shift_index, real_day)
        if shift is not None:
            res.append(shift)



    return res


def get_shift_from_index(employee_skello_index, day_index, shift_index, real_day):
    """
    :param shift_index:
    :param employee_skello_index:
    :param day_index:
    :param i:
    :return: shift if it does exist,None if not
    """
    return get_shift_from_elem(employee_skello_index, day_index, shift_index, real_day)


def get_shift_from_elem(employee_skello_index, day_index, shift_index, current_day):
    """
    Preconditions:
        start_time = /html/body/div[1]/div[2]/div/div/table/tbody/tr[23]/td[4]/div/div[8]/div[3]/div/span[1]/div/span[1]
        end_time   = /html/body/div[1]/div[2]/div/div/table/tbody/tr[23]/td[4]/div/div[8]/div[3]/div/span[1]/div/span[3]
        title      = /html/body/div[1]/div[2]/div/div/table/tbody/tr[23]/td[4]/div/div[8]/div[3]/div/span[2]
        with
            23 = employee_index
            4  = day_index
            8  = shift_index
    :param employee_skello_index:
    :param day_index:
    :param shift_index:
    :return: shift or None if it does not exist
    invrion:
            get shift start_time
            get shift end_time
            get shift title
            init shift: shift(:param:day)
            add attribute: s_time, e_time, title
            return shift
    """
    try:
        start_time_elem = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[" + str(
            employee_skello_index) + "]/td[" + str(day_index) + "]/div/div[" + str(
            shift_index) + "]/div[3]/div/span[1]/div/span[1]")
        start_time = start_time_elem.text
        end_time_elem = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[" + str(
            employee_skello_index) + "]/td[" + str(day_index) + "]/div/div[" + str(
            shift_index) + "]/div[3]/div/span[1]/div/span[3]")
        end_time = end_time_elem.text
        title_elem = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[" + str(
            employee_skello_index) + "]/td[" + str(day_index) + "]/div/div[" + str(shift_index) + "]/div[3]/div/span[2]")
        title = title_elem.text

        shift = Shift(current_day)
        shift.add_start(start_time)
        shift.add_end(end_time)
        shift.add_title(title)
        raise(ElemExistError(shift))
    except ElemExistError as e:
        return e.shift

    except NoSuchElementException as nsee:
        return None
