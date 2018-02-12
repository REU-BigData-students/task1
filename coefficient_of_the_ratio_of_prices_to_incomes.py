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
    filtr = price.filter(like='федеральный округ', axis=0)
    average_2013 = meanValue(0, 12)
    average_2014 = meanValue(12, 24)
    average_2015 = meanValue(24, 36)
    average_2016 = meanValue(36, 48)
    average_2015.pop(7)
    names_value = []
    for index, row in filtr.iterrows():
        names_value.append(index)
    names_value.pop(2)
    names_value.pop(7)
    filtr_income = income.filter(like='федеральный', axis=0)
    income_2013 = filtr_income['2013 год']
    income_2014 = filtr_income['2014 год']
    income_2015 = filtr_income['2015год']
    income_2016 = filtr_income['2016год']

    value_2013 = addValue(income_2013)
    value_2014 = addValue(income_2014)
    value_2015 = addValue(income_2015)
    value_2016 = addValue(income_2016)

    rslt1 = preparationResult(average_2013, value_2013)
    rslt2 = preparationResult(average_2014, value_2014)
    rslt3 = preparationResult(average_2015, value_2015)
    rslt4 = preparationResult(average_2016, value_2016)

    print('Результаты за 2013 год:' + '\n')
    printResult(rslt1, names_value)

    print('Результаты за 2014 год:' + '\n')
    printResult(rslt2, names_value)

    print('Результаты за 2015 год:' + '\n')
    printResult(rslt3, names_value)

    print('Результаты за 2016 год:' + '\n')
    printResult(rslt4, names_value)

    arr = ['ЦФО', 'CЗФО', 'СКФО', 'ПФО', 'УФО', 'СФО', 'ДФО']
    graf(arr, rslt1, rslt2, rslt3, rslt4)


def meanValue(begin, end):
    """ Calculation of the average value of the basket by years.

    Keyword arguments:
    begin -- the month from which the value of the basket is counted
    end -- month to which the cost of the basket is calculated


    """
    filtr = price.filter(like='федеральный округ', axis=0)
    average = []
    lst = []
    for i in range(0, len(filtr)):
        for j in range(begin, end):
            lst.append(filtr.iloc[i][j])
        average.append(np.mean(lst))
        lst.clear()
    average = list(filter(lambda i: str(i) != 'nan', average))
    return average


def addValue(income):
    """ Adding only numeric values to the lists for each year """
    value = []
    for i in range(0, len(income)):
        value.append(income.iloc[i])
    value.pop(2)
    return value


def preparationResult(average, value):
    """Calculating the ratio of the value of the basket to the income"""
    rslt = []
    for i in range(0, len(average)):
        rslt.append(average[i]/value[i])
    return rslt


def printResult(result, names_value):
    """Displaying results"""
    filtr = price.filter(like='федеральный округ', axis=0)
    for i in range(0, len(result)):
        print(names_value[i], result[i])


def graf(arr, rslt1, rslt2, rslt3, rslt4):
    """Construction of results charts

    firstly, the diagram a coefficient chart for 2015 and 2016
    secondly, the coefficient chart for 2016
    thirdly, the diagram of average per capita income for 2016

    """
    filtr_income = income.filter(like='федеральный', axis=0)
    income_2016 = filtr_income['2016год']
    average_2016 = meanValue(36, 48)
    value_2016 = addValue(income_2016)
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
    plt.barh([x + 0.38 for x in xs], rslt2,
             height=0.2, color='red', alpha=0.7, label='2015 год',
             zorder=2)
    plt.barh([x + 0.05 for x in xs], rslt3,
             height=0.2, color='blue', alpha=0.7, label='2016 год',
             zorder=2)
    plt.yticks(xs, arr, rotation=10)
    plt.legend(loc='upper right')
    plt.show()

    plt.bar(arr, average_2016, color='red', label='2016', alpha=0.7, zorder=2)
    plt.xlabel('Наименование федерального округа')
    plt.ylabel('Стоимость минимальной потребительской корзины')
    plt.title(
        'Диаграмма стоимости минимальной потребительской корзины' +
        '\n' + 'по федеральным округам за 2016 год')
    plt.show()

    plt.bar(arr, value_2016, color='black', alpha=0.7, label='2016',
            zorder=2)
    plt.xlabel('Наименование федерального округа')
    plt.ylabel('Средняя зарплата по округу')
    plt.title('Диаграмма усредненных доходов по федеральным округам' + '\n' +
              'за 2016 год')
    plt.show()

if __name__ == '__main__':
    main()
