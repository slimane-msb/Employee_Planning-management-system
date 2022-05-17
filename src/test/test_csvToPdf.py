from src.main.readWriteUtils import csv_to_pdf, open_file, get_user_name


def test_csv_to_pdf():
    csv_to_pdf()
    assert True


def test_open_file():
    res_string = open_file("../input/config.login")
    print(res_string)
    assert res_string is not None


def test_get_user_name():
    res_string = open_file("../input/config.login")
    config = get_user_name(res_string)
    print(config)
    assert len(config) ==2
