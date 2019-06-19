from django.test import TestCase
from lists.models import Goods



class ItemModelTest(TestCase):

    def test_saving_and_retrieving_goods(self):
        goods_1 = Goods()
        goods_1.name = 'test first goods'
        goods_1.price = '5000'
        goods_1.link = 'www.google.com'
        goods_1.keyword = 'test'
        goods_1.store = 'etmall'
        goods_1.save()

        goods_2 = Goods()
        goods_2.name = 'test second goods'
        goods_2.price = '9999'
        goods_2.link = 'www.msn.com'
        goods_2.keyword = 'test'
        goods_2.store = 'rakuten'
        goods_2.save()

        saved_goods = Goods.objects.all()
        self.assertEqual(saved_goods.count(), 2)

        first_saved_goods = saved_goods[0]
        second_saved_goods = saved_goods[1]

        self.assertEqual(first_saved_goods.name, 'test first goods')
        self.assertEqual(second_saved_goods.name, 'test second goods')
        self.assertEqual(first_saved_goods.price, '5000')
        self.assertEqual(second_saved_goods.price, '9999')