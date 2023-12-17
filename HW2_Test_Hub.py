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


if TestItem.__name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)
if TestHub.__name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)

# suite = unittest.TestLoader().loadTestsFromTestCase(TestHub)
# unittest.TextTestRunner(verbosity=2).run(suite)
# suite = unittest.TestLoader().loadTestsFromTestCase(TestItem)
# unittest.TextTestRunner(verbosity=2).run(suite)
# f = TestHub()
# g = TestItem()

It.Item.test_active = 0
