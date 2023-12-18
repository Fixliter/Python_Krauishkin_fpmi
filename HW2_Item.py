class Item:
    """Класс каких-либо предметов"""
    __count = 0
    __count_list = []
    _list_base_tags = {1: "габаритный", 2: "маленький", 3: "скользкий", 4: "твердый", 5: "мягкий", 6: "темный",
                       7: "светлый",
                       8: "съедобный", 9: "несъедобный", 10: "легкий", 11: "хрупкий", 12: "тяжелый"}

    list_items = dict()

    def __init__(self, name="Item_from_json", test_active=0, cost=0):
        if name != "Item_from_json":

            self.name = name
            self._numbers = []
            Item.__count += 1
            Item.__count_list.append(Item.__count)
            self._id_item = Item.__count
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

            Item.list_items[self._id_item] = self

    @property
    def id_item(self):
        """Возвращает ID Item"""
        return self._id_item

    @id_item.setter
    def id_item(self, new_id):
        """Изменяет ID Item и проверяет не существует ли уже iD, данный метод рекомендуется использовать после
         формирования основной базы данных Items, так как не реализована корректировка основного механизма определения
          ID последовательностью count и при штатном добавлении Item возможно дублирование ID,тогда может помочь
           уникальный uid, пока не будет реализована модификация основного механизма создания ID с учетом
            введенных ID вручную"""
        if new_id not in Item.list_items.keys():
            self._id_item = new_id
        else:
            raise ValueError(f"{new_id} - введенный ID уже существует, выберите другой")

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

    # def __hash__(self):
    #     return hash(str(self.id_item)) # - альтернатива по hash

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
        return f"[Item: {self.name}, ID: {self.id_item}, UID: {self.it_uid}, description: {self.descr}, delivery date is {self.deldate} tags:{self._id_tags}, cost is {self.cost}]"

    def __repr__(self):
        """Представление repr для предмета"""
        return f"[Item: {self.name}, ID: {self.id_item}, UID: {self.it_uid}, description: {self.descr}, delivery date is {self.deldate} tags:{self._id_tags}, cost:{self.cost}]"

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
        new_copy._id_item = sorted(Item.__count_list)[-1] + 1
        Item.__count_list.append(new_copy._id_item)
        Item.__count = new_copy._id_item
        return new_copy

    def create_from_json_message(self, json_message):
        """Создает Item из переменной текстового формата json"""
        import json
        data_json = json.loads(json_message)
        print(data_json)
        self.name = data_json["name"]
        self.descr = data_json["descr"]
        self.deldate = data_json["deldate"]
        self._id_item = data_json["id_item"]
        self.it_uid = data_json["it_uid"]
        self._id_tags = data_json["_id_tags"]
        self.cost = data_json["cost"]
        return self

    def create_from_json_file(self, json_path):
        """Создает Item из файла с json текстом"""
        import json
        with open(json_path, 'r') as file_from_path:
            data_json = json.load(file_from_path)
            print(data_json)
            self.name = data_json["name"]
            self.descr = data_json["descr"]
            self.deldate = data_json["deldate"]
            self._id_item = data_json["id_item"]
            self.it_uid = data_json["it_uid"]
            self._id_tags = data_json["_id_tags"]
            self.cost = data_json["cost"]
            # print(self)

    def save_as_json_var(self):
        """Сохраняет Item в переменную текстового формата json)"""
        import json
        data_item = {'name': self.name, 'descr': self.descr, 'deldate': self.deldate_item.strftime('%Y-%m-%d'),
                     'id_item': self.id_item, 'it_uid': str(self.it_uid), 'id_tags': self._id_tags, 'cost': self.cost}
        json_mes = json.dumps(data_item, indent=4)
        return json_mes

    def save_as_json_file(self):
        """Сохраняет Item в файл формата json)"""
        import json
        data_item = {'name': self.name, 'descr': self.descr, 'deldate': self.deldate_item.strftime('%Y-%m-%d'),
                     'id_item': self.id_item, 'it_uid': str(self.it_uid), 'id_tags': self._id_tags, 'cost': self.cost}
        with open('item_result.json', 'w') as file_json_from_item:
            json.dump(data_item, file_json_from_item, indent=4, ensure_ascii=True)

# json_message = """
#         {
#           "name": "диван",
#           "id_item": 12242,
#           "descr": "какой-то диван",
#           "deldate": "2022-01-01",
#           "it_uid": "2dc97de8-3974-4424-bc2e-7b0d36bef067",
#           "_id_tags": {
#             "1": "габаритный",
#             "2": "маленький"
#             },
#           "cost": 500
#         }
#         """
# import json
#
# print(json_message)
# print(type(json_message))
# data = json.loads(json_message)
# print(data)
# for attr in data:
#     print(data[attr])
#     name = data["name"]
#     descr = data["descr"]
#     deldate = data["deldate"]
#     it_uid = data["it_uid"]
#     _id_tags = data["_id_tags"]
#     cost = data["cost"]
#
# new_json = json.dumps(data, indent=2)
# print(new_json)
# with open('item.json', 'w') as file_json:
#     json.dump(data, file_json, indent=4, ensure_ascii=True)
# with open('item.json', 'r') as file:
#     data = json.load(file)
# print(data)

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
# gg.cost = 100
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

# print(f.save_as_json_var())
# f.save_as_json_file()

# json_message = """
#         {
#           "name": "диван",
#           "id_item": 12242,
#           "descr": "какой-то диван",
#           "deldate": "2022-01-01",
#           "it_uid": "2dc97de8-3974-4424-bc2e-7b0d36bef067",
#           "_id_tags": {
#             "1": "габаритный",
#             "2": "маленький"
#             },
#           "cost": 500
#         }
#         """
# f = Item()
# # f.create_from_json_file("item.json")
# f.create_from_json_message(json_message)
# print(f)
# print(g)
# print(gg)
# print(hash(f))
# print(hash(g))
# print(hash(gg))
# print(Item.list_items)
