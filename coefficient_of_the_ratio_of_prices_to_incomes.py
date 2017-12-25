from pandas import DataFrame
import pandas as pd
import xlrd
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

fee = 'fee.xls'
cen = 'cen.xls'

# считываем необходимые файлы с сайта Росстата со среднедушевыми доходами
# по субъектам РФ за 2013-2106 гг, а также данные о стоимости минимального
# набора продуктов питания

income = pd.read_excel(fee, sheet_name=0, header=2, index_col=0,
    skiprows=0, na_values='NaN')
price = pd.read_excel(cen, sheet_name=0, header=3, index_col=0,
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

lst2 = []
lst3 = []
lst4 = []
lst1 = []

average_2013 = []
average_2014 = []
average_2015 = []
average_2016 = []

# посчитаем среднее значение по годам стоимости минимального набора питания
# о всем ФО, так как данных за год не предоставлено

for i in range(0, len(filtr)):
    for j in range(0, 12):
        lst1.append(filtr.iloc[i][j])
    average_2013.append(np.mean(lst1))
    lst1.clear()

for i in range(0, len(filtr)):
    for j in range(12, 24):
        lst2.append(filtr.iloc[i][j])
    average_2014.append(np.mean(lst2))
    lst2.clear()

for i in range(0, len(filtr)):
    for j in range(24, 36):
        lst3.append(filtr.iloc[i][j])
    average_2015.append(np.mean(lst3))
    lst3.clear()

for i in range(0, len(filtr)):
    for j in range(36, 48):
        lst4.append(filtr.iloc[i][j])
    average_2016.append(np.mean(lst4))
    lst4.clear()

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

value_2013 = []
value_2014 = []
value_2015 = []
value_2016 = []

# добавим в списки только значения по каждому году из данных об усредненных
# доходах, также удалим данные по Южному ФО, так как их не с чем сравнивать

for i in range(0, len(income_2013)):
    value_2013.append(income_2013.iloc[i])
value_2013.pop(2)

for i in range(0, len(income_2014)):
    value_2014.append(income_2014.iloc[i])
value_2014.pop(2)

for i in range(0, len(income_2015)):
    value_2015.append(income_2015.iloc[i])
value_2015.pop(2)

for i in range(0, len(income_2016)):
    value_2016.append(income_2016.iloc[i])
value_2016.pop(2)

rslt = []
rslt1 = []
rslt2 = []
rslt3 = []

for i in range(0, len(average_2013)):
        rslt.append(average_2013[i]/value_2013[i])

for i in range(0, len(average_2014)):
        rslt1.append(average_2014[i]/value_2014[i])

for i in range(0, len(average_2015)):
        rslt2.append(average_2015[i]/value_2015[i])

for i in range(0, len(average_2016)):
        rslt3.append(average_2016[i]/value_2016[i])

print('\n')
print('Результаты за 2013 год:' + '\n')


# вывод результатов (2013 год)
for i in range(0, len(rslt)):
    print(names_value[i], rslt[i])

print('\n')
print('Результаты за 2014 год:' + '\n')

# вывод результатов (2014 год)
for i in range(0, len(rslt1)):
    print(names_value[i], rslt1[i])

print('\n')
print('Результаты за 2015 год:' + '\n')

# вывод результатов (2015 год)
for i in range(0, len(rslt2)):
    print(names_value[i], rslt2[i])

print('\n')
print('Результаты за 2016 год:' + '\n')

# вывод результатов (2016 год)
for i in range(0, len(rslt3)):
    print(names_value[i], rslt3[i])

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
