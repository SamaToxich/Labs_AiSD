# Лабораторная работа №3

С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E заполняется случайным образом целыми числами в интервале [-10,10]. Для тестирования использовать не случайное заполнение, а целенаправленное.

Для ИСТд-13 вид матрицы А:

D Е С В

Для ИСТбд-13 каждая из матриц B,C,D,E имеет вид:

   4
3     1
   2

Вариант 9:

Формируется матрица F следующим образом: если в В количество строк, состоящих из одних нулей в четных столбцах в области 2 больше, чем сумма положительных  элементов в четных строках в области 4, то поменять в С симметрично области 1 и 2 местами, иначе С и Е поменять местами несимметрично. При этом матрица А не меняется. После чего вычисляется выражение: (К  * F) * А – (K * AT) . Выводятся по мере формирования А, F и все матричные операции последовательно.
