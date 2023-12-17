class Item:
    """Класс каких-либо предметов"""
    __count = 0
    __count_list = []
    _list_base_tags = {1: "габаритный", 2: "маленький", 3: "скользкий", 4: "твердый", 5: "мягкий", 6: "темный",
                       7: "светлый",
                       8: "съедобный", 9: "несъедобный", 10: "легкий", 11: "хрупкий", 12: "тяжелый"}

    def __init__(self, name, test_active=0, cost=0):
        self.name = name
        self._numbers = []
        Item.__count += 1
        Item.__count_list.append(Item.__count)
        self.id_item = Item.__count
        self._cost = cost
        self.item_test_active = test_active
        self._list_tags = Item._list_base_tags
        # self._list_tags = {1: "габаритный", 2: "маленький", 3: "скользкий", 4: "твердый", 5: "мягкий", 6: "темный",
        #                    7: "светлый",
        #                    8: "съедобный", 9: "несъедобный", 10: "легкий", 11: "хрупкий", 12: "тяжелый"}
        self._id_tags = dict()
        self.descr = ""
        if self.item_test_active == 0:
            self.choose_tags()
            self.description()
            self._delivery_date()
        self._uid_gen()

    def get_id_item(self):
        return self.id_item

    def choose_tags(self):
        """Выбор тегов для предмета или добавление, если отсутствует подходящий"""
        print(
            f"Выберите номера тегов для '{self.name}' через пробел и нажмите Enter или наберите 'new' для добавления нового тега, "
            f"наберите 'pass' для пропуска шага доп.выбора тегов или пустого поля тегов:")
        print(self._list_tags)
        _numbers = input().rstrip().split(" ")
        base = list(self._id_tags.keys())
        __rem_list = []
        if "new" in _numbers:
            self.add_tags()
        elif "pass" in _numbers:
            pass
        else:
            for el in _numbers:
                if int(el) in base:
                    __rem_list.append(el)
                    print(
                        f"Обнаружен тег, который уже присвоен данному Item, он не будет добавлен повторно: {self._id_tags[int(el)]}")
            for rel in __rem_list:
                _numbers.remove(rel)
            for i, tag in enumerate(_numbers):
                self._id_tags[tag] = self._list_tags[int(tag)]
            print(self._id_tags)

    def add_tags(self):
        """Добавление тегов в базовый список с возможностью добавить в список для item"""
        from collections import Counter
        base = list(self._id_tags.values())
        __rem_list = []
        print(f"Запишите новые наименования тегов для '{self.name}' через пробел:")
        _new_tags = input().rstrip().lower().split(" ")

        cnt_sametags = Counter(_new_tags)
        for cel in cnt_sametags:
            if cnt_sametags[cel] > 1:
                for i in range(cnt_sametags[cel] - 1):
                    _new_tags.remove(cel)
        print(cnt_sametags)

        for el in _new_tags:
            if el in base:
                __rem_list.append(el)
                print(
                    f"Обнаружен тег, который уже присвоен данному Item, он не будет добавлен повторно: {el}")
        for rel in __rem_list:
            _new_tags.remove(rel)
        print(f"Хотите ли Вы добавить новые теги для '{self.name}'? Y/N")
        _add_auto = input().strip()
        if _add_auto.upper() == "Y":
            for new_tag in _new_tags:
                key_id_tags = str(len(self._list_tags) + 1)
                self._list_tags[str(len(self._list_tags) + 1)] = new_tag
                self._id_tags[key_id_tags] = new_tag
            self.choose_tags()
        elif _add_auto == "N":
            print(f"Вы можете добавить еще тегов или набрать pass для пропуска")
            self.choose_tags()  # если вдруг захотелось еще добавить тегов из базового списка
        else:
            print(f"Введена неправильная команда")
        print(self._list_tags)
        print(self._id_tags)

    def rm_tags(self):
        """Удаление тегов из списка предмета"""
        print(f"Вы можете удалить конкретные теги для '{self.name}' или удалить все теги")
        print(self._id_tags)
        __selector_del = input(
            f"Наберите 'S' (specific) для удаления конкретных тегов или 'A' (all) для удаления всех тегов для '{self.name}': ").strip()
        if __selector_del.lower() == "s":
            __numbers_del_tags_ = input("Укажите номера тегов через пробел и нажмите Enter: ").rstrip().split(" ")
            for i in __numbers_del_tags_:
                del self._id_tags[i]
        elif __selector_del.lower() == "a":
            self._id_tags.clear()
        else:
            print("Неправильная команда")
            self.rm_tags()

    def __len__(self):
        return len(self._id_tags)

    def __hash__(self):
        return self.id_item

    def _uid_gen(self):
        """Генератор уникального id"""
        import uuid
        self.it_uid = uuid.uuid4()
        return self.it_uid

    def description(self):
        """Текстовое описание предметов и комментарии"""
        print(
            f"Здесь Вы можете добавить описание для '{self.name}' или комментарии по особенностям обращения или доставки для '{self.name}',"
            f"поcле заверщения описания нажмите Enter, для пропуска наберите 'pass' и нажмите Enter")
        self.descr = input().rstrip()
        if self.descr.lower() == "pass":
            self.descr = ""

    def _datecheck(self):
        """Проверка даты отправки предмета"""
        from datetime import datetime, date, time
        if self.deldate == date.today():
            print(f'Сегодня отправляем')
        if self.deldate < date.today():
            print(f'Доставка просрочена')
        if self.deldate > date.today():
            _num_days = (self.deldate - date.today()).days
            print(f'Запланирована отправка через {_num_days} дня')

    def _delivery_date(self):
        """Заполнение даты отправки по предмету"""
        list_dt = []
        print(f'Введите дату отправки для "{self.name}": ')
        dattup = int(input("Введите год: ").strip()), int(input("Введите месяц(1-12): ").strip()), int(
            input("Введите день (1-31): ").strip())
        # list_dt.append(int(input("Введите год: ").strip()))
        # list_dt.append(int(input("Введите месяц (1-12): ").strip()))
        # list_dt.append(int(input("Введите день (1-31): ").strip()))
        import datetime as dt
        self.deldate = dt.date(*dattup)
        # self.ldate = dt.date(*list_dt)
        print(self.deldate)
        # print(self.ldate)
        self._datecheck()

    @property
    def deldate_item(self):
        from dateutil.parser import parse
        _date = parse(str(self.deldate))
        return _date

    @deldate_item.setter
    def deldate_item(self, new_d_date):
        from dateutil.parser import parse
        self.deldate = parse(new_d_date)

    @deldate_item.deleter
    def deldate_item(self):
        print("Дату доставки нельзя сбросить, данную дату можно только перенести(переназначить)")

    def __str__(self):
        """Представление str для предмета"""
        return f"[Item: {self.name}, ID: {self.id_item}, UID: {self.it_uid}, description: {self.descr}, delivery date is {self.deldate} tags:{self._id_tags}]"

    def __repr__(self):
        """Представление repr для предмета"""
        return f"[Item: {self.name}, ID: {self.id_item}, UID: {self.it_uid}, description: {self.descr}, delivery date is {self.deldate} tags:{self._id_tags}]"

    @staticmethod
    def is_tagged(tag: dict):
        for i in tag.values():  # self.id_tags
            yield i

    def choose_tags_for_search(self=None):
        """Выбор набора тегов для поиска совпадений в Item"""
        _search_tags = dict()
        print(
            f"Выберите номера тегов для 'Item' через пробел и нажмите Enter")
        print(Item._list_base_tags)

        _numbers = input().rstrip().split(" ")
        __base = list(_search_tags.keys())
        __rem_list = []
        for el in _numbers:
            if int(el) in __base:
                __rem_list.append(el)
                print(
                    f"Обнаружен тег, который уже есть в списке поиска, он не будет добавлен повторно: {_search_tags[int(el)]}")
        for rel in __rem_list:
            _numbers.remove(rel)
        for i, tag in enumerate(_numbers):
            _search_tags[int(tag)] = Item._list_base_tags[int(tag)]
        return _search_tags

    @property
    def cost(self):
        """Получение цены для Item"""
        print(f"Get cost для '{self.name}'")
        return self._cost

    @cost.setter
    def cost(self, new_cost):
        """Пере/Определение цены для Item"""
        print(f"Set cost для '{self.name}'")
        if not isinstance(new_cost, (int, float)) and new_cost < 0:
            raise ValueError("Цена должна быть положительным числом или нуль")
        self._cost = new_cost

    @cost.deleter
    def cost(self):
        """Удаление цены для Item"""
        print(f"Delete cost для '{self.name}'")
        del self._cost

    def setdef_cost(self):
        """Сброс цены Item в нуль"""
        self._cost = 0

    # cost.setdef_cost = setdef_cost()

    def __lt__(self, other):
        """Реализация операции "меньше чем" для Items"""
        if not isinstance(other.cost, (int, float)) and other.cost < 0:
            raise ValueError("Цена должна быть положительным числом или нуль")
        return self.cost < other.cost

    def __eq__(self, other):
        """Реализация операции "равно" для Items"""
        if not isinstance(other.cost, (int, float)) and other.cost < 0:
            raise ValueError("Цена должна быть положительным числом или нуль")
        return self.cost == other.cost

    def __ge__(self, other):
        """Реализация операции "больше или равно" для Items"""
        if not isinstance(other.cost, (int, float)) and other.cost < 0:
            raise ValueError("Цена должна быть положительным числом или нуль")
        return self.cost >= other.cost

    def __copy__(self):
        """Создает полную непривязанную копию с новым ID и новым Unique ID(UID)"""
        import copy
        new_copy = copy.deepcopy(self)
        new_copy.it_uid = new_copy._uid_gen()
        new_copy.id_item = sorted(Item.__count_list)[-1] + 1
        Item.__count_list.append(new_copy.id_item)
        Item.__count = new_copy.id_item
        return new_copy

# import json
#
# with open("data.json", encoding="UTF-8") as file_in:
#     records = json.load(file_in)
# print(records)


##############################
# Unit test внутри Item функционала Item
# f = Item("диван")
# g = Item("кресло")
# gg = Item("chair")
# print(f.id_item)
# #f.del_tags()
# print(f._id_tags)
# print(f)
# print(len(f))
# print(g.id_item)
# print(gg.id_item)

# f.choose_tags()
# print(f)
# print(len(f._list_tags))
# f.add_tags() #жидкое
# stre = "1 3 4"
# ll = stre.split(" ")
# print(ll)
# _id_tags = dict()
# list_tags = {1: "габаритный", 2: "маленький", 3: "скользкий", 4: "твердый", 5: "мягкий", 6: "темный",
#                      7: "светлый",
#                      8: "съедобный", 9: "несъедобный", 10: "легкий", 11: "хрупкий", 12: "тяжелый"}
# for i, tag in enumerate(ll):
#     _id_tags[tag] = list_tags[int(tag)]
# print(_id_tags)
# del Item

# f.cost = 300
# g.cost = 400
# print(f.cost)
# print(g.cost)
# if f > g:
#     print("f > g")
# if f == g:
#     print("f == g")
# if f >= g:
#     print("f >= g")
# if f < g:
#     print("f < g")
# if f != g:
#     print("f != g")
# if f <= g:
#     print("f <= g")
#
# f.cost = 400
# g.cost = 400
# print(f.cost)
# print(g.cost)
# if f > g:
#     print("f > g")
# if f == g:
#     print("f == g")
# if f >= g:
#     print("f >= g")
# if f < g:
#     print("f < g")
# if f != g:
#     print("f != g")
# if f <= g:
#     print("f <= g")
#
# f.cost = 400
# g.cost = 100
# print(f.cost)
# print(g.cost)
# if f > g:
#     print("f > g")
# if f == g:
#     print("f == g")
# if f >= g:
#     print("f >= g")
# if f < g:
#     print("f < g")
# if f != g:
#     print("f != g")
# if f <= g:
#     print("f <= g")
# f.add_tags()
# print(f)
# # print(f.id_item)
# # print(f.__copy__().id_item)
# # print(f.it_uid)
# # print(f.__copy__().it_uid)
# # print(id(f))
# # print(id(f.__copy__()))
# f.rm_tags()
#
# print(f)
