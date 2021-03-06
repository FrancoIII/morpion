# Franco, 12 oct. 2019

# This script manage a morpion's physical interface

# IN : GPIO 1-7 as rows, GPIO 8-14 as columns
# OUT : GPPIO 15-21 as rows, GPIO 22-28 as columns

import IA_morpion_4_class as IA_mp_class
import RPi.GPIO as GPIO
import time

GPIO_IN_rows = [1, 2, 3, 4, 5, 6, 7]
GPIO_IN_columns = [8, 9, 10, 11, 12, 13, 14]
GPIO_OUT_rows = [15, 16, 17, 18, 19, 20, 21]
GPIO_OUT_columns = [22, 23, 24, 25, 26, 27, 28]
GPIO_OUT_ground = [32]
GPIO_OUT_leds = [29, 30]
GPIO_IN_reset = [31]


def GPIO_initmodes():
    """
    Initiate RasPi's pins that we need
    :return: None
    """
    for r in GPIO_IN_rows:
        GPIO.setmode(r, GPIO.IN)
    for c in GPIO_IN_columns:
        GPIO.setmode(c, GPIO.IN)
    for r in GPIO_OUT_rows:
        GPIO.setmode(r, GPIO.OUT, initial=GPIO.LOW)
    for c in GPIO_OUT_columns:
        GPIO.setmode(c, GPIO.OUT, initial=GPIO.HIGH)
    for g in GPIO_OUT_ground:
        GPIO.setmode(g, GPIO.OUT, initial=GPIO.LOW)
    for p in GPIO_OUT_leds:
        GPIO.setmode(p, GPIO.OUT, initial=GPIO.LOW)
    for s in GPIO_IN_reset:
        GPIO.setmode(s, GPIO.IN)


def cases2dict(IA):
    """

    :type IA: IA_mp_class.IA_morpion
    :param IA:
    :return: the dictionary of lists coresponding to IA.Cases list
    """
    res = {}
    for i in range(IA.nbl):
        res[i] = []
        for j in range(IA.nbc):
            if IA.Cases[IA.lc2ind(i, j)] == IA.sym[1]:
                res[i] += [j]
    return res


def outprint(IA):
    """
    Display IA's pawns on physical interface
    :type IA: IA_mp_class.IA_morpion
    :param IA:
    :return: None
    """
    cases_dict = cases2dict(IA)
    for row in cases_dict:
        GPIO.setup(GPIO_OUT_rows[row], GPIO.HIGH)
        for col in cases_dict[row]:
            GPIO.setup(GPIO_OUT_columns[col], GPIO.LOW)
            time.sleep(0.002)
            GPIO.setup(GPIO_OUT_columns[col], GPIO.HIGH)
        GPIO.setup(GPIO_OUT_rows[row], GPIO.LOW)


def caseInput(IA):
    """
    Check if players added a new pawn
    :type IA: IA_mp_class.IA_morpion
    :param IA:
    :return: the index of the pawn if there is a new one, None otherwise
    """
    cases_dict = cases2dict(IA)
    for row in cases_dict:
        GPIO.setup(GPIO_IN_rows[row], GPIO.HIGH)
        for col in cases_dict[row]:
            if GPIO.input(GPIO_IN_columns[col]) and cases_dict[row][col] == 0:
                return IA.lc2ind(row, col)
        GPIO.setup(GPIO_IN_rows[row], GPIO.LOW)
    return


def playLoop():
    IAmp = IA_mp_class.IA_morpion(7, 7)
    while not IAmp.Victoire():
        outprint(IAmp)
        coup_joueur = caseInput(IAmp)
        outprint(IAmp)
        if coup_joueur is not None:
            outprint(IAmp)
            IAmp.Cases[coup_joueur] = -1
            outprint(IAmp)
            IAmp.UpdateScore(coup_joueur)
            outprint(IAmp)
            coup = IAmp.CoupJouer()
            outprint(IAmp)
            IAmp.Cases[coup] = 1
            outprint(IAmp)
            IAmp.UpdateScore(coup)
            outprint(IAmp)
    GPIO.setup(GPIO_OUT_leds[IAmp.Victoire() - 1], GPIO.HIGH)


while True:
    GPIO_initmodes()
    playLoop()
    while not GPIO.input(GPIO_IN_reset[0]):
        pass
    time.sleep(2)
