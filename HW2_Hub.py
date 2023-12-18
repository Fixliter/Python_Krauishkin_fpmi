import HW2_Item as It
###################################################################
# Создание тестового облегченного Item для debug HUB
# class Item:
#     def __init__(self, name, id, date):
#         """Тестовый облегченный класс Item"""
#         self.name = name
#         self.id = id
#         self.date = date
#
#     def add(self):
#         pass
#
#     def __str__(self):
#         return f"[Items: {self.name}, Date: {self.date}, ID: {self.id}]"
#
#     def __repr__(self):
#         return f"[Items: {self.name}, Date: {self.date}, ID: {self.id}]"
#
#
# f = Item("диван", 1234, "12-02-23")
# g = Item("кресло", 3456, "20230202")
# c = Item("тумба", 12353534, "8 марта 2023")
# ====================================================================================

# Hub должен поддерживать обращение к предметам по индексам и иметь метод добавления предмета в лист _items, поле _date
# с датой в любом формате, а так же быть синглтоном (при любом вызове Hub() возвращается один и тот же инстанс объекта)

from threading import Lock, Thread


class SingletonMeta(type):
    """
    Это потокобезопасная реализация класса Singleton с использованием метакласса.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    У нас теперь есть объект-блокировка для синхронизации потоков во время
    первого доступа к Одиночке.
    """

    def __call__(cls, *args, **kwargs):
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.
        """
        # Теперь представьте, что программа была только-только запущена.
        # Объекта-одиночки ещё никто не создавал, поэтому несколько потоков
        # вполне могли одновременно пройти через предыдущее условие и достигнуть
        # блокировки. Самый быстрый поток поставит блокировку и двинется внутрь
        # секции, пока другие будут здесь его ожидать.
        with cls._lock:
            # Первый поток достигает этого условия и проходит внутрь, создавая
            # объект-одиночку. Как только этот поток покинет секцию и освободит
            # блокировку, следующий поток может снова установить блокировку и
            # зайти внутрь. Однако теперь экземпляр одиночки уже будет создан и
            # поток не сможет пройти через это условие, а значит новый объект не
            # будет создан.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Hub(metaclass=SingletonMeta):
    """Класс на основе паттерна Синглтон"""
    _items = []
    _instance = None
    __password = 111

    def __init__(self, password=111, title="shop", test_active=0):
        from datetime import datetime, date, time
        self.hub_test_active = test_active
        self.password = password
        self.title = title
        self._date = date.today()
        while self.password != Hub.__password:
            break



    # def add_item(func):
    #     def inner(*args, **kwargs):
    #         for i in range(1, len(args)):
    #             print(args[i])
    #             if isinstance(args[i], It.Item):
    #                 return func(args[i], **kwargs)
    #             else:
    #                 raise ValueError("Объект не является классом или наследником класса")
    #
    #     inner.__name__ = func.__name__
    #     inner.__doc__ = func.__doc__
    #     inner.__module__ = func.__module__
    #     return inner

    # @add_item
    def __add_item__(self, *args):
        """Добавление предмета в список"""
        for item in args:
            if isinstance(item, It.Item):
                self._items.append(item)
            else:
                raise ValueError("Объект не является классом или наследником класса")

    def __add_new_item__(self):
        """Добавление нового предмета"""
        new_name = input("Введите название Item: ")
        temp = It.Item(new_name)
        self.__add_item__(temp)  # ДОРАБОТАТЬ

    def __del_item__(self, item):
        """Удаление предмета по значению (первое вхождение)"""
        self._items.remove(item)

    def __del_index_item__(self, index):
        """Удаление предмета по индексу"""
        self._items.pop(index)

    def rm_item(self, i):
        """Удаление item"""
        if type(i) is int:
            self.__del_index_item__(self.find_by_id(i)[0])
            print(f"Удаление item: {i} по ID")

        if isinstance(i, It.Item):
            self.__del_index_item__(self.find_by_id(i.id_item)[0])
            print(f"Удаление item: {i}")

    def drop_items(self, items):
        """Удаление списка items"""
        for i in items:
            if isinstance(i, It.Item):
                self.__del_index_item__(self.find_by_id(i.id_item)[0])
                print(f"Удаление item: {i}")

    def __clear_items__(self):
        """Очистка всего списка предметов"""
        print(f"Очистка списка Items для {self.title}")
        self._items.clear()

    def find_by_startswith(self, start):
        """Возвращает список Items найденных по вхождению строки в название"""
        found_list = []
        for i in self._items:
            if i.name.startswith(str(start).lower()):
                found_list.append(i)
        if len(found_list) < 1:
            print(f"Ничего не найдено по '{start}'")
            # return found_list  # - если понадобится выводить пустой список
        else:
            return found_list

    def find_by_id(self, id):
        """Выдает (pos, Item) по ID или  (-1, None) если не нашло"""
        __count = -1
        for i in self:
            __count += 1
            if i.id_item == id:
                # print(__count, i)
                return tuple([__count, i])
        return tuple([-1, None])

    def find_by_tags(self):
        self._found = []
        _search_tags_tuple = ()
        _item_tags_tuple = ()
        _search_tags = It.Item.choose_tags_for_search()

        for n in It.Item.is_tagged(_search_tags):
            _temp1 = (n,)
            _search_tags_tuple += _temp1
        print(_search_tags_tuple)
        for i in self:
            _item_tags_tuple = ()
            for n in It.Item.is_tagged(i._id_tags):
                _temp2 = (n,)

                _item_tags_tuple += _temp2
            if hash(_item_tags_tuple) == hash(_search_tags_tuple):
                print(f"Попался {i}")
                self._found.append(i)
            del _temp2
            del _item_tags_tuple
        return self._found

    def find_by_date(self, *args):
        """Поиск Items о дате, если введены две даты - в промежутке между датами, если введена одна дата - то все Item c датами до введенной"""
        from dateutil.parser import parse
        from datetime import datetime, date, time
        dates_check = []
        found_by_date = []
        for i in args:
            dates_check.append(parse(i))
        if len(dates_check) == 1:
            for item in self._items:
                if item.deldate_item <= dates_check[0]:
                    found_by_date.append(item)
            print(f' Найдено по дате до {dates_check[0]}: {found_by_date}')
            return found_by_date
        if len(dates_check) == 2:
            dates_check.sort()
            for item in self._items:
                if dates_check[0] <= item.deldate_item <= dates_check[1]:
                    found_by_date.append(item)
            print(f' Найдено по дате от {dates_check[0]} и до {dates_check[1]}: {found_by_date}')
            return found_by_date
        if len(dates_check) > 2:
            raise ValueError("Слишком много введено дат")

    def find_most_valuable(self, amount=1):
        """Поиск самых дорогих Items"""
        sorted_by_cost_items = sorted(self._items, key=lambda x: x.cost, reverse=True)
        print(sorted_by_cost_items)
        _most_valuable = []
        if len(self) < amount:
            for i in range(len(self)):
                _most_valuable.append(sorted_by_cost_items[i])
            print(_most_valuable)
            return _most_valuable
        else:
            for i in range(amount):
                _most_valuable.append(sorted_by_cost_items[i])
            print(_most_valuable)
            return _most_valuable

    @property
    def date_hub(self):
        return self._date

    @date_hub.setter
    def date_hub(self, new_date):
        from dateutil.parser import parse
        self._date = parse(new_date)

    @date_hub.deleter
    def date_hub(self):
        import datetime
        print(f"Сброс даты {self.date_hub} для {self.title}")
        self._date = datetime.date(1, 1, 1).isoformat()

    def outdated(self, date):
        from dateutil.parser import parse
        self.date_hub = date
        return self.find_by_date(str(self.date_hub))

    # def __new__(cls, *args, **kwargs):
    # """Синглтон через класс new (не решена проблема многопоточности, но альтернатива создания Синглтона)"""

    #     if cls._instance is None:
    #         cls._instance = object.__new__(cls, *args, **kwargs)
    #     return cls._instance

    def __del__(self):
        """Удаление синглтона"""
        print("Удаление экземпляра: " + str(self))
        Hub._instance = None

    def __str__(self):
        """Представление str"""
        return f"HUB: {self.title}, Items: {self._items}, Date: {self.date_hub}"

    def __repr__(self):
        """Представление repr"""
        return f"HUB: {self.title}, Items: {self._items}, Date: {self.date_hub}"

    def __getitem__(self, position):
        """Обращение к предметам по индексам"""

        return self._items[position]

    def __len__(self):
        """Выдает количество предметов"""
        return len(self._items)

    def __reversed__(self):
        """Переворачивает список предметов"""
        return self._items[::-1]

    def info(self):
        """Вывод инфо о Hub"""
        self.__str__()

    def save_as_json_var(self):
        """Сохраняет содержимое Hub в переменную текстового формата json)"""
        import json
        data_hub = {'title': self.title, 'Items:': self._items.__repr__(),
                    'date_hub': self.date_hub.strftime('%Y-%m-%d')}
        json_mes = json.dumps(data_hub, indent=4)
        return json_mes

    def save_as_json_file(self):
        """Сохраняет содержимое Hub в файл формата json)"""
        import json
        data_hub = {'title': self.title, 'Items:': self._items.__repr__(),
                    'date_hub': self.date_hub.strftime('%Y-%m-%d')}
        with open('hub_result.json', 'w') as file_json_from_hub:
            json.dump(data_hub, file_json_from_hub, indent=4, ensure_ascii=True)

    def read_from_json_var(self, json_var):
        """Создает Hub из переменной текстового формата json"""
        import json
        data_json = json.loads(json_var)
        print(data_json)
        self.title = data_json["title"]
        self._items = data_json['Items:']
        self.date_hub = data_json["date_hub"]
        return self

    def read_from_json_file(self, json_path):
        """Создает Hub из файла формата json"""
        import json
        with open(json_path, 'r') as file_from_path:
            data_json = json.load(file_from_path)
            print(data_json)
        self.title = data_json["title"]
        self._items = data_json['Items:']
        self.date_hub = data_json["date_hub"]
        return self


##Тест на синглтон 1
# FOO = Hub(f, "Foo", "Foo")
# Boom = Hub(f, "Boom", "Boom")
# FOO.info()
# Boom.info()
# print(FOO._items)


###Тест на синглтон 2
# def test_singleton(items, date, hub) -> None:
#     singleton = Hub(items, date, hub)
#     print(singleton._date, singleton._hub, singleton._items)
# if __name__ == "__main__":
#     # Клиентский код.
#     print("If you see the same value, then singleton was reused (yay!)\n"
#           "If you see different values, "
#           "then 2 singletons were created (booo!!)\n\n"
#           "RESULT:\n")
#
#     process1 = Thread(target=test_singleton, args=("FOO","FOO","FOO" ))
#     process2 = Thread(target=test_singleton, args=("BAR","BAR","BAR" ))
#     process1.start()
#     process2.start()

# Item должен иметь уникальный _id, наименование, описание, дату, в которую он должен быть отправлен а так же множество
# тегов _tags. Должен поддерживать добавление и удаление тегов. (В нашей задаче теги это просто строки ненулевой длинны,
# например "Хрупкий", "Скоропортящийся" и т.д.)
#############################################
# Тест получения Item
# f = It.Item("диван")
# g = It.Item("кресло")
# c = It.Item("тумба")
# FOO = Hub(112, "Magazin")
# FOO.__add_item__(f)
# FOO.__add_item__(g)
# FOO.__add_item__(c)
# print(FOO)
###################################################
# Тест некоторого функционала HUB
# print(FOO._items)
# print(FOO[2])
# print(len(FOO))
# print(reversed(FOO))
# #FOO.__del_item__(f)
# print(FOO._items)
# FOO.__del_index_item__(0)
# print(FOO._items)
# FOO.__clear_items__()
# print(FOO._items)
# print(FOO._date)
#######################################################
# Тест заброса Item и проверки
# h1 = Hub(112, "Shop")
# h2 = Hub(112, "Point")
# print("Пытаемся задать пару инстансов в Hub")
# if h1 is h2:
#     print("Hub выполняет функционал Синглтона")
# else:
#     print("Два объекта Hub не являются одним инстансом")
# print("Hub выполняет функционал Синглтона" if h1 is h2 else "Два объекта Hub не являются одним инстансом")
#
# item1 = It.Item("диван")
# item2 = It.Item("кресло")
# item1._id_tags = {1: "габаритный", 2: "маленький", 3: "скользкий", 4: "твердый"}
# item1.descr = "Грузить вместе"
# item1.deldate = "2023-01-01"
# item1.ldate = "2023-01-01"
# item2._id_tags = {9: "несъедобный", 10: "легкий", 11: "хрупкий"}
# item2.descr = "Ответственный: Куприянов В.С."
# item2.deldate = "2023-12-23"
# item2.ldate = "2023-12-23"
# print("Item создаёт разные id" if item1.id_item != item2.id_item else "Item не создаёт разные id")
# h1.__add_item__(item1)
# print(h1)
# h1.__add_item__(item2)
# print(h1)
# print(h2)
# h1.__add_new_item__()

# h1 = Hub(112, "Shop")
# h1.__add_new_item__()
# print(h1)

# h1 = Hub(112, "Shop")
#
# f = It.Item("диван")
# h1.__add_item__(f)
# print(h1)
# print("Проверяем на дубликаты")
# f.choose_tags()
# print(f)
# del h1
# print(h1)

# g = It.Item("кресло")
# c = It.Item("тумба")
# f = It.Item("диван")
# e = It.Item("кровать")
# r = It.Item("комод")
# t = It.Item("табуретка")
# h1.find_by_id(2)

# g.cost = 100
# c.cost = 200
# f.cost = 12
# e.cost = 1200
# r.cost = 500
# t.cost = 10

# h1.__add_item__(g)
# h1.__add_item__(c)
# h1.__add_item__(f)
# h1.__add_item__(e)
# h1.__add_item__(r)
# h1.__add_item__(t)
# h1.__add_item__(g, c, f, r, t)
# print(h1)
# # for i in h1:
# #     if i.id_item == 3:
# #         print(i)
# # print(h1.find_by_id(3))
# print(h1.find_by_tags())
# print(h1.find_by_id(2)[0], "Нашел позицию ")

# h1.rm_item(f)
# h1.rm_item(c.get_id_item())
# print(h1)
# h1.__del_item__(f)
# l1 = [g,f]
# h1.drop_items(l1)
# print(h1)
# h1.__clear_items__()
# print(h1, "После чистки")


# print(h1.date_hub)
# h1.date_hub = "Mon, 21 March, 2024"
# print(h1.date_hub)
# del h1.date_hub
# print(h1.date_hub)

# h1.find_by_date("21 March, 2024")
# h1.find_by_date("21 March, 2024", "21 March, 2025")
# h1.find_by_date("21 March, 2024", "21 March, 2025", "21 March, 2025")

# k = 1
# h1.__add_item__(k)
# print(h1)

# h1.find_most_valuable()
# h1.find_most_valuable(10)


# print(h1.find_by_startswith("кр"))
# print(h1.find_by_startswith("р"))

# outdated = h1.outdated("21 March, 2024")
# print(outdated)

# print(h1.save_as_json_var())
# print(h1.save_as_json_file())

# h1 = Hub()
# u = """{
#     "title": "Shop",
#     "Items:": "[[Item: \u043a\u0440\u0435\u0441\u043b\u043e, ID: 1, UID: 79a740fc-9123-4bd9-a697-d811ec194ab4, description: dg, delivery date is 0002-02-02 tags:{'1': '\u0433\u0430\u0431\u0430\u0440\u0438\u0442\u043d\u044b\u0439', '2': '\u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0439', '3': '\u0441\u043a\u043e\u043b\u044c\u0437\u043a\u0438\u0439', '4': '\u0442\u0432\u0435\u0440\u0434\u044b\u0439'}, cost:100], [Item: \u0442\u0443\u043c\u0431\u0430, ID: 2, UID: 55b0f9a8-6152-4b33-9886-d4f3f4afe038, description: fg, delivery date is 0203-03-03 tags:{'2': '\u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0439', '9': '\u043d\u0435\u0441\u044a\u0435\u0434\u043e\u0431\u043d\u044b\u0439'}, cost:200]]",
#     "date_hub": "2023-12-18"
# }"""
# h1.read_from_json_var(u)
# h1.read_from_json_file("hub_result.json")
# print(h1)
