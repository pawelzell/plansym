import pygame
import time
import inputbox
import linecache
import os
from math import sqrt


class Planeta():
    def __init__(self, dane_planety):
        self.x = float(dane_planety[0])
        self.y = float(dane_planety[1])
        self.m = float(dane_planety[2])
        self.vx = float(dane_planety[3])
        self.vy = float(dane_planety[4])
        self.g = [0.0, 0.0]  # WYPADKOWE PRZYSPIESZENIE GRAWITACYJNE DZIALAJACE W DANEJ TURZE


class Dane():
    obiekty = []
    _n = 100  # LICZBA SKOKOW NA SEKUNDE
    k = 1

    def __init__(self):
        self.rozdzielczosc = self.ustal_rozdzielczosc()
        self.exit = False

    def lista_planet(self):
        return self.obiekty

    def czas(self):
        return self._n

    def ustal_rozdzielczosc(self):
        pygame.init()
        infoObject = pygame.display.Info()
        pygame.quit()
        return infoObject.current_w, infoObject.current_h


class Wczytywanie():
    def __init__(self, dane, rysowanie):
        self.dane = dane
        self.rysowanie = rysowanie

    def wczytaj_polozenie_xy(self, i, n):
        screen = self.dane.screen
        bialy = (255, 255, 255)
        czarny = (0, 0, 0)
        screen.fill(czarny)
        self.rysowanie.rysuj_naglowek("PlanSym Load data: New planet " + str(i) + " / " + str(n))
        self.rysowanie.rysuj_panel_dolny("Click to set position of planet.")
        self.rysowanie.rysuj_planety()
        click = False
        pos = [0, 0]
        while not click and not self.dane.exit:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = event.pos
                    click = True
                if event.type == pygame.QUIT:
                    self.dane.exit = True
        return pos

    def wczytaj_mase(self, i, n):
        screen = self.dane.screen
        bialy = (255, 255, 255)
        czarny = (0, 0, 0)
        screen.fill(czarny)
        self.rysowanie.rysuj_naglowek("PlanSym Load data: New planet "+ str(i) + " / " + str(n))
        self.rysowanie.rysuj_planety()

        self.rysowanie.rysuj_panel_dolny("Set mass of planet")
        font = pygame.font.SysFont('Calibri', 60)
        inputbox.display_box_disabled(screen, (450, screen.get_height() - 120, 70, 60), "")
        text = font.render("*10^", True, czarny)
        screen.blit(text, [325, screen.get_height() - 120])
        pygame.display.flip()
        m_text = inputbox.ask(screen, (20, screen.get_height() - 120, 300, 60), "m = ", self.dane)
        m = float(m_text)

        self.rysowanie.rysuj_panel_dolny("Set mass of planet")
        inputbox.display_box_disabled(screen, (20, screen.get_height() - 120, 300, 60), "m = " + m_text)
        screen.blit(text, [325, screen.get_height() - 120])
        pygame.display.flip()
        w_text = inputbox.ask(screen, (450, screen.get_height() - 120, 70, 60), "", self.dane)
        w = int(w_text)
        c = 1
        for i in range(1, w + 1):
            c *= 10
        return m * c

    def wczytaj_predkosc(self, i, n, xy_planety):
        screen = self.dane.screen
        bialy = (255, 255, 255)
        czarny = (0, 0, 0)
        screen.fill(czarny)
        self.rysowanie.rysuj_naglowek("PlanSym Load data: New planet "+ str(i) + " / " + str(n))
        self.rysowanie.rysuj_panel_dolny("Click to set speed vector.")
        self.rysowanie.rysuj_planety()
        click = False
        pos = [0, 0]
        while not click and not self.dane.exit:
            pygame.draw.rect(screen, czarny, (0, 100, screen.get_width(), screen.get_height() - 300))
            pygame.draw.circle(screen, bialy, (xy_planety[0], xy_planety[1]), 2, 0)
            pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, bialy, [xy_planety[0], xy_planety[1]], [pos[0], pos[1]], 1)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = event.pos
                    click = True
                if event.type == pygame.QUIT:
                    self.dane.exit = True

        v = [pos[0] - xy_planety[0], pos[1] - xy_planety[1]]
        return v

    def wczytaj_planete(self, i, n, exit):
        dane_planety = [0, 0, 0.0, 0.0, 0.0]
        pos = self.wczytaj_polozenie_xy(i, n)
        dane_planety[0] = pos[0]
        dane_planety[1] = pos[1]

        dane_planety[2] = self.wczytaj_mase(i, n)

        xy_planety = [dane_planety[0], dane_planety[1]]

        v = self.wczytaj_predkosc(i, n, xy_planety)
        dane_planety[3] = v[0]
        dane_planety[4] = v[1]

        planeta = Planeta(dane_planety)
        return planeta

    def wczytaj(self):
        obiekty = []
        self.dane.screen.fill((0, 0, 0))
        self.rysowanie.rysuj_naglowek("PlanSym Load data ")
        self.rysowanie.rysuj_panel_dolny("Set number of planets:")
        n_text = inputbox.ask(self.dane.screen, (20, self.dane.screen.get_height() - 120, 220, 60), "n = ", self.dane)
        n = int(n_text)

        for i in xrange(1, n + 1):
            obiekty.append(self.wczytaj_planete(i, n, exit))
            self.dane.obiekty = obiekty
            if self.dane.exit:
                break

    def wczytaj_z_pliku(self):
        # FORMAT DANYCH W PLIKU
        # W PIERWSZEJ LINI LICZBA CALKOWITE N OZNACZAJACA LICZBE PLANET
        # W KAZDEJ Z KOLEJNYCH N LINII 5 LICZB ODDZIELONE ODSTEPEM OZNACZAJACE KOLEJNO,X,Y,M,V_X,V_Y PLANETY BEZ SPACJI NA KONCU LINII
        # LICZBA M MOZE BYC PODANA W NOTACJI WYKLADNICZEJ NP:. 1.24e+13 BEZ SPACJI POMIEDZY LICZBAMI ORAZ WYRAZENIEM e+
        wymiary_x = 500
        x = (self.dane.screen.get_width() - wymiary_x) / 2
        y = 300
        wymiary_y = 220
        rect = (x, y, wymiary_x, wymiary_y)
        pos = (0, 0)
        plik_znaleziono = False
        while not plik_znaleziono and not self.dane.exit:
            self.dane.screen.fill((0, 0, 0))
            self.rysowanie.rysuj_naglowek("PlanSym Load data: New planet ")
            self.rysowanie.rysuj_menu(rect, pos, "Name of file")
            font = pygame.font.SysFont('Calibri', 30)
            text = font.render("Click to accept.", True, (0, 0, 0))
            self.dane.screen.blit(text, [x + 30, y + 180])
            pygame.display.flip()
            plik = inputbox.ask(self.dane.screen, (x + 30, y + 100, wymiary_x - 60, 60), "", self.dane)
            if not self.dane.exit:
                try:
                    f = open(plik)
                    plik_znaleziono = True
                    f.close()
                except IOError:
                    plik_znaleziono = False
                    self.dane.screen.fill((0, 0, 0))
                    self.rysowanie.rysuj_naglowek("PlanSym Load data from file ")
                    self.rysowanie.rysuj_menu(rect, pos, "Clic correct")
                    font = pygame.font.SysFont('Calibri', 60)
                    text = font.render("neme of file", True, (0, 0, 0))
                    self.dane.screen.blit(text, [x + 30, y + 90])
                    pygame.display.flip()
                    time.sleep(2.0)
        if not self.dane.exit:
            obiekty = []
            n_text = linecache.getline(plik, 1)
            n = int(n_text)
            for i in range(2, n + 2):
                dane = linecache.getline(plik, i)
                dane_planety = self.obrob_dane_z_pliku(dane)
                obiekty.append(Planeta(dane_planety))
            self.dane.obiekty = obiekty

    def nalezy_do(self, pos, rect):
        if (pos[0] >= rect[0] and pos[0] <= rect[0] + rect[2]) and (pos[1] >= rect[1] and pos[1] <= rect[1] + rect[3]):
            return True
        else:
            return False

    def obrob_dane_z_pliku(self, dane):
        ujemna_wartosc = False
        if dane[0] == "-":
            dane = dane[1:len(dane)]
            ujemna_wartosc = True
        i = dane.find(" ")
        x = float(dane[:i])
        dane = dane[i + 1:len(dane)]
        if ujemna_wartosc:
            x = -x
            ujemna_wartosc = False

        if dane[0] == "-":
            dane = dane[1:len(dane)]
            ujemna_wartosc = True
        i = dane.find(" ")
        y = float(dane[:i])
        dane = dane[i + 1:len(dane)]
        if ujemna_wartosc:
            y = -y
            ujemna_wartosc = False

        if dane[0] == "-":
            dane = dane[1:len(dane)]
            ujemna_wartosc = True
        i = dane.find("e+")
        if i == -1:
            i = dane.find(" ")
            m = float(dane[:i])
            dane = dane[i + 1:len(dane)]
        else:
            m = float(dane[:i])
            dane = dane[i + 2:len(dane)]
            i = dane.find(" ")
            w = int(dane[:i])
            dane = dane[i + 1:len(dane)]
            for i in range(0, w):
                m *= 10.0
        if ujemna_wartosc:
            m = -m
            ujemna_wartosc = False

        if dane[0] == "-":
            dane = dane[1:len(dane)]
            ujemna_wartosc = True
        i = dane.find(" ")
        v_x = float(dane[:i])
        dane = dane[i + 1:len(dane)]
        if ujemna_wartosc:
            v_x = -v_x
            ujemna_wartosc = False

        if dane[0] == "-":
            dane = dane[1:len(dane)]
            ujemna_wartosc = True
        v_y = float(dane)
        if ujemna_wartosc:
            v_y = -v_y
            ujemna_wartosc = False
        dane_planety = [x, y, m, v_x, v_y]
        return dane_planety

    def menu_wczytaj(self):
        self.dane.screen.fill((0, 0, 0))
        self.rysowanie.rysuj_naglowek("PlanSym")
        wymiary_x = 500
        x = (self.dane.screen.get_width() - wymiary_x) / 2
        y = 300
        wymiary_y = 260
        rect = (x, y, wymiary_x, wymiary_y)
        pos = pygame.mouse.get_pos()
        self.rysowanie.rysuj_menu(rect, pos, "Menu", "Enter data", "Enter data file")
        click = False

        clock = pygame.time.Clock()
        while not click and not self.dane.exit:
            pos = pygame.mouse.get_pos()
            self.rysowanie.rysuj_menu(rect, pos, "Menu", "Enter data", "Enter data file")
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and (
                    self.nalezy_do(pos, (x + 30, y + 100, wymiary_x - 60, 60)) or self.nalezy_do(pos, (
                    x + 30, y + 180, wymiary_x - 60, 60))):
                    pos = event.pos
                    click = True
                if event.type == pygame.QUIT:
                    self.dane.exit = True
            clock.tick(25)

        if click:
            if self.nalezy_do(pos, (x + 30, y + 100, wymiary_x - 60, 60)):
                self.wczytaj()
            elif self.nalezy_do(pos, (x + 30, y + 180, wymiary_x - 60, 60)):
                self.wczytaj_z_pliku()


class Runda():
    G = 0.00000000000673848

    def __init__(self, dane):
        self.dane = dane

    def odleglosc(self, planetaa, planetab):
        return sqrt((planetaa.x - planetab.x) * (planetaa.x - planetab.x) + (planetaa.y - planetab.y) * (
        planetaa.y - planetab.y))

    def aktualizuj(self):
        t = 1.0 / float(self.dane.czas())
        lista_planet = self.dane.lista_planet()
        for planetaa in lista_planet:
            for planetab in lista_planet:
                if planetaa != planetab:
                    r = self.odleglosc(planetaa, planetab)
                    if r == 0:
                        break
                    x = planetab.x - planetaa.x
                    y = planetab.y - planetaa.y
                    F = self.G * planetab.m / (r * r)
                    planetaa.g[0] += F * x / r
                    planetaa.g[1] += F * y / r
        for planeta in lista_planet:
            planeta.x += planeta.g[0] * t + planeta.vx * t
            planeta.y += planeta.g[1] * t + planeta.vy * t
            # planeta.vx += planeta.g[0] *t
        #planeta.vy += planeta.g[1] *t


class Rysowanie():
    def __init__(self, dane):
        self.dane = dane
        self.bialy = (255, 255, 255)
        self.czarny = (0, 0, 0)
        self.seledynowy = (172, 225, 175)

    def nalezy_do(self, pos, rect):
        if (pos[0] >= rect[0] and pos[0] <= rect[0] + rect[2]) and (pos[1] >= rect[1] and pos[1] <= rect[1] + rect[3]):
            return True
        else:
            return False

    def start_symulacji(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)
        pygame.init()
        self.size = (self.dane.rozdzielczosc[0] - 20, self.dane.rozdzielczosc[1] - 100)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Planets simulator")
        self.screen.fill(self.czarny)
        pygame.display.flip()
        return self.screen

    def rysuj_panel_dolny(self, napis):
        pygame.draw.rect(self.screen, self.bialy, (0, self.screen.get_height() - 200, self.screen.get_width(), 200))
        font = pygame.font.SysFont('Calibri', 60)
        text = font.render(napis, True, (0, 0, 0))
        self.screen.blit(text, [20, self.screen.get_height() - 180])
        pygame.display.flip()

    def rysuj_naglowek(self, napis):
        pygame.draw.rect(self.screen, self.bialy, (0, 0, self.screen.get_width(), 100))
        font = pygame.font.SysFont('Calibri', 60)
        tytul = font.render(napis, True, (0, 0, 0))
        self.screen.blit(tytul, [20, 20])
        pygame.display.flip()

    def rysuj_planety(self):
        lista_planet = self.dane.lista_planet()
        for planeta in lista_planet:
            pygame.draw.circle(self.screen, self.bialy, (int(planeta.x), int(planeta.y)), 2, 0)
        pygame.display.flip()

    def rysuj_stan_symulacji(self, pos, x, y, napis, rect1, rect2):
        pygame.draw.rect(self.screen, self.czarny, (0, 0, self.screen.get_width(), self.screen.get_height()))
        self.rysuj_panel_dolny_maly("Click Esc to exit simulation.")
        font = pygame.font.SysFont('Calibri', 25)
        text = font.render(napis, True, self.czarny)
        self.screen.blit(text, [x, y])

        if self.nalezy_do(pos, rect1):
            self.rysuj_przycisk_aktywny(rect1, "+", 50, 7, -4)
        else:
            self.rysuj_przycisk_nieaktywny(rect1, "+", 50, 7, -4)

        if self.nalezy_do(pos, rect2):
            self.rysuj_przycisk_aktywny(rect2, "-", 50, 12, -6)
        else:
            self.rysuj_przycisk_nieaktywny(rect2, "-", 50, 12, -6)

        self.rysuj_planety()

    def rysuj_panel_dolny_maly(self, napis):
        pygame.draw.rect(self.screen, self.bialy, (0, self.screen.get_height() - 70, self.screen.get_width(), 70))
        font = pygame.font.SysFont('Calibri', 45)
        text = font.render(napis, True, (0, 0, 0))
        self.screen.blit(text, [20, self.screen.get_height() - 60])

    def rysuj_przycisk_aktywny(self, rect, napis, napis_wielkosc, margin_x, margin_y):
        pygame.draw.rect(self.screen, self.czarny, rect)
        pygame.draw.rect(self.screen, self.seledynowy, (rect[0] + 4, rect[1] + 4, rect[2] - 8, rect[3] - 8))
        font = pygame.font.SysFont('Calibri', napis_wielkosc)
        text = font.render(napis, True, (0, 0, 0))
        self.screen.blit(text, [rect[0] + margin_x, rect[1] + margin_y])

    def rysuj_przycisk_nieaktywny(self, rect, napis, napis_wielkosc, margin_x, margin_y):
        pygame.draw.rect(self.screen, self.czarny, rect)
        pygame.draw.rect(self.screen, self.bialy, (rect[0] + 4, rect[1] + 4, rect[2] - 8, rect[3] - 8))
        font = pygame.font.SysFont('Calibri', napis_wielkosc)
        text = font.render(napis, True, (0, 0, 0))
        self.screen.blit(text, [rect[0] + margin_x, rect[1] + margin_y])

    def rysuj_menu(self, rect, pos, tytul, *args):
        n = len(args)
        x = rect[0]
        y = rect[1]
        wymiary_x = rect[2]
        pygame.draw.rect(self.screen, self.bialy, rect)
        font = pygame.font.SysFont('Calibri', 60)
        text = font.render(tytul, True, self.czarny)
        self.screen.blit(text, [x + 30, y + 20])
        for i in range(0, n):
            if self.nalezy_do(pos, (x + 30, y + 100 + i * 80, wymiary_x - 60, 60)):
                self.rysuj_przycisk_aktywny((x + 30, y + 100 + i * 80, wymiary_x - 60, 60), args[i], 40, 10, 10)
            else:
                self.rysuj_przycisk_nieaktywny((x + 30, y + 100 + i * 80, wymiary_x - 60, 60), args[i], 40, 10, 10)
        pygame.display.flip()


class Interfejs():
    """ Klasa interakcji z uzytkownikiem """

    def __init__(self):
        self.dane = Dane()
        self.rysowanie = Rysowanie(self.dane)
        self.runda = Runda(self.dane)
        self.wczytywanie = Wczytywanie(self.dane, self.rysowanie)

    def nalezy_do(self, pos, rect):
        if (pos[0] >= rect[0] and pos[0] <= rect[0] + rect[2]) and (pos[1] >= rect[1] and pos[1] <= rect[1] + rect[3]):
            return True
        else:
            return False

    def wczytaj(self):
        self.wczytywanie.menu_wczytaj()

    def aktualizuj(self):
        self.runda.aktualizuj()

    def rysuj(self):
        self.rysowanie.rysuj()

    def czas(self):
        return self.dane.czas()

    def start_symulacji(self):
        self.dane.screen = self.rysowanie.start_symulacji()

    def symuluj(self):
        screen = self.dane.screen
        clock = pygame.time.Clock()
        rect1 = (665, screen.get_height() - 45, 40, 40)
        rect2 = (715, screen.get_height() - 45, 40, 40)
        escape = False
        while not self.dane.exit and not escape:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = event.pos
                    if self.nalezy_do(pos, rect1):
                        self.dane.k += 1
                    if self.nalezy_do(pos, rect2) and self.dane.k > 1:
                        self.dane.k -= 1
                if event.type == pygame.QUIT:
                    self.dane.exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        escape = True

            pos = pygame.mouse.get_pos()
            for i in range(0, self.dane.k):  # k PREDKOSC SYMULACJI
                self.aktualizuj()
            self.rysowanie.rysuj_stan_symulacji(pos, 650, screen.get_height() - 68, "Speed: " + str(self.dane.k),
                                                rect1, rect2)
            clock.tick(self.czas())


def main():
    it = Interfejs()
    it.start_symulacji()
    while not it.dane.exit:
        it.wczytaj()
        it.symuluj()
    pygame.quit()


if __name__ == '__main__':
    main()
