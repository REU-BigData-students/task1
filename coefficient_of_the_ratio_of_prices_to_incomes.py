from pandas import DataFrame
import pandas as pd
import xlrd
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
""" Module displays the statistics of the ratio of the minimum consumer basket to the average per capita average income """
income = pd.read_excel('fee.xls', sheet_name=0, header=2, index_col=0,
                       skiprows=0, na_values='NaN')
price = pd.read_excel('cen.xls', sheet_name=0, header=3, index_col=0,
                      skiprows=0, na_values='NaN')


def main():
    average = meanValue(4)
    names_value = form()
    value = addValue()
    rslt = preparationResult(average, value)
    formData = changeForm(rslt)
    print('Результаты:' + '\n')
    printResult(formData, names_value)
    graf(average, formData, value)


def meanValue(countYears):
    """ Calculation of the average value of the basket by years.

    Keyword arguments:
    countYears -- number of years for statistics

    """
    filtr = price.filter(like='федеральный округ', axis=0)
    average = []
    lst = []
    lst1 = []
    result = []
    begin = 0
    end = 12
    for i in range(0, len(filtr)):
        for j in range(0, countYears * 12):
            lst.append(filtr.iloc[i][j])
    for i in range(0, 36):
        for j in range(begin, end):
            lst1.append(lst[j])
        result.append(np.nanmean(lst1))
        lst1.clear()
        begin += 12
        end += 12
    result = list(filter(lambda i: str(i) != 'nan', result))
    result.pop(8)
    result.pop(28)
    result.pop(28)
    return result


def addValue():
    """ Adding only numeric values to the lists for each year """
    filtr_income = income.filter(like='федеральный', axis=0)
    value = []
    for i in range(0, 8):
        for j in range(15, 78, 16):
            value.append(filtr_income.iloc[i][j])
    indices = 8, 9, 10, 11
    value = [i for j, i in enumerate(value) if j not in indices]
    return value


def form():
    filtr = price.filter(like='федеральный округ', axis=0)
    """Create a list with the desired names of regions"""
    names_value = []
    for index, row in filtr.iterrows():
        names_value.append(index)
    names_value.pop(2)
    names_value.pop(7)
    return names_value


def preparationResult(average, value):
    """Calculating the ratio of the value of the basket to the income"""
    rslt = []
    for i in range(0, len(average)):
        rslt.append(average[i]/value[i])
    return rslt


def printResult(result, names_value):
    """Displaying results"""
    begin = 0
    end = 7
    lst = []
    for i in range(0, 4):
        for j in range(0, len(names_value)):
            lst.append(names_value[j])
    for i in range(0, 4):
        for j in range(begin, end):
            print(lst[j], result[j])
        print('\n' + 'Следующий год:' + '\n')
        begin += 7
        end += 7


def changeForm(rslt):
    """Arranging the elements in the list in a convenient form"""
    result = []
    count = 0
    for i in range(0, 4):
        for j in range(count, len(rslt), 4):
            result.append(rslt[j])
        count += 1
    return result


def graf(average, formData, value):
    """Construction of results charts

    firstly, the diagram a coefficient chart for 2015 and 2016
    secondly, the coefficient chart for 2016
    thirdly, the diagram of average per capita income for 2016

    """
    arr = ['ЦФО', 'CЗФО', 'СКФО', 'ПФО', 'УФО', 'СФО', 'ДФО']
    b = formData[14:21]
    c = formData[21:]
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(879 / dpi, 600 / dpi))
    mpl.rcParams.update({'font.size': 9})
    plt.title(
        'Гистограмма отношения минимальной продуктовой потребительской' +
        '\n' + 'корзины от среднедушевых доходов граждан по регионам' +
        '\n' + 'за 2015 и 2016 года')
    plt.ylabel('Наименование федерального округа')
    plt.xlabel('Значение коэффициента')
    xs = range(len(arr))
    plt.barh([x + 0.38 for x in xs], c,
             height=0.2, color='red', alpha=0.7, label='2015 год',
             zorder=2)

    plt.barh([x + 0.05 for x in xs], b,
             height=0.2, color='blue', alpha=0.7, label='2016 год',
             zorder=2)
    plt.yticks(xs, arr, rotation=10)
    plt.legend(loc='upper right')
    plt.show()
    a = average[3::4]
    plt.bar(arr, a, color='red', label='2016', alpha=0.7, zorder=2)
    plt.xlabel('Наименование федерального округа')
    plt.ylabel('Стоимость минимальной потребительской корзины')
    plt.title(
        'Диаграмма стоимости минимальной потребительской корзины' +
        '\n' + 'по федеральным округам за 2016 год')
    plt.show()
    v = value[3::4]
    plt.bar(arr, v, color='black', alpha=0.7, label='2016',
            zorder=2)
    plt.xlabel('Наименование федерального округа')
    plt.ylabel('Средняя зарплата по округу')
    plt.title('Диаграмма усредненных доходов по федеральным округам' + '\n' +
              'за 2016 год')
    plt.show()

if __name__ == '__main__':
    main()
