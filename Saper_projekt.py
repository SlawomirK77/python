from dataclasses import dataclass
import random

import pygame as pg
import tkinter

import assets

rozmiar_okna = []
plansza = []
ile_kolumn: int
ile_wierszy: int
ile_min: int
odleglosc: int
bok_kratki = 16
wygrana = False
kod = []
sasiadujace_pola = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

assets.Assets.load()


@dataclass
class Komorka:
    kolumna: int
    wiersz: int
    bomba: bool = False
    wybrana: bool = False
    flaga_bomba: bool = False
    flaga_bomba_moze: bool = False
    bomby_w_sasiedztwie = int = 0

    def pokaz(self):
        pozycja = (self.kolumna * bok_kratki, self.wiersz * bok_kratki)
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
            if kod == [120, 121, 122, 122, 121] and not self.flaga_bomba and not self.flaga_bomba_moze:
                if self.bomba:
                    ekran.blit(assets.Assets.komorka_z_bomba, pozycja)

    def identyfikuj_miny(self):
        for pozycja in sasiadujace_pola:
            nowy_wiersz = self.wiersz + pozycja[0]
            nowy_kolumna = self.kolumna + pozycja[1]
            if czy_na_planszy(nowy_wiersz, nowy_kolumna):
                if plansza[nowy_kolumna * ile_wierszy + nowy_wiersz].bomba:
                    self.bomby_w_sasiedztwie += 1


def czy_na_planszy(wiersz, kolumna):
    return wiersz > -1 and wiersz < ile_wierszy and kolumna > -1 and kolumna < ile_kolumn


def zaminuj_plansze(zmienna):
    i = ile_min
    bezpieczna_lista = []
    komorka = plansza[zmienna]
    for pozycja in sasiadujace_pola:
        nowy_wiersz = komorka.wiersz + pozycja[0]
        nowy_kolumna = komorka.kolumna + pozycja[1]
        if czy_na_planszy(nowy_wiersz, nowy_kolumna):
            bezpieczna_lista.append(plansza[nowy_kolumna * ile_wierszy + nowy_wiersz])
    while i > 0:
        x = random.randrange(ile_wierszy * ile_kolumn)
        if not plansza[x].bomba and not plansza[x].wybrana and plansza[x] not in bezpieczna_lista:
            plansza[x].bomba = True
            i -= 1


def policz_bomby():
    for kratka in plansza:
        if not kratka.bomba:
            kratka.identyfikuj_miny()


def odkryj_pobliskie(wiersz, kolumna):
    for zmienna in sasiadujace_pola:
        nowy_wiersz = wiersz + zmienna[0]
        nowy_kolumna = kolumna + zmienna[1]
        if czy_na_planszy(nowy_wiersz, nowy_kolumna):
            komorka = plansza[nowy_kolumna * ile_wierszy + nowy_wiersz]
            if komorka.bomby_w_sasiedztwie == 0 and not komorka.wybrana:
                komorka.wybrana = True
                odkryj_pobliskie(nowy_wiersz, nowy_kolumna)
            else:
                komorka.wybrana = True


def czy_wygrana():
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


def przypisz_wartosci():
    plansza.clear()
    kod.clear()
    global ile_kolumn
    ile_kolumn = int(szerokosc_planszy_wprowadz.get())
    global ile_wierszy
    ile_wierszy = int(wysokosc_planszy_wprowadz.get())
    global ile_min
    ile_min = int(ilosc_min_wprowadz.get())
    global rozmiar_okna
    rozmiar_okna = [ile_kolumn * bok_kratki, ile_wierszy * bok_kratki]
    for i in range(ile_kolumn * ile_wierszy):
        plansza.append(Komorka(i // ile_wierszy, i % ile_wierszy))
    global odleglosc
    if ile_wierszy > ile_kolumn:
        odleglosc = (ile_wierszy * bok_kratki) // ile_kolumn + 1
    else:
        odleglosc = (ile_kolumn * bok_kratki) // ile_wierszy + 1
    global wygrana
    wygrana = False
    global ekran
    ekran = pg.display.set_mode(rozmiar_okna)


def graj():
    pierwszy_ruch = True
    akcja_trwa = True
    pg.init()
    while akcja_trwa:
        for wydarzenie in pg.event.get():
            if wydarzenie.type == pg.KEYDOWN:
                kod.append(wydarzenie.key)
            if wydarzenie.type == pg.QUIT:
                akcja_trwa = False
            if wydarzenie.type == pg.MOUSEBUTTONDOWN:
                mysz_os_x, mysz_os_y = pg.mouse.get_pos()
                kolumna = mysz_os_x//bok_kratki
                wiersz = mysz_os_y//bok_kratki
                zmienna = kolumna * ile_wierszy + wiersz
                komorka = plansza[zmienna]
                if pierwszy_ruch:
                    if pg.mouse.get_pressed()[0]:
                        komorka.wybrana = True
                        zaminuj_plansze(zmienna)
                        policz_bomby()
                        odkryj_pobliskie(wiersz, kolumna)
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
                        odkryj_pobliskie(wiersz, kolumna)
                    if komorka.bomba:
                        for kratka in plansza:
                            kratka.wybrana = True
        for kratka in plansza:
            kratka.pokaz()
        pg.display.flip()
        wygrana = czy_wygrana()
        if len(kod) > 5:
            kod.pop(0)
        if kod == [120, 121, 122, 122, 121]:
            for kratka in plansza:
                kratka.pokaz()
            pg.display.flip()
        if wygrana:
            ekran.blit(assets.Assets.wygrana_partia, (20, 20))
            pg.display.flip()
            pg.event.wait()
            p1,p2,p3 = pg.mouse.get_pressed()
            if p1 or p2 or p3:
                break

    pg.display.quit()


#pg.quit()

okno = tkinter.Tk()


def zlozenie():
    przypisz_wartosci()
    graj()


ilosc_min_opis = tkinter.Label(okno, text='Podaj ilość min')
szerokosc_planszy_opis = tkinter.Label(okno, text='Podaj szerokość planszy')
wysokosc_planszy_opis = tkinter.Label(okno, text='Podaj wysokość planszy')

ilosc_min_wprowadz = tkinter.Entry(okno)
szerokosc_planszy_wprowadz = tkinter.Entry(okno)
wysokosc_planszy_wprowadz = tkinter.Entry(okno)

przycisk_startu = tkinter.Button(okno, text='Rozpocznij', command=zlozenie, padx=30, pady=15)
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
