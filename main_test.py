import random
import main
import unittest
import assets


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

    def test_czy_wygrana(self):
        """Testuje funkcję 'czy_wygrana' dla 'surowych' wartości"""
        kolumny = 5
        wiersze = 5
        miny = 5
        plansza = []
        main.inicjuj_pusta_plansze(plansza, kolumny, wiersze)

        self.assertFalse(main.czy_wygrana(plansza, kolumny, wiersze, miny))

        for i in range(miny):
            plansza[i].bomba = True
            plansza[i].flaga_bomba = True

        self.assertTrue(main.czy_wygrana(plansza, kolumny, wiersze, miny))

        for i in plansza:
            i.flaga_bomba = False

        self.assertFalse(main.czy_wygrana(plansza, kolumny, wiersze, miny))

        for i in plansza:
            if not i.bomba:
                i.wybrana = True

        self.assertTrue(main.czy_wygrana(plansza, kolumny, wiersze, miny))

    def test_czy_wygrana2(self):
        """Testuje funkcję 'czy_wygrana' dla losowych wartości"""
        kolumny = random.randint(5, 25)
        wiersze = random.randint(5, 25)
        miny = int((kolumny * wiersze) ** 0.5) * 2
        plansza = []
        main.inicjuj_pusta_plansze(plansza, kolumny, wiersze)
        self.assertFalse(main.czy_wygrana(plansza, kolumny, wiersze, miny))
        warunek = miny
        while warunek:
            pozycja = random.randint(0, wiersze * kolumny - 1)
            if not plansza[pozycja].bomba:
                plansza[pozycja].bomba = True
                warunek -= 1
        self.assertFalse(main.czy_wygrana(plansza, kolumny, wiersze, miny))
        for i in plansza:
            if i.bomba:
                i.flaga_bomba = True
        self.assertTrue(main.czy_wygrana(plansza, kolumny, wiersze, miny))
        for i in plansza:
            if not i.bomba:
                i.wybrana = True
        self.assertTrue(main.czy_wygrana(plansza, kolumny, wiersze, miny))
        plansza.clear()

    def test_policz_bomby(self):
        """Testuje liczenie bomb"""
        kolumny = 2
        wiersze = 2
        plansza = []
        main.inicjuj_pusta_plansze(plansza, kolumny, wiersze)
        plansza[0].bomba = True
        main.policz_bomby(plansza, kolumny, wiersze)
        for i in [1, 2, 3]:
            self.assertEqual(plansza[i].bomby_w_sasiedztwie, 1)

        kolumny = 3
        wiersze = 10
        main.inicjuj_pusta_plansze(plansza, kolumny, wiersze)
        for i in range(10):
            plansza[i].bomba = True
        for i in range(20, 30):
            plansza[i].bomba = True
        main.policz_bomby(plansza, kolumny, wiersze)
        for i in plansza:
            print(i.bomby_w_sasiedztwie)
        self.assertEqual(
            plansza[kolumny].bomby_w_sasiedztwie,
            plansza[2 * kolumny - 1].bomby_w_sasiedztwie)
        for i in range(11, 19):
            self.assertEqual(plansza[i].bomby_w_sasiedztwie, 6)


class TestAssets(unittest.TestCase):
    def test_plikow(self):
        assets.Assets.load()
        self.assertIsNotNone(assets.Assets.komorka_normalna)
        self.assertIsNotNone(assets.Assets.wygrana_partia)
        self.assertIsNotNone(assets.Assets.komorka_wybrana)
        self.assertIsNotNone(assets.Assets.komorka_flaga_bomba_moze)
        self.assertIsNotNone(assets.Assets.komorka_flaga_bomba)
        self.assertIsNotNone(assets.Assets.komorka_zaminowana)
        self.assertIsNotNone(assets.Assets.wygrana_partia)


if __name__ == '__main__':
    unittest.main()
