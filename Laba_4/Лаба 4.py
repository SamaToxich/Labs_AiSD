""" С клавиатуры вводятся два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц,
B, C, D, E заполняется случайным образом целыми числами в интервале [-10,10]. Для тестирования использовать не случайное
заполнение, а целенаправленное.
Вид матрицы А:
D	Е
С	В
Для простоты все индексы в подматрицах относительные.
По сформированной матрице F (или ее частям) необходимо вывести не менее 3 разных графика.
Программа должна использовать функции библиотек numpy  и mathplotlib

Вариант 9:
Формируется матрица F следующим образом: скопировать в нее "А" и если в "В" количество строк, состоящих из одних нулей
в четных столбцах больше, чем сумма положительных  элементов в четных строках, то поменять местами C и E симметрично,
иначе В и Е поменять местами несимметрично. При этом матрица А не меняется. После чего если определитель матрицы А
больше суммы диагональных элементов матрицы F, то вычисляется выражение: A^-1 * AT – K * F^-1, иначе вычисляется
выражение (AТ + G - FТ) * K, где G-нижняя треугольная матрица, полученная из А. Выводятся по мере формирования А,
F и все матричные операции последовательно. """

from math import ceil
import random as r
import numpy as np
from matplotlib import pyplot as plt


def heatmap(data, row_labels, col_labels, ax, cbar_kw=None, **kwargs):  # аннотированная тепловая карта
    if cbar_kw is None:
        cbar_kw = {}
    im = ax.imshow(data, **kwargs)
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)
    return im, cbar


def annotate_heatmap(im, data=None, textcolors=("black", "white"), threshold=0):
    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()
    kw = dict(horizontalalignment="center", verticalalignment="center")
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(data[i, j] > threshold)])
            text = im.axes.text(j, i, data[i, j], **kw)
            texts.append(text)
    return texts


try:
    n = int(input('Введите число N: '))
    k = int(input('Введите число K: '))
    while n < 5:
        n = int(input('Введите число N больше 4: '))

    cnt_b2 = sum_ch4 = sum_det_F = 0
    middle_n = n // 2 + n % 2  # Середина матрицы
    A = np.zeros((n, n))  # Задаём матрицу A
    for i in range(n):
        for j in range(n):
            A[i][j] = r.randint(-10, 10)
    AT = np.transpose(A)  # Транспонированная матрица А
    A_obr = np.linalg.inv(A)  # Обратная матрица А
    det_A = np.linalg.det(A)  # Определитель матрицы А
    F = A.copy()  # Задаём матрицу F
    G = np.zeros((n, n))  # Заготовка матрицы G

    print('\nМатрица А:')
    print(A)
    print('\nТранспонированная А:')
    print(AT)

    # Выделяем матрицы E C B
    if n % 2 == 1:
        E = [A[i][middle_n - 1:n] for i in range(middle_n)]
        C = [A[i][0:middle_n] for i in range(middle_n - 1, n)]
        B = [A[i][middle_n - 1:n] for i in range(middle_n - 1, n)]
    else:
        E = [A[i][middle_n:n] for i in range(0, middle_n)]
        C = [A[i][0:middle_n] for i in range(middle_n, n)]
        B = [A[i][middle_n:n] for i in range(middle_n, n)]

    for i in range(middle_n):  # Проверяем, что в чётных столбцах в матрице "В" всё значения равны 0
        l_cnt = zero_cnt = 0
        for j in range(middle_n):
            if (j + 1) % 2 == 0:
                l_cnt += 1
                if B[i][j] == 0:  # Считаем кол-во подходящих строк
                    zero_cnt += 1
        if l_cnt == zero_cnt and l_cnt > 0:
            cnt_b2 += 1

    for i in range(middle_n):  # Считаем сумму положительных элементов в чётных строках в матрице B
        for j in range(middle_n):
            if (i + 1) % 2 == 0:
                if B[i][j] > 0:
                    sum_ch4 += int(B[i][j])

    if cnt_b2 > sum_ch4:
        print(f'\nВ матрице "В" количество строк с нулями на чётных позициях в области 2({cnt_b2})')
        print(f'больше чем сумма чётных строк в области 4({sum_ch4})')
        print('поэтому симметрично местами подматрицы C и E:')
        C, E = E, C
        for i in range(middle_n):
            C[i] = C[i][::-1]  # Симметрично меняем значения в C
            E[i] = E[i][::-1]  # Симметрично меняем значения в E
        if n % 2 == 1:
            for i in range(middle_n - 1, n):  # Перезаписываем С
                for j in range(middle_n):
                    F[i][j] = C[i - (middle_n - 1)][j]
            for i in range(middle_n):  # Перезаписываем Е
                for j in range(middle_n - 1, n):
                    F[i][j] = E[i][j - (middle_n - 1)]
        else:
            for i in range(middle_n, n):
                for j in range(middle_n):
                    F[i][j] = C[i - middle_n][j]
            for i in range(0, middle_n):
                for j in range(middle_n, n):
                    F[i][j] = E[i][j - middle_n]
    else:
        print(f'\nВ матрице "В" количеств строк с нулями на чётных позициях({cnt_b2})')
        print(f'меньше суммы чётных строк({sum_ch4}) или равно ей')
        print('поэтому несимметрично меняем местами подматрицы B и E:')
        B, E = E, B
        if n % 2 == 1:
            for i in range(middle_n - 1, n):  # Перезаписываем B
                for j in range(middle_n - 1, n):
                    F[i][j] = B[i - (middle_n - 1)][j - (middle_n - 1)]
            for i in range(middle_n):  # Перезаписываем Е
                for j in range(middle_n - 1, n):
                    F[i][j] = E[i][j - (middle_n - 1)]
        else:
            for i in range(middle_n, n):
                for j in range(middle_n, n):
                    F[i][j] = B[i - middle_n][j - middle_n]  # Перезаписываем B
            for i in range(0, middle_n):
                for j in range(middle_n, n):
                    F[i][j] = E[i][j - middle_n]  # Перезаписываем Е

    print('\nМатрица F:')
    print(F)
    # Сумма диагональных элементов матрицы F
    for i in range(n):
        for j in range(n):
            if i == j:
                sum_det_F += F[i][j]
            if (i + j + 1) == n and ((i == j) != ((i + j + 1) == n)):
                sum_det_F += F[i][j]

    if det_A > sum_det_F:
        print(f'\nОпределитель матрицы А({int(det_A)})')
        print(f'больше суммы диагональных элементов матрицы F({int(sum_det_F)})')
        print('поэтому вычисляем выражение: A^-1 * AT – K * F^-1:')

        try:
            F_obr = np.linalg.inv(F)  # Обратная матрица F
            KF_obr = F_obr * k  # K * F^-1
            A_obrAT = np.matmul(A_obr, AT)  # A^-1 * AT
            result = A_obrAT - KF_obr  # A^-1 * AT – K * F^-1

            print('\nОбратная матрица F:')
            print(F_obr)
            print('\nРезультат K * F^-1:')
            print(KF_obr)
            print("\nРезультат A_obr * AT:")
            print(A_obrAT)
            print('\nРезультат (К * F) * А – K * AT:')
            print(result)
        except np.linalg.LinAlgError:
            print("Одна из матриц является вырожденной (определитель равен 0),"
                  " поэтому обратную матрицу найти невозможно.")
    else:
        print(f'\nОпределитель матрицы А({int(det_A)})')
        print(f'меньше суммы диагональных элементов матрицы F({int(sum_det_F)}) или равен ей')
        print('поэтому вычисляем выражение (AТ + G - FТ) * K:')

        FT = np.transpose(F)  # Транспонированная матрица F

        for i in range(n):
            for j in range(n):
                if i >= j and (i + j + 1) >= n:
                    G[i][j] = A[i][j]

        ATG = AT + G  # AТ + G
        ATGFT = ATG - FT  # AT + G - FT
        result = ATGFT * k  # (AТ + G - FТ) * K

        print('\nТранспонированная матрица F:')
        print(FT)
        print('\nМатрица G:')
        print(G)
        print('\nРезультат AТ + G:')
        print(ATG)
        print('\nРезультат AТ + G - FT:')
        print(ATGFT)
        print('\nРезультат (AТ + G - FТ) * K:')
        print(result)

    av = [np.mean(abs(F[i, ::])) for i in range(n)]
    av = int(sum(av))  # сумма средних значений строк (используется при создании третьего графика)
    fig, axs = plt.subplots(2, 2, figsize=(11, 8))
    x = list(range(1, n + 1))
    for j in range(n):
        y = list(F[j, ::])  # обычный график
        axs[0, 0].plot(x, y, ',-', label=f"{j + 1} строка.")
        axs[0, 0].set(title="График с использованием функции plot:", xlabel='Номер элемента в строке',
                      ylabel='Значение элемента')
        axs[0, 0].grid()
        axs[0, 1].bar(x, y, 0.4, label=f"{j + 1} строка.")  # гистограмма
        axs[0, 1].set(title="График с использованием функции bar:", xlabel='Номер элемента в строке',
                      ylabel='Значение элемента')
        if n <= 10:
            axs[0, 1].legend(loc='lower right')
            axs[0, 1].legend(loc='lower right')
    explode = [0] * (n - 1)  # отношение средних значений от каждой строки
    explode.append(0.1)
    sizes = [round(np.mean(abs(F[i, ::])) * 100 / av, 1) for i in range(n)]
    axs[1, 0].set_title("График с использованием функции pie:")
    axs[1, 0].pie(sizes, labels=list(range(1, n + 1)), explode=explode, autopct='%1.1f%%', shadow=True)

    im, cbar = heatmap(F, list(range(n)), list(range(n)), ax=axs[1, 1], cmap="magma_r")
    texts = annotate_heatmap(im)
    axs[1, 1].set(title="Создание аннотированных тепловых карт:", xlabel="Номер столбца", ylabel="Номер строки")
    plt.suptitle("Использование библиотеки matplotlib")
    plt.tight_layout()
    plt.show()

    print('\nРабота программы завершена.')
except ValueError:  # ошибка на случай введения не числа в качестве порядка или коэффициента
    print('\nВведенный символ не является числом. Перезапустите программу и введите число.')
