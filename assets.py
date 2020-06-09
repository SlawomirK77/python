"""Zasoby potrzebne do gry."""

import pygame as pg


class Assets:
    """Przechowuje zasoby."""
    # pylint: disable=too-few-public-methods

    @staticmethod
    def load():
        """Wczytuje zasoby z dysku."""
        Assets.komorka_wybrana = []
        Assets.komorka_normalna = pg.image.load('assets/komorka_normalna.png')
        Assets.komorka_flaga_bomba = pg.image.load('assets/komorka_flaga_bomba.png')
        Assets.komorka_flaga_bomba_moze = pg.image.load('assets/komorka_flaga_bomba_moze.png')
        Assets.komorka_zaminowana = pg.image.load('assets/komorka_zaminowana.png')
        Assets.wygrana_partia = pg.transform.scale(pg.image.load('assets/wygrana.png'),(50,50))
        Assets.komorka_z_bomba = pg.image.load('assets/komorka_z_bomba.png')
        for i in range(9):
            Assets.komorka_wybrana.append(pg.image.load(f'assets/komorka_{i}.png'))
