import main
import unittest
import assets
#'''


class KomorkaTest(unittest.TestCase):
    def setUp(self):
        self.komorka = main.Komorka(kolumna=5, wiersz=4, bomba=False, wybrana=False, flaga_bomba=False,
                                     flaga_bomba_moze=False)

    def test_bomba(self):
        self.assertFalse(self.komorka.bomba)

    def test_wybrana(self):
        self.assertFalse(self.komorka.wybrana)

    def test_flaga_bomba(self):
        self.assertFalse(self.komorka.flaga_bomba)

    def test_flaga_bomba_moze(self):
        self.assertFalse(self.komorka.flaga_bomba_moze)


class TestAssets(unittest.TestCase):
    def test_plikow(self):
        assets.Assets.load()
        self.assertIsNotNone(assets.Assets.komorka_normalna)
        self.assertIsNotNone(assets.Assets.wygrana_partia)
        self.assertIsNotNone(assets.Assets.komorka_wybrana)
        self.assertIsNotNone(assets.Assets.komorka_flaga_bomba_moze)


if __name__ == '__main__':
    unittest.main()
