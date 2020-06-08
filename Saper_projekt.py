from dataclasses import dataclass
import random

import pygame as pg
#import tkinter

ile_wierszy = 5
ile_kolumn = 5
bok_kratki = 16
ile_min = 6
plansza = []
pierwszy_ruch = True
wygrana = False
kod = []
sąsiadujące_pola = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
if ile_wierszy > ile_kolumn:
    odległość = (ile_wierszy * 16) // ile_kolumn + 1
else:
    odległość = (ile_kolumn * 16) // ile_wierszy + 1
rozmiar_okna = [ile_kolumn * 16, ile_wierszy * 16]

pg.init()
ekran = pg.display.set_mode(rozmiar_okna)

komórka_normalna = pg.image.load('komórka_normalna.png')
komórka_flaga_bomba = pg.image.load('komórka_flaga_bomba.png')
komórka_flaga_bomba_może = pg.image.load('komórka_flaga_bomba_może.png')
komórka_zaminowana = pg.image.load('komórka_zaminowana.png')
wygrana_partia = pg.image.load('wygrana.png')
komórka_z_bombą = pg.image.load('komórka_z_bombą.png')
komórka_wybrana = []

for i in range(9):
    komórka_wybrana.append(pg.image.load(f'komórka_{i}.png'))


def czy_na_planszy(wiersz, kolumna):
    return wiersz > -1 and wiersz < ile_wierszy and kolumna > -1 and kolumna < ile_kolumn


def zaminuj_planszę(zmienna):
    i = ile_min
    bezpieczna_lista = []
    komórka = plansza[zmienna]
    for pozycja in sąsiadujące_pola:
        nowy_wiersz = komórka.wiersz + pozycja[0]
        nowy_kolumna = komórka.kolumna + pozycja[1]
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


@dataclass
class Komórka:
    kolumna: int
    wiersz: int
    bomba: bool = False
    wybrana: bool = False
    flaga_bomba: bool = False
    flaga_bomba_może: bool = False
    bomby_w_sąsiedztwie = int = 0

    def pokaż(self):
        pozycja = (self.kolumna * bok_kratki, self.wiersz * bok_kratki)
        if self.wybrana:
            if self.bomba:
                ekran.blit(komórka_zaminowana, pozycja)
            else:
                ekran.blit(komórka_wybrana[self.bomby_w_sąsiedztwie], pozycja)
        else:
            if self.flaga_bomba:
                ekran.blit(komórka_flaga_bomba, pozycja)
            elif self.flaga_bomba_może:
                ekran.blit(komórka_flaga_bomba_może, pozycja)
            else:
                ekran.blit(komórka_normalna, pozycja)
            if kod == [120, 121, 122, 122, 121] and not self.flaga_bomba and not self.flaga_bomba_może:
                if self.bomba:
                    ekran.blit(komórka_z_bombą, pozycja)

    def identyfikuj_miny(self):
        for pozycja in sąsiadujące_pola:
            nowy_wiersz = self.wiersz + pozycja[0]
            nowy_kolumna = self.kolumna + pozycja[1]
            if czy_na_planszy(nowy_wiersz, nowy_kolumna):
                if plansza[nowy_kolumna * ile_wierszy + nowy_wiersz].bomba:
                    self.bomby_w_sąsiedztwie += 1


def odkryj_pobliskie(wiersz, kolumna):
    for zmienna in sąsiadujące_pola:
        nowy_wiersz = wiersz + zmienna[0]
        nowy_kolumna = kolumna + zmienna[1]
        if czy_na_planszy(nowy_wiersz, nowy_kolumna):
            komórka = plansza[nowy_kolumna * ile_wierszy + nowy_wiersz]
            if komórka.bomby_w_sąsiedztwie == 0 and not komórka.wybrana:
                komórka.wybrana = True
                odkryj_pobliskie(nowy_wiersz, nowy_kolumna)
            else:
                komórka.wybrana = True


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


for i in range(ile_kolumn * ile_wierszy):
    plansza.append(Komórka(i // ile_wierszy, i % ile_wierszy))

akcja_trwa = True
while akcja_trwa:
    for wydarzenie in pg.event.get():
        if wydarzenie.type == pg.KEYDOWN:
            kod.append(wydarzenie.key)
        if wydarzenie.type == pg.QUIT:
            akcja_trwa = False
        if wydarzenie.type == pg.MOUSEBUTTONDOWN:
            mysz_oś_X, mysz_oś_Y = pg.mouse.get_pos()
            kolumna = mysz_oś_X//bok_kratki
            wiersz = mysz_oś_Y//bok_kratki
            zmienna = kolumna * ile_wierszy + wiersz
            komórka = plansza[zmienna]
            if pierwszy_ruch:
                if pg.mouse.get_pressed()[0]:
                    komórka.wybrana = True
                    zaminuj_planszę(zmienna)
                    policz_bomby()
                    odkryj_pobliskie(wiersz, kolumna)
                    pierwszy_ruch = False
            if pg.mouse.get_pressed()[2]:
                if komórka.flaga_bomba:
                    komórka.flaga_bomba = False
                    komórka.flaga_bomba_może = True
                elif komórka.flaga_bomba_może:
                    komórka.flaga_bomba = False
                    komórka.flaga_bomba_może = False
                else:
                    komórka.flaga_bomba = True
            if pg.mouse.get_pressed()[0]:
                komórka.wybrana = True
                if komórka.bomby_w_sąsiedztwie == 0 and not komórka.bomba:
                    odkryj_pobliskie(wiersz, kolumna)
                if komórka.bomba:
                    for kratka in plansza:
                        kratka.wybrana = True
    for kratka in plansza:
        kratka.pokaż()
    pg.display.flip()
    wygrana = czy_wygrana()
    if len(kod) > 5:
        kod.pop(0)
        print(kod)
    if kod == [120, 121, 122, 122, 121]:
        for kratka in plansza:
            kratka.pokaż()
        pg.display.flip()
    if wygrana:
        #akcja_trwa = False
        #print("Wygrałeś")
        ekran.blit(wygrana_partia, (20, 20))
        pg.display.flip()
        pass
pg.quit()
