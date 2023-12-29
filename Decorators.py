def even_num(mode):
    """Декоратор в качестве аргумента принимает номер режима: "1" - для нечетных "2" - для четных,
    при указании иного режимы будет вызвана ошибка Valuerror"""

    def even(func):
        """Декоратор для выполнения функции для четных параметров вызова"""

        def wrapper_even(*args, **kwargs):
            """Осуществляем проверку на четность и тип int"""
            if mode != 1 and mode != 2:
                raise ValueError(
                    "Неправильно задан номер режима, он может быть либо  '1' - для нечетных, либо '2' - для четных")

            for arg in args:
                if arg % 2 == mode % 2 and isinstance(arg, int):
                    return func(*args, **kwargs)

        wrapper_even.__name__ = func.__name__
        wrapper_even.__doc__ = func.__doc__
        wrapper_even.__module__ = func.__module__

        return wrapper_even

    return even


def even_launch_ext(mode):
    """Декоратор позволяет управлять запуском функции для четного или нечетного запуска при этом выбор режима задается
     любым четным или нечетным числом соответственно в качестве аргумента декоратора и может быть результатом какого-то
      функционала для определения режима в зависимости от каких-то условий"""

    def even_launch(func):
        """Декоратор для выполнения функции для четных вызовов функции"""
        count = 0

        def wrapper_even(*args, **kwargs):
            """Осуществляем проверку на четность и тип int"""
            nonlocal count
            count += 1
            for arg in args:
                if (count % 2 == mode % 2 and isinstance(arg, int) and isinstance(mode, int)
                        and isinstance(int(mode), int) and isinstance(int(arg), int)):
                    # print(count)
                    return func(*args, **kwargs)

        wrapper_even.__name__ = func.__name__
        wrapper_even.__doc__ = func.__doc__
        wrapper_even.__module__ = func.__module__

        return wrapper_even

    return even_launch


@even_num(1)
def print_hello(x):
    """Функция выполняет приветственный функционал с заданным номером в виде аргумента, который может быть как
     ID кого-то или чего-то в какой-то БД"""
    print("hello", x)


print_hello(1)
print_hello(2)
print_hello(3)
print_hello(4)


@even_launch_ext(45)
def print_hello(x):
    """Функция выполняет приветственный функционал с заданным номером в виде аргумента, который может быть как
         ID кого-то или чего-то в какой-то БД"""
    print("hello", x)


print_hello(1)
print_hello(2)
print_hello(3)
print_hello(4)


def clip_choose(a=None, k=None):
    """В зависимости от состояния двух аргументов декоратора отличного от None отбрасывает kwargs или
    пробрасывает всё, если оба аргумента декоратора не None, то есть в явном виде указано, что надо и то и то,
    если оба None, то декорируемая функция не вызывается вообще, если args = None, то предупреждает, что возможна ошибка"""

    def clip(f):

        if a is not None and k is None:

            def wrapper_arg_kwarg_rm(*args, **kwargs):
                return f(*args)
        elif a is None and k is not None:
            def wrapper_arg_kwarg_rm(*args, **kwargs):
                print(
                    "декорирование без args: возможна ошибка атрибутов функции, пожалуйста, проверьте и выберите правильный режим декорирования для вашей функции")
                return f(**kwargs)
        elif a is not None and k is not None:
            def wrapper_arg_kwarg_rm(*args, **kwargs):
                return f(*args, **kwargs)
        else:
            def wrapper_arg_kwarg_rm(*args, **kwargs):
                pass

        wrapper_arg_kwarg_rm.__name__ = f.__name__
        wrapper_arg_kwarg_rm.__doc__ = f.__doc__
        wrapper_arg_kwarg_rm.__module__ = f.__module__

        return wrapper_arg_kwarg_rm

    return clip


@clip_choose(a=1)
def print_clip(x, y, z=0, s="~"):
    """Функция отображающая значения введенных аргументов"""
    print(x, y, z, sep=s)


print_clip(1, 2, z=3, s="_")  # 1~2~0
print(1, 2, 3, sep="_")  # 1_2_3

import random


def repeat(x):
    """Функция-внешняя обертка для передачи аргумента в декоратор"""

    def decorator(func):
        """Декоратор, принимающий декорируемый объект(функцию)"""

        def wrapper_repeat(*args, **kwargs):
            """Функция-обертка, добавляющая новый функционал и вызывающая декорируемую функцию """
            result = []
            for i in range(x):
                result.append(func(*args, **kwargs))
            return tuple(result)

        wrapper_repeat.__name__ = func.__name__
        wrapper_repeat.__doc__ = func.__doc__
        wrapper_repeat.__module__ = func.__module__

        return wrapper_repeat

    return decorator


@repeat(2)
def random_sum(n):
    """Функция для вывода суммы рандомных числе в диапазоне, указанном в аргументе функции"""
    return sum(random.random() for i in range(n))


print(random_sum(1_000_000))  # должны получить tuple содержащий 50 сумм миллиона случайных чисел от 0 до 1


def cash(f):
    """Декоратор для одного хэшируемого аргумента для ускорения выполнения нескольких запросов функции"""
    stash = dict()

    def wrapper_cash(*args, **kwargs):
        """Внутренняя функция декоратора"""
        if args[0] in stash.keys():
            return stash[args[0]]
        else:
            stash[args[0]] = f(*args, **kwargs)
            return f(*args, **kwargs)

    wrapper_cash.__name__ = f.__name__
    wrapper_cash.__doc__ = f.__doc__
    wrapper_cash.__module__ = f.__module__

    return wrapper_cash


# для хранения результатов можете, например, создать в этом замыкании словарь cash = dict() где ключами будут аргументы - а значениями return-ы
def cash_general(f):
    """Декоратор для общего случая состава аргументов функции для ускорения выполнения нескольких запросов функции"""
    # stash = dict()

    def wrapper_cash(*args, **kwargs):
        """Внутренняя функция декоратора для общего случая аргументов функций"""
        if str(args) + str(kwargs) in wrapper_cash.results:
            return wrapper_cash.results[str(args) + str(kwargs)]
        else:
            wrapper_cash.results[str(args) + str(kwargs)] = f(*args, **kwargs)

            return f(*args, **kwargs)

    wrapper_cash.__name__ = f.__name__
    wrapper_cash.__doc__ = f.__doc__
    wrapper_cash.__module__ = f.__module__

    wrapper_cash.results = {}
    return wrapper_cash


# class decorator_cash:
#     stash = dict()
#     def __init__(self, func):
#         # self.stash = dict()
#         self.func = func
#
#     def __call__(self, *args, **kwargs):
#         self.args = args
#         self.kwargs = kwargs
#         if str(self.args) + str(self.kwargs) in decorator_cash.stash:
#             return decorator_cash.stash[str(self.args) + str(self.kwargs)]
#         else:
#             decorator_cash.stash[str(self.args) + str(self.kwargs)] = self.func(*args, **kwargs)
#             return self.func(*args, **kwargs)


# @cash
@cash_general
# @decorator_cash
def fib(x):
    """Функция калькуляции числа Фибоначчи от аргумента"""
    print(f"вызвана функция Фибоначчи f({x})")
    if x < 2:
        return 1
    else:
        return fib(x - 1) + fib(x - 2)


print(fib(100))  # здесь при первом вызове функции должны вызваться все f(a) для a из промежутка 0-10

print("Вызван новый вызов")
print(fib(100),
      "новый вызов")  # повторный вызов функции не должен выводить ничего в поток вывода, а сразу выдать значения


# print(fib(4), "новый вызов") # повторный вызов функции не должен выводить ничего в поток вывода а сразу выдать значения

def old_fib(x):
    """Функция калькуляции числа Фибоначчи от аргумента без декоратора"""
    print(f"вызвана функция old Фибоначчи f({x})")
    if x < 2:
        return 1
    else:
        return old_fib(x - 1) + old_fib(x - 2)


print("Вызываем проверку---------------------------------------------------------------------------------------------")
print(fib(100))
# print(fib(1496))
# print(fib(1990))
# print(fib(2450))
# print(len(str(fib(2450))))
print("Вызвана старая функция(недекорированная) ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print(old_fib(20))
