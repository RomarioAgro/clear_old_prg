import os
import re
import datetime
import subprocess
import pprint
import json


def clear_calling_func(ipath: str = 'u:\\prg\\test\\',
                       list_promo=None,
                       file_calling: str = '_Продажа.prg'):
    """
    перебор файла вызова функций (обычно это _Продажа.prg) и исключение протухших акций
    получаем список строк которые должны остаться в файле
    :param ipath:
    :param list_promo:
    :param file_calling str файл из которого обычно вызываются функции
    :return:
    """
    if list_promo is None:  #список истекших акций
        list_promo = ['1212', '1501']
    new_selling_list = []
    pattern_number_akcii = r'\d{3,5}'
    pattern_number = r'\b.*_Акция_(?!(?:6099|2571))\d{1,4}\b'
    with open(ipath + file_calling, 'r', encoding='cp866') as f_calling:
        selling_list = f_calling.readlines()
    for elem in selling_list:
        match_s = re.search(pattern_number, elem)
        if match_s:
            match_number = re.search(pattern_number_akcii, match_s[0])
        else:
            match_number = []
        if match_s and match_number[0] in list_promo:
            new_selling_list.append('')
        else:
            new_selling_list.append(elem)
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
    # pattern_number = r'\b(?!\d*6099\b)\d{3,5}\b'
    # оставляем акцию 6099 - это отключение разрешительного режима
    # оставляем акцию 2571 - это список украденных сертификатов
    pattern = r'_ПроверкаДат_(?!\d*6099|\d*2571\b)\d{0,4}.prg'
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
                            if datetime.datetime.strptime(match[1], '%d.%m.%Y').date() < datetime.datetime.today().date():
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

    if list_promo is None:  #список истекших акций
        list_promo = []
    procs = []
    # Запускаем процессы
    for elem in list_promo:
        command = f'for %f in ("{ipath}*{elem}*.prg") do move "%f" "d:\\files\\qr\\\\"'
        p = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        procs.append(p)

    # Ждем завершения всех процессов и обрабатываем вывод
    for proc in procs:
        stdout, stderr = proc.communicate()
        # Декодируем вывод из кодировки cp866
        stdout_decoded = stdout.decode('cp866') if stdout else ''
        stderr_decoded = stderr.decode('cp866') if stderr else ''

        print(f"Return code: {proc.returncode}")
        if stdout_decoded:
            print(f"Standard output:\n{stdout_decoded}")
        if stderr_decoded:
            print(f"Error output:\n{stderr_decoded}")

def find_not_used_prg(ipath: str = 'u:\\prg\\test\\'):
    file_list = os.listdir(ipath)
    pattern = r'(?i)Функция .*\s*\([^)]*\)'
    pattern_prg = r'.*.prg'
    pattern_number_promo = r'\d{1,4}'
    list_funk_sbis = []
    prg_count = dict()
    # Перебор файлов
    for filename in file_list:
        if re.fullmatch(pattern_prg, filename):
            with open(ipath + filename, 'r', encoding='cp866') as file_prg:
                for line in file_prg:
                    match = re.search(pattern, line)
                    if match:
                        sbis_funk = match[0].split(' ')[1].split('(')[0]
                        list_funk_sbis.append(sbis_funk)
                        prg_count[sbis_funk] = prg_count.get(sbis_funk, 0) + 1
                        print(sbis_funk)

        #                 if datetime.datetime.strptime(match[1], '%d.%m.%Y') < datetime.datetime.today():
        #                     number_promo = re.search(pattern_number_promo, filename)
        #                     promo_list.append(number_promo[0])
        #                     print(filename)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(prg_count)
        # return promo_list


def main():
    path_prg = 'u:\\prg\\__\\'
    # path_prg = 'd:\\kassa\\prg\\'
    path_prg = 'u:\\prg\\test\\'
    # find_not_used_prg(ipath=path_prg)
    promo_list = []
    promo_list = find_ended_func(ipath=path_prg)  #поиск кончившихся функций
    # #очистка файла вызова функций от тех которые кончились
    new_calling_promo = clear_calling_func(ipath=path_prg, list_promo=promo_list, file_calling='_Продажа.prg')
    new_prg_file(path=path_prg, name='_Продажа.prg', list_string_file=new_calling_promo)
    # # очистка файла вызова функций от тех которые кончились
    new_calling_promo = clear_calling_func(ipath=path_prg, list_promo=promo_list, file_calling='_ПечатьКупонаPY.prg')
    new_prg_file(path=path_prg, name='_ПечатьКупонаPY.prg', list_string_file=new_calling_promo)
    # удаление кончившихся функций
    del_ended_prg(ipath=path_prg, list_promo=promo_list)
    # print(promo_list)


if __name__ == '__main__':
    main()