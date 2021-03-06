# Антагонистическая игра

## Решение

Основная функция **nash_equilibrium(A)** получает на вход платежную матрицу. 

Данная функция ищет значения седловых точек. Если эта точка единственная, то она и есть решение, иначе решаем задачу в смешанных стратегиях, сводим решение матричной игры к паре двойственных задач линейного программирования и решаем с помощью **linprog** из модуля **SciPy**.

Функция возвращает значение игры и векторы оптимальных стратегий для первого и второго игрока.

Далее с помощью модуля языка Python **matplotlib**, визуализируем спектры стратегий игроков. На графиках отображаются вероятности принять ту или иную стратегию. Приведены примеры игр, в которых:

 (1) Достигается равновесие по Нэшу

 (2) Спектр стратегий не полон

 (3) Спектр стратегий полон


## Необходимое ПО:
**Jupyter Notebook**, библиотеки **NumPy**, **SciPy**, **matplotlib** для Python

## Инструкция по запуску:
В терминале Ubuntu запускаем **jupyter notebook**, выбераем директорию с файлом io-prac-task-1.ipynb и запускаем его.

## Студенты выполнившие задание
*Зеленский Сергей* и *Ларичев Никита*, 311 группа

Все этапы работы были выполненны совместно.
