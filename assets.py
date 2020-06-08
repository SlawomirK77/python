"""Zasoby potrzebne do gry."""

import pygame as pg


class Assets:
    """Przechowuje zasoby."""
    # pylint: disable=too-few-public-methods

    @staticmethod
    def load():
        """Wczytuje zasoby z dysku."""
        Assets.komórka_normalna = pg.image.load('assets/komórka_normalna.png')
        Assets.komórka_flaga_bomba = pg.image.load('assets/komórka_flaga_bomba.png')
        Assets.komórka_flaga_bomba_może = pg.image.load('assets/komórka_flaga_bomba_może.png')
        Assets.komórka_zaminowana = pg.image.load('assets/komórka_zaminowana.png')
        Assets.wygrana_partia = pg.image.load('assets/wygrana.png')
        Assets.komórka_z_bombą = pg.image.load('assets/komórka_z_bombą.png')
        for i in range(9):
            Assets.komórka_wybrana.append(pg.image.load(f'assets/komórka_{i}.png'))
            
