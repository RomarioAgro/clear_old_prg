import os
import re
import datetime
import subprocess


def clear_calling_func(ipath: str = 'u:\\prg\\test\\', list_promo=None):
    """
    перебор файла _Продажа.prg и исключение протухших акций
    получаем список строк которые должны остаться в файле
    :param ipath:
    :param list_promo:
    :return:
    """
    if list_promo is None:  #список истекших акций
        list_promo = ['1212', '1501']
    list_promo2 = [x + '()' for x in list_promo]
    new_selling_list = []
    file_calling = '_Продажа.prg'
    pattern_number = r'\d{4}\(\)'
    with open(ipath + file_calling, 'r', encoding='cp866') as f_calling:
        selling_list = f_calling.readlines()
    for elem in selling_list:
        match_s = re.search(pattern_number, elem)
        new_promo_str = elem
        if match_s and match_s[0] in list_promo2:
            new_promo_str = ''
        if new_promo_str != '':
            new_selling_list.append(new_promo_str)
    return new_selling_list

def new_prg_file(path: str = 'u:\\prg\\test\\',
                 name:str = '_Продажа.prg',
                 list_string_file=None):
    """
    создаем новый файл _Продажа.prg
    :param path:
    :param name:
    :param list_string_file:
    :return:
    """
    if list_string_file is None:
        list_string_file = []
    with open(path + name, 'w', encoding='cp866') as new_file:
        new_file.writelines(list_string_file)


def find_ended_func(ipath: str = 'u:\\prg\\test\\'):
    """
    перебираем все файлы в папке с функциями, ищем функции у которых истек срок действия
    :param ipath: путь до папки с функциями
    :return: список с номерами истекших функций
    """

    file_list = os.listdir(ipath)
    pattern = r'_ПроверкаДат_\d{0,4}.prg'
    pattern_date = r'\d{2}[.]\d{2}[.]\d{4}'
    pattern_number_promo = r'\d{1,4}'
    promo_list = []
    # Перебор файлов
    for filename in file_list:
        if os.path.isfile(os.path.join(ipath, filename)) \
                and re.fullmatch(pattern, filename):
                with open(ipath + filename, 'r', encoding='cp866') as file_prg:
                    for line in file_prg:
                        match = re.findall(pattern_date, line)
                        if match:
                            if datetime.datetime.strptime(match[1], '%d.%m.%Y') < datetime.datetime.today():
                                number_promo = re.search(pattern_number_promo, filename)
                                promo_list.append(number_promo[0])
                                print(filename)
    return promo_list

def del_ended_prg(ipath: str = 'u:\\prg\\test\\', list_promo=None):
    """
    функция удаления файлов истекших функций
    :param ipath:
    :param list_promo:
    :return:
    """
    procs = []
    if list_promo is None:  #список истекших акций
        list_promo = []
    for elem in list_promo:
        p = subprocess.Popen('start /B del {1}*{0}*.prg /Q'.format(elem, ipath), encoding='cp1251', shell=True)
        procs.append(p)
    for proc in procs:
        proc.wait()
        print(proc.returncode)


def main():
    path_prg = 'u:\\prg\\test\\'
    promo_list = []
    promo_list = find_ended_func(ipath=path_prg)
    new_calling_promo = clear_calling_func(ipath=path_prg, list_promo=promo_list)
    new_prg_file(path=path_prg, name='_Продажа.prg', list_string_file=new_calling_promo)
    del_ended_prg(ipath=path_prg, list_promo=promo_list)
    # print(promo_list)


if __name__ == '__main__':
    main()