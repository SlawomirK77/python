import main
import unittest
import assets
#'''


class KomorkaTest(unittest.TestCase):
    def przygotuj(self):
        self.komorka = main.Komorka(kolumna=1, wiersz=1, bomba=False, wybrana=False, flaga_bomba=False,
                                     flaga_bomba_moze=False)

    def test_bomba(self):
        self.assertFalse(self.komorka.bomba)

    def test_wybrana(self):
        self.assertFalse(self.komorka.wybrana)

    def test_flaga_bomba(self):
        self.assertFalse(self.komorka.flaga_bomba)

    def test_flaga_bomba_moze(self):
        self.assertFalse(self.komorka.flaga_bomba_moze)

    def test_identyfikuj_miny(self):
        plansza = []
        self.assertEqual(self.komorka.identyfikuj_miny(plansza, 0, 0), 0)


'''
    def test_plansza(self):
        ile_wierszy = 3
        ile_kolumn = 4
        plansza = []
        main.inicjuj_pusta_plansze(plansza, ile_kolumn, ile_wierszy)
        for i in [0, 4, 7]:
            plansza[i].bomba=True

        przewidywania = [True, False, False, False,
                         True, False, False, False,
                         True, False, False, False]

        #self.assertListEqual(plansza,przewidywania)
        for i in range(ile_kolumn * ile_wierszy):
            self.assertEqual(plansza[i], przewidywania[i])
'''


class TestAssets(unittest.TestCase):
    def test_plikow(self):
        assets.Assets.load()
        self.assertIsNotNone(assets.Assets.komorka_normalna)
        self.assertIsNotNone(assets.Assets.wygrana_partia)
        self.assertIsNotNone(assets.Assets.komorka_wybrana)
        self.assertIsNotNone(assets.Assets.komorka_flaga_bomba_moze)


if __name__ == '__main__':
    unittest.main()
