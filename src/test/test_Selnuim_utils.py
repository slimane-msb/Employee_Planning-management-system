from src.main.Selnuim_utils import *


def test_check_date():
    right_date = datetime.datetime(2020, 10, 12)
    wrong_date = datetime.datetime(2018, 10, 12)
    assert check_date(right_date) == True
    assert check_date(wrong_date) == False


def test_get_shift_from_elem():
    login()
    employees = init_employees()
    day = datetime.datetime(2020, 10, 20)
    shift = get_shift_from_elem(5, 3, 1, day)
    # elem exist
    #       "/html/body/div[1]/div[2]/div/div/table/tbody/tr[5]/td[3]/div/div/div[3]/div/span[1]/div/span[3]"
    # elem does not exist
    #       "/html/body/div[1]/div[2]/div/div/table/tbody/tr[5]/td[2]/div/div/div[3]/div/span[1]/div/span[3]"
    assert shift is not None
    shift = get_shift_from_elem(5, 2, 1, day)
    assert shift is None

