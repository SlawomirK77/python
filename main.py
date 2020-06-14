from dataclasses import dataclass
import random

import pygame as pg
import tkinter

import assets


BOK_KRATKI = 16
SASIADUJACE_POLA = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


@dataclass
class Komorka:
    kolumna: int
    wiersz: int
    bomba: bool = False
    wybrana: bool = False
    flaga_bomba: bool = False
    flaga_bomba_moze: bool = False
    bomby_w_sasiedztwie = int = 0

    def pokaz(self, ekran, kod):
        pozycja = (self.kolumna * BOK_KRATKI, self.wiersz * BOK_KRATKI)
        if self.wybrana:
            if self.bomba:
                ekran.blit(assets.Assets.komorka_zaminowana, pozycja)
            else:
                ekran.blit(assets.Assets.komorka_wybrana[self.bomby_w_sasiedztwie], pozycja)
        else:
            if self.flaga_bomba:
                ekran.blit(assets.Assets.komorka_flaga_bomba, pozycja)
            elif self.flaga_bomba_moze:
                ekran.blit(assets.Assets.komorka_flaga_bomba_moze, pozycja)
            else:
                ekran.blit(assets.Assets.komorka_normalna, pozycja)
            if kod == ['x', 'y', 'z', 'z', 'y'] and not self.flaga_bomba and not self.flaga_bomba_moze:
                if self.bomba:
                    ekran.blit(assets.Assets.komorka_z_bomba, pozycja)

    def identyfikuj_miny(self, plansza, ile_kolumn, ile_wierszy):
        for pozycja in SASIADUJACE_POLA:
            nowy_wiersz = self.wiersz + pozycja[0]
            nowy_kolumna = self.kolumna + pozycja[1]
            if czy_na_planszy(nowy_wiersz, nowy_kolumna, ile_kolumn, ile_wierszy):
                if plansza[nowy_kolumna * ile_wierszy + nowy_wiersz].bomba:
                    self.bomby_w_sasiedztwie += 1


def czy_na_planszy(wiersz, kolumna, ile_kolumn, ile_wierszy):
    return wiersz > -1 and wiersz < ile_wierszy and kolumna > -1 and kolumna < ile_kolumn


def zaminuj_plansze(wiersz, kolumna, plansza, zmienna, ile_kolumn, ile_wierszy, ile_min):
    i = ile_min
    bezpieczna_lista = []
    komorka = plansza[zmienna]
    for pozycja in SASIADUJACE_POLA:
        nowy_wiersz = komorka.wiersz + pozycja[0]
        nowy_kolumna = komorka.kolumna + pozycja[1]
        if czy_na_planszy(nowy_wiersz, nowy_kolumna, ile_kolumn, ile_wierszy):
            bezpieczna_lista.append(plansza[nowy_kolumna * ile_wierszy + nowy_wiersz])
    while i > 0:
        x = random.randrange(ile_wierszy * ile_kolumn)
        if not plansza[x].bomba and not plansza[x].wybrana and plansza[x] not in bezpieczna_lista:
            plansza[x].bomba = True
            i -= 1


def policz_bomby(plansza, ile_kolumn, ile_wierszy):
    for kratka in plansza:
        if not kratka.bomba:
            kratka.identyfikuj_miny(plansza, ile_kolumn, ile_wierszy)


def odkryj_pobliskie(plansza, wiersz, kolumna, ile_kolumn, ile_wierszy):
    for zmienna in SASIADUJACE_POLA:
        nowy_wiersz = wiersz + zmienna[0]
        nowy_kolumna = kolumna + zmienna[1]
        if czy_na_planszy(nowy_wiersz, nowy_kolumna, ile_kolumn, ile_wierszy):
            komorka = plansza[nowy_kolumna * ile_wierszy + nowy_wiersz]
            #komorka = plansza[nowy_wiersz * ile_kolumn + nowy_kolumna]
            if komorka.bomby_w_sasiedztwie == 0 and not komorka.wybrana:
                komorka.wybrana = True
                odkryj_pobliskie(plansza, nowy_wiersz, nowy_kolumna, ile_kolumn, ile_wierszy)
            else:
                komorka.wybrana = True


def czy_wygrana(plansza, ile_kolumn, ile_wierszy, ile_min):
    i = ile_min
    j = ile_wierszy * ile_kolumn - ile_min
    for kratka in plansza:
        if kratka.bomba and kratka.flaga_bomba:
            i -= 1
        if not kratka.bomba and kratka.wybrana:
            j -= 1
    if i == 0 or j == 0:
        return True
    return False
    

def inicjuj_pusta_plansze(plansza, ile_kolumn, ile_wierszy):
    for i in range(ile_kolumn * ile_wierszy):
        plansza.append(Komorka(i // ile_wierszy, i % ile_wierszy))


def graj(szerokosc, wysokosc, ilosc_min):
    
    plansza = []
    plansza.clear()
    kod = []
    kod.clear()
    ile_kolumn = szerokosc
    ile_wierszy = wysokosc
    ile_min = ilosc_min
    rozmiar_okna = [ile_kolumn * BOK_KRATKI, ile_wierszy * BOK_KRATKI]
    inicjuj_pusta_plansze(plansza, ile_kolumn, ile_wierszy)

    assets.Assets.load()

    wygrana = False
    pierwszy_ruch = True
    akcja_trwa = True
    ekran = pg.display.set_mode(rozmiar_okna)
    pg.init()
    while akcja_trwa:
        for wydarzenie in pg.event.get():
            if wydarzenie.type == pg.KEYDOWN:
                kod += (wydarzenie.unicode)
            if wydarzenie.type == pg.QUIT:
                akcja_trwa = False
            if wydarzenie.type == pg.MOUSEBUTTONDOWN:
                mysz_os_x, mysz_os_y = pg.mouse.get_pos()
                kolumna = mysz_os_x//BOK_KRATKI
                wiersz = mysz_os_y//BOK_KRATKI
                zmienna = kolumna * ile_wierszy + wiersz
                komorka = plansza[zmienna]
                if pierwszy_ruch:
                    if pg.mouse.get_pressed()[0]:
                        komorka.wybrana = True
                        zaminuj_plansze(wiersz, kolumna, plansza, zmienna, ile_kolumn, ile_wierszy, ile_min)
                        policz_bomby(plansza, ile_kolumn, ile_wierszy)
                        odkryj_pobliskie(plansza, wiersz, kolumna, ile_kolumn, ile_wierszy)
                        pierwszy_ruch = False
                if pg.mouse.get_pressed()[2]:
                    if komorka.flaga_bomba:
                        komorka.flaga_bomba = False
                        komorka.flaga_bomba_moze = True
                    elif komorka.flaga_bomba_moze:
                        komorka.flaga_bomba = False
                        komorka.flaga_bomba_moze = False
                    else:
                        komorka.flaga_bomba = True
                if pg.mouse.get_pressed()[0]:
                    komorka.wybrana = True
                    if komorka.bomby_w_sasiedztwie == 0 and not komorka.bomba:
                        odkryj_pobliskie(plansza, wiersz, kolumna, ile_kolumn, ile_wierszy)
                    if komorka.bomba:
                        for kratka in plansza:
                            kratka.wybrana = True
        for kratka in plansza:
            kratka.pokaz(ekran, kod)
        pg.display.flip()
        wygrana = czy_wygrana(plansza, ile_kolumn, ile_wierszy, ile_min)
        if len(kod) > 5:
            kod.pop(0)
        if kod == kod == ['x', 'y', 'z', 'z', 'y']:
            for kratka in plansza:
                kratka.pokaz(ekran, kod)
            pg.display.flip()
        if wygrana:
            ekran.blit(assets.Assets.wygrana_partia, (20, 20))
            pg.display.flip()
            pg.event.wait()
            p1, p2, p3 = pg.mouse.get_pressed()
            if p1 or p2 or p3:
                break

    pg.display.quit()


def main():
    okno = tkinter.Tk()
    ilosc_min_opis = tkinter.Label(okno, text='Podaj ilość min')
    szerokosc_planszy_opis = tkinter.Label(okno, text='Podaj szerokość planszy')
    wysokosc_planszy_opis = tkinter.Label(okno, text='Podaj wysokość planszy')

    ilosc_min_wprowadz = tkinter.Entry(okno)
    szerokosc_planszy_wprowadz = tkinter.Entry(okno)
    wysokosc_planszy_wprowadz = tkinter.Entry(okno)

    przycisk_startu = tkinter.Button(okno, text='Rozpocznij', command=lambda:graj(int(szerokosc_planszy_wprowadz.get()),
     int(wysokosc_planszy_wprowadz.get()), int(ilosc_min_wprowadz.get())), padx=30, pady=15)
    
    przycisk_zakonczenia = tkinter.Button(okno, text='Zakończ', command=exit, padx=37, pady=15)

    szerokosc_planszy_opis.grid(row=0, column=1)
    szerokosc_planszy_wprowadz.grid(row=1, column=1)

    wysokosc_planszy_opis.grid(row=2, column=1)
    wysokosc_planszy_wprowadz.grid(row=3, column=1)

    ilosc_min_opis.grid(row=4, column=1)
    ilosc_min_wprowadz.grid(row=5, column=1)

    przycisk_startu.grid(row=10, column=2)
    przycisk_zakonczenia.grid(row=10, column=0)

    okno.mainloop()
    pg.quit()


if __name__ == '__main__':
    main()
