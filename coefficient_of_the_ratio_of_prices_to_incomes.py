from pandas import DataFrame
import pandas as pd
import xlrd
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# считываем необходимые файлы с сайта Росстата со среднедушевыми доходами
# по субъектам РФ за 2013-2106 гг, а также данные о стоимости минимального
# набора продуктов питания

income = pd.read_excel('fee.xls', sheet_name=0, header=2, index_col=0,
    skiprows=0, na_values='NaN')
price = pd.read_excel('cen.xls', sheet_name=0, header=3, index_col=0,
    skiprows=0, na_values='NaN')

names_value = []

filtr = price.filter(like='федеральный округ', axis=0)

# извлечем наименования федеральных округов

for index, row in filtr.iterrows():
    names_value.append(index)

# удалим из списка Южный, а также Крымский Федеральные округа, так как данных
# по ним очень мало

names_value.pop(2)
names_value.pop(7)

def meanValue(begin, end):
    average = []
    lst = []
    for i in range(0, len(filtr)):
        for j in range(begin, end):
            lst.append(filtr.iloc[i][j])
        average.append(np.mean(lst))
        lst.clear()
    return average

def addValue(income):
    value = []
    for i in range(0, len(income)):
        value.append(income.iloc[i])
    value.pop(2)
    return value

def preparationResult(average, value):
    rslt = []
    for i in range(0, len(average)):
        rslt.append(average[i]/value[i])
    return rslt

def printResult(result):
    for i in range(0, len(result)):
        print(names_value[i], result[i])

# посчитаем среднее значение по годам стоимости минимального набора питания
# о всем ФО, так как данных за год не предоставлено

average_2013 = meanValue(0, 12)
average_2014 = meanValue(12, 24)
average_2015 = meanValue(24, 36)
average_2016 = meanValue(36, 48)

# очистим списки от ненужных nan

average_2013 = list(filter(lambda i: str(i) != 'nan', average_2013))
average_2014 = list(filter(lambda i: str(i) != 'nan', average_2014))
average_2015 = list(filter(lambda i: str(i) != 'nan', average_2015))
average_2016 = list(filter(lambda i: str(i) != 'nan', average_2016))

average_2015.pop(7)

# отфильтруем данные усредненных доходов, оставив лишь федеральные округа

filtr_income = income.filter(like='федеральный', axis=0)

income_2013 = filtr_income['2013 год']
income_2014 = filtr_income['2014 год']
income_2015 = filtr_income['2015год']
income_2016 = filtr_income['2016год']

# добавим в списки только значения по каждому году из данных об усредненных
# доходах, также удалим данные по Южному ФО, так как их не с чем сравнивать

value_2013 = addValue(income_2013)
value_2014 = addValue(income_2014)
value_2015 = addValue(income_2015)
value_2016 = addValue(income_2016)

rslt1 = preparationResult(average_2013, value_2013)
rslt2 = preparationResult(average_2014, value_2014)
rslt3 = preparationResult(average_2015, value_2015)
rslt4 = preparationResult(average_2016, value_2016)

print('Результаты за 2013 год:' + '\n')
printResult(rslt1)

print('Результаты за 2014 год:' + '\n')
printResult(rslt2)

print('Результаты за 2015 год:' + '\n')
printResult(rslt3)

print('Результаты за 2016 год:' + '\n')
printResult(rslt4)

# построим диаграмму отношения минимального набора
# питания к доходам за 2015, 2016 гг

arr = ['ЦФО', 'CЗФО', 'СКФО', 'ПФО', 'УФО', 'СФО', 'ДФО']

dpi = 80
fig = plt.figure(dpi=dpi, figsize=(879 / dpi, 600 / dpi))
mpl.rcParams.update({'font.size': 9})
plt.title('Гистограмма отношения минимальной продуктовой потребительской' +
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

# построим диаграмму стоимости минимальной корзины по округам за 2016 год

plt.bar(arr, average_2016, color='red', label='2016', alpha=0.7, zorder=2)

plt.xlabel('Наименование федерального округа')
plt.ylabel('Стоимость минимальной потребительской корзины')
plt.title('Диаграмма стоимости минимальной потребительской корзины' + '\n' +
          'по федеральным округам за 2016 год')
plt.show()

# построим диаграмму средней заработной платы по округам за 2016 год

plt.bar(arr, value_2016, color='black', alpha=0.7, label='2016',
        zorder=2)
plt.xlabel('Наименование федерального округа')
plt.ylabel('Средняя зарплата по округу')
plt.title('Диаграмма усредненных доходов по федеральным округам' + '\n' +
          'за 2016 год')
plt.show()
