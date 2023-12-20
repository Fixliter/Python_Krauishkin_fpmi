import unittest
import HW2_Hub as h
import HW2_Item as It

password = 111
title = "shop"
test_active = 1


class TestHub(unittest.TestCase):
    def setUp(self):
        """Создание тестовых инстансов"""

        print(f"Загрузка данных для {self}")
        self.hub1 = h.Hub(password, title, 1)
        self.hub2 = h.Hub(password, title, 1)

    def tearDown(self):
        del self.hub1
        del self.hub2

    def test_hub_singleton(self):
        """Проверка того что hub - синглтон, сравнивая созданные два инстанса класса Hub:"""
        print(f"Выполняется {self}")
        self.assertTrue(self.hub1 is self.hub2)
        print("Проверка того что hub - синглтон прошла УСПЕШНО")

    def test_hub_len(self):
        """Проверка того что при добавлении предметов меняется значение len(item), вызывая несколько раз метод класса
        Hub __add_item__ и добавляя Item в список"""
        print(f"Выполняется {self}")
        temp_item = []
        for i in range(5):
            temp_item.append(It.Item("стул", 1))
            self.hub1.__add_item__(temp_item[i])
            It.Item.deldate = "2023-01-01"
        # print(temp_item)
        # print(self.hub1)
        self.assertEqual(len(self.hub1), 5,
                         f"Количество добавленных предметов не соответствует результату метода Len()")
        print(
            f"Проверка добавления предметов и метода len прошла УСПЕШНО, добавлено {len(self.hub1)} - ожидалось  - 5 ")
        self.hub1.__clear_items__()
        temp_item.clear()
        # print(temp_item)
        # print(self.hub1)

    def test_hub_add_item(self):
        """Проверка добавления нескольких item"""
        print(f"Выполняется 'test_hub_add_item'")
        for i in range(3):
            for item in TestItem.gen_item():
                print(item)
                self.hub1.__add_item__(item)
        self.assertEqual(len(self.hub1), 3,
                         f"Количество добавленных предметов не соответствует результату метода Len() после добавления Items")
        print(
            f"Проверка добавления предметов и метода len прошла УСПЕШНО, добавлено {len(self.hub1)} - ожидалось  - 5 ")
        self.hub1.__clear_items__()

    def test_hub_add_new_item(self):
        """Проверка вызова создания нового Item от Hub и добавление его в Hub"""
        print(f"Выполняется 'test_hub_add_new_item'")
        self.hub1.__add_new_item__()
        print(self.hub1)
        self.assertEqual(len(self.hub1), 1,
                         f"Количество добавленных предметов не соответствует результату метода Len() после создания и добавления нового Item")
        print(
            f"Проверка создания нового item от Hub и добавления в Hub прошла УСПЕШНО, добавлено {len(self.hub1)} - ожидалось  - 1 ")
        self.hub1.__clear_items__()

    def test_hub_del_index_item(self):
        """Проверка удаления item по индексу из Hub"""
        print(f"Выполняется 'test_hub_del_index_item'")
        for i in range(3):
            for item in TestItem.gen_item():
                print(item)
                self.hub1.__add_item__(item)
        print(self.hub1)
        temp_it = self.hub1.__getitem__(0)
        self.hub1.__del_index_item__(0)
        print(self.hub1)
        self.assertEqual(len(self.hub1), 2,
                         f"Количество  предметов не соответствует результату метода Len() после добавления 3 Item и удаления одного Item")
        self.assertNotIn(temp_it, self.hub1._items, f"Item ({temp_it}) не удален из Hub")
        print(
            f"Проверка удаления Item по индексу из Hub прошла УСПЕШНО")
        self.hub1.__clear_items__()

    def test_hub_del_item(self):
        """Проверка удаления item по первому вхождению из Hub"""
        print(f"Выполняется 'test_hub_del_item'")
        for i in range(3):
            for item in TestItem.gen_item():
                print(item)
                self.hub1.__add_item__(item)
                if i == 0:
                    temp_it = item
        print(self.hub1)
        self.hub1.__del_item__(temp_it)
        print(self.hub1)
        self.assertEqual(len(self.hub1), 2,
                         f"Количество предметов не соответствует результату метода Len() после добавления 3 Item и удаления одного Item")

        self.assertNotIn(temp_it, self.hub1._items, f"Item ({temp_it}) не удален из Hub")
        print(
            f"Проверка удаления Item по первому вхождению в Hub прошла УСПЕШНО")
        self.hub1.__clear_items__()

    def test_hub_rm_item(self):
        """Проверка удаления item по первому вхождению из Hub"""
        print(f"Выполняется 'test_hub_rm_item'")
        for i in range(3):
            for item in TestItem.gen_item():
                print(item)
                self.hub1.__add_item__(item)
                if i == 0:
                    temp_it = item
        print(self.hub1)
        self.hub1.rm_item(temp_it)
        print(self.hub1)
        self.assertEqual(len(self.hub1), 2,
                         f"Количество предметов не соответствует результату метода Len() после добавления 3 Item и удаления одного Item")

        self.assertNotIn(temp_it, self.hub1._items, f"Item ({temp_it}) не удален из Hub")
        print(
            f"Проверка удаления Item по первому вхождению в Hub прошла УСПЕШНО")
        self.hub1.__clear_items__()

    def test_hub_drop_items(self):
        """Проверка удаления коллекции(списка) items из Hub"""
        print(f"Выполняется 'test_hub_drop_items'")
        temp_it = []
        for i in range(5):
            for item in TestItem.gen_item():
                self.hub1.__add_item__(item)
                if i == 0 or i == 2 or i == 3:
                    temp_it.append(item)
        print(temp_it)
        print(self.hub1)
        self.hub1.drop_items(temp_it)
        print(self.hub1)
        self.assertEqual(len(self.hub1), 2,
                         f"Количество предметов не соответствует результату метода Len() после добавления 3 Item и удаления одного Item")
        for elem in temp_it:
            self.assertNotIn(elem, self.hub1._items, f"Item ({temp_it}) не удален из Hub")
        print(
            f"Проверка удаления Item по первому вхождению в Hub прошла УСПЕШНО")
        self.hub1.__clear_items__()

    def test_hub_clear_items(self):
        """Проверка очистки списка items Hub"""
        print(f"Выполняется 'test_hub_clear_items'")
        temp_it = []
        for i in range(5):
            for item in TestItem.gen_item():
                self.hub1.__add_item__(item)
        print(self.hub1)
        self.hub1.__clear_items__()
        print(self.hub1)
        self.assertEqual(len(self.hub1), 0,
                         f"Количество предметов (нуль предметов) не соответствует результату метода Len() после очистки списка Items")
        empty_list = []
        self.assertEqual(self.hub1._items, empty_list, f"Список Items в Hub не очищен")
        print(
            f"Проверка удаления Item по первому вхождению в Hub прошла УСПЕШНО")
        self.hub1.__clear_items__()


class TestItem(unittest.TestCase):
    def setUp(self):
        print(f"Загрузка данных для {self}")
        self.item1 = It.Item("шкаф", 1)
        self.item2 = It.Item("софа", 1)
        self.item3 = It.Item("тумба", 1)
        self.item1._id_tags = {1: "габаритный", 2: "маленький", 3: "скользкий", 4: "твердый"}
        self.item1.descr = "Грузить вместе"
        self.item1.deldate = "2023-01-01"
        self.item1.ldate = "2023-01-01"
        self.item2._id_tags = {9: "несъедобный", 10: "легкий", 11: "хрупкий"}
        self.item2.descr = "Ответственный: Куприянов В.С."
        self.item2.deldate = "2023-12-23"
        self.item2.ldate = "2023-12-23"
        self.item3._id_tags = {9: "несъедобный", 10: "легкий", 11: "хрупкий"}
        self.item3.descr = "Документы УПД у водителя"
        self.item3.deldate = "2024-01-21"
        self.item3.ldate = "2024-01-21"

    def tearDown(self):
        del self.item1
        del self.item2
        del self.item3

    def test_item_id(self):
        """Проверка того что у разных Items разные id. Проверяем, создавая два или более Item"""
        print(f"Выполняется {self}")
        print(
            f"Item создаёт разные id: {self.item1.id_item} и {self.item2.id_item}" if self.item1.id_item != self.item2.id_item else "Item не создаёт разные id")
        self.assertTrue(self.item1.id_item != self.item2.id_item, f"Разные Items имеют одинаковые id")
        self.assertTrue(self.item1.it_uid != self.item2.it_uid, f"Разные Items имеют одинаковые id")
        print("Проверка на создание разных ID прошла УСПЕШНО")

        # Реализована проверка того, что у разных Items разные id разным синтаксисом

    def test_item_len(self):
        """Проверка того что при добавлении тэгов меняется значение len(item)"""

        item4 = It.Item("диван", 1)
        item4._id_tags = {1: "габаритный", 2: "маленький", 3: "скользкий", 4: "твердый"}
        __l1 = len(item4._id_tags)
        item4.descr = "Грузить вместе"
        item4.deldate = "2023-01-01"
        item4.ldate = "2023-01-01"
        print(item4._id_tags)
        print(f"Выполняется {self}")
        item4.choose_tags()
        __l2 = len(item4._id_tags)
        self.assertEqual(len(item4), len(item4._id_tags), f"Результаты метода Len() не совпадают")
        print(
            f"Проверка прошла УСПЕШНО, было {__l1} tags, добавлено {__l2 - __l1} tags, в результате всего {len(item4._id_tags)} tags")
        del item4
        # Реализована проверку того, что при добавлении тэгов меняется значение len(item)

    def test_equal_tags(self):
        """Проверка того что если к предмету добавить два идентичных тега - их количество будет один"""
        item5 = It.Item("тумба", 1)
        item5.descr = "Грузить вместе"
        item5._id_tags = {1: "габаритный", 2: "маленький", 3: "скользкий", 4: "твердый"}
        item5.deldate = "2023-01-01"
        print(f"Выполняется {self}")
        item5.choose_tags()
        from collections import Counter
        cnt_sametags = Counter(item5._id_tags.values())
        for k in cnt_sametags:
            self.assertTrue(cnt_sametags[k] == 1, f"Теги повторяются, счетчики тегов: {cnt_sametags}")

        # for i in range(len(cnt_sametags)):
        # self.assertTrue([*cnt_sametags.values()][i] == 1, f"Теги повторяются, счетчики тегов: {cnt_sametags}")
        # print(int([*cnt_sametags.values()][i]) == 1)

    @staticmethod
    def gen_item():
        import random
        import datetime
        import uuid

        gen_name = random.choice(["диван", "кресло", "комод", "стул", "стол", "шкаф", "тумба", "лампа", "мяч"])
        item_gen = It.Item(gen_name, 1)
        item_gen.descr = gen_descr = random.choice(
            ["Документы подписать", "Передать водителю", "Реализовать первым", "С повреждением", "б.у.",
             "После восстановления", "Новый", "Иванову", "Продано"])
        item_gen.id_item = gen_item_id = random.randint(1, 111111111111)
        item_gen.deldate_item = gen_deldate = str(datetime.date(2009, 12, 4) + datetime.timedelta(
            days=random.randint(1, 14111)))
        _tags = {1: "габаритный", 2: "маленький", 3: "скользкий", 4: "твердый", 5: "мягкий", 6: "темный",
                 7: "светлый",
                 8: "съедобный", 9: "несъедобный", 10: "легкий", 11: "хрупкий", 12: "тяжелый"}
        # gen_id_tags = _tags[random.randrange(len(_tags))]
        gen_id_tags = dict()
        for i in range(random.randint(1, 4)):
            item_gen._id_tags = gen_id_tags[random.randrange(1, len(_tags))] = _tags[random.randrange(1, len(_tags))]
        item_gen.it_uid = gen_it_uid = uuid.uuid4()
        item_gen.cost = gen_cost = random.randrange(10, 2000, 20)
        yield item_gen

        # Проверка генераций:
        # print(gen_name)
        # print(gen_descr)
        # print(gen_item_id)
        # print(gen_deldate)
        # print(gen_id_tags)
        # print(gen_it_uid)
        # print(gen_cost)
        # print(item_gen)


# print(TestItem.gen_item())
# print(type(TestItem.gen_item()))

# suite = unittest.TestLoader().loadTestsFromTestCase(TestHub)
# unittest.TextTestRunner(verbosity=2).run(suite)
# suite = unittest.TestLoader().loadTestsFromTestCase(TestItem)
# unittest.TextTestRunner(verbosity=2).run(suite)
# f = TestHub()
# g = TestItem()

for i in range(3):
    for item in TestItem.gen_item():
        print(item)
# adf.append(TestItem.gen_item())
# adf.append(TestItem.gen_item())
# adf.append(TestItem.gen_item())
# print(adf)


if TestItem.__name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)
if TestHub.__name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)

It.Item.test_active = 0
