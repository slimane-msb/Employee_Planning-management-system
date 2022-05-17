import os

import pandas as pd
import pdfkit


def csv_to_pdf():
    for employee_file_name in os.listdir("../output/csv"):
        print(employee_file_name)
        df = pd.read_csv("../output/csv/" + employee_file_name, sep=",", encoding="ISO-8859-1")

        html_name = "../output/html/" + employee_file_name[:-3] + 'html'
        print(html_name)
        html_cource = df.to_html()
        write_file(html_name, html_cource)

        # path_wkhtmltopdf = r'C:\Users\mesba\Desktop\disque E\software\python\pdfkit\wkhtmltox-0.12.4_msvc2015-win64.exe'
        # config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        #
        # pdf_name = "../output/pdf/"+employee_file_name[:-3] + 'pdf'
        #
        # pdfkit.from_file(html_name, pdf_name, configuration=config)


def write_file(path, text):
    try:
        f = open(path, "w+")
        f.write(text)
        f.close()
    except FileNotFoundError as fnfe:
        print("FileNotFoundError")


def open_file(path):
    """
    :param path: path to the file
    :return: string in that file
    """
    try:
        f = open(path, "r")
        res = f.read()
        f.close()
        return res
    except FileNotFoundError as fnfe:
        print("FileNotFoundError: can't open the file")


def get_user_name(txt_config_login):
    """
    :param txt_config_login: username\npassword : string
    :return: list[username,password]
    """
    config_list = txt_config_login.split("\n")
    return config_list
