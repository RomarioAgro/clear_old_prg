import os
import re
import datetime


def clear_calling_func(ipath: str = 'u:\\prg\\test\\', list_promo=None):
    """
    перебор файла _Продажа.prg и исключение протухших акций
    :param ipath:
    :param list_promo:
    :return:
    """
    if list_promo is None:
        list_promo = ['1212', '1501']
    list_promo2 = [x + '()' for x in list_promo]
    print(list_promo2)
    selling_list = []
    file_calling = '_Продажа.prg'
    pattern_promo = r'_Акция_\d{1,4}\(\)'
    pattern_number = r'\d{1,4}\(\)'
    with open(ipath + file_calling, 'r', encoding='cp866') as f_calling:
        for line in f_calling:
            selling_list.append(line[0:len(line) - 1])
    for elem in selling_list:
        match_s = re.search(pattern_number, elem)
        if match_s and match_s[0] not in list_promo2:
            # if match_s[0] not in list_promo2:
            # print(match_s[0])
            print(elem)
    # print(selling_list)

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



def main():
    path_prg = 'u:\\prg\\test\\'
    promo_list = []
    # promo_list = find_ended_func(ipath=path_prg)
    clear_calling_func(ipath=path_prg, list_promo=promo_list)
    # print(promo_list)


if __name__ == '__main__':
    main()