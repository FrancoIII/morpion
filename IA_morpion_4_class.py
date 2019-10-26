######################
#   Franco and al.   #
#     morpion.py     #
#     10/05/2018     #
# fonctions de base  #
#  pour le morpion   #
# Version à 4 pionts #
######################


class IA_morpion:
    def_sym = [0, 1, -1]
    def_scores = [1, 4, 80, 1500, 1000000, 0, -2, -40, -180, -1000000]

    def __init__(self, nbl, nbc, Symboles=def_sym, Scores=def_scores):
        """

        :param nbl: le nombre de lignes
        :param nbc: le nombre de colones
        :param Symboles: les symboles pour Vide, O, et X
        :param Scores: les scores (ScoreVide, ScoreO, ScoreOO, ...)
        """
        self.nbl = nbl
        self.nbc = nbc
        self.sym = Symboles
        self.scores = Scores
        Vide, ScoreVide = Symboles[0], Scores[0]
        # les cases
        self.Cases = [Vide for _ in range(nbl * nbc)]
        # les quadruplés
        self.QDPL = []
        qtpl = 0
        # les quadruplés qui contiennent la case
        self.C2QDPL = [[] for _ in range(nbl * nbc)]
        # quadruplés horizontaux
        for i in range(nbl):
            for j in range(nbc - 3):
                self.QDPL += [(self.lc2ind(i, j), self.lc2ind(i, j + 1), self.lc2ind(i, j + 2), self.lc2ind(i, j + 3))]
                self.C2QDPL[self.lc2ind(i, j)] += [qtpl]
                self.C2QDPL[self.lc2ind(i, j + 1)] += [qtpl]
                self.C2QDPL[self.lc2ind(i, j + 2)] += [qtpl]
                self.C2QDPL[self.lc2ind(i, j + 3)] += [qtpl]
                qtpl += 1
        # quadruplés verticaux
        for j in range(nbc):
            for i in range(nbl - 3):
                self.QDPL += [(self.lc2ind(i, j), self.lc2ind(i + 1, j), self.lc2ind(i + 2, j), self.lc2ind(i + 3, j))]
                self.C2QDPL[self.lc2ind(i, j)] += [qtpl]
                self.C2QDPL[self.lc2ind(i + 1, j)] += [qtpl]
                self.C2QDPL[self.lc2ind(i + 2, j)] += [qtpl]
                self.C2QDPL[self.lc2ind(i + 3, j)] += [qtpl]
                qtpl += 1
        # quadruplés diagonaux, vers le bas à droite
        for i in range(nbl - 3):
            for j in range(nbc - 3):
                self.QDPL += [(self.lc2ind(i, j), self.lc2ind(i + 1, j + 1), self.lc2ind(i + 2, j + 2),
                               self.lc2ind(i + 3, j + 3))]
                self.C2QDPL[self.lc2ind(i, j)] += [qtpl]
                self.C2QDPL[self.lc2ind(i + 1, j + 1)] += [qtpl]
                self.C2QDPL[self.lc2ind(i + 2, j + 2)] += [qtpl]
                self.C2QDPL[self.lc2ind(i + 3, j + 3)] += [qtpl]
                qtpl += 1
        # quadruplés diagonaux, vers le bas à gauche
        for i in range(nbl - 3):
            for j in range(3, nbc):
                self.QDPL += [(self.lc2ind(i, j), self.lc2ind(i + 1, j - 1), self.lc2ind(i + 2, j - 2),
                               self.lc2ind(i + 3, j - 3))]
                self.C2QDPL[self.lc2ind(i, j)] += [qtpl]
                self.C2QDPL[self.lc2ind(i + 1, j - 1)] += [qtpl]
                self.C2QDPL[self.lc2ind(i + 2, j - 2)] += [qtpl]
                self.C2QDPL[self.lc2ind(i + 3, j - 3)] += [qtpl]
                qtpl += 1
        # les scores des quadruplés
        self.QDPL2Score = [ScoreVide for _ in range(len(self.QDPL))]
        self.C2Score = [self.Evalc(i) for i in range(nbl * nbc)]

    @property
    def nbl(self):
        """

        :return: le nombre de lignes du damier
        """
        return self.__nbl

    @nbl.setter
    def nbl(self, nbl):
        """

        :param nbl: le nombre de ligne du damier
        :return: None
        """
        self.__nbl = nbl

    @property
    def nbc(self):
        """

        :return: le nombre de colones du damier
        """
        return self.__nbc

    @nbc.setter
    def nbc(self, nbc):
        """

        :param nbc: le nombre de colones du damier
        :return: None
        """
        self.__nbc = nbc

    @property
    def sym(self):
        """

        :return: la liste des symboles utilisés pour Vide, O, X
        """
        return self.__sym

    @sym.setter
    def sym(self, Symboles):
        """

        :param Symboles: la liste des symboles à utiliser pour Vide, O, X
        :return: None
        """
        self.__sym = Symboles

    @property
    def scores(self):
        """

        :return: les scores utilisés pour  les quintuplés (vide, les O croissants, OX, les X croissants)
        """
        return self.__scores

    @scores.setter
    def scores(self, Scores):
        """

        :param Scores: les scores à utiliser pour  les quintuplés (vide, les O croissants, OX, les X croissants)
        :return: None
        """
        self.__scores = Scores

    @property
    def Cases(self):
        """

        :return: la liste des cases du damier
        """
        return self.__Cases

    @Cases.setter
    def Cases(self, Cases):
        """

        :param Cases: la liste des cases du damier
        :return: None
        """
        self.__Cases = Cases

    @property
    def QDPL(self):
        """

        :return: la liste des quadruplés du damier
        """
        return self.__QDPL

    @QDPL.setter
    def QDPL(self, QDPL):
        """

        :param QDPL: la liste des quadruplés du damier
        :return: None
        """
        self.__QDPL = QDPL

    @property
    def C2QDPL(self):
        """

        :return: la liste des liste des quadruplés contenant une certaine case, pour chaque case
        """
        return self.__C2QDPL

    @C2QDPL.setter
    def C2QDPL(self, C2QDPL):
        """

        :param C2QDPL: la liste des liste des quadruplés contenant une certaine case, pour chaque case
        :return: None
        """
        self.__C2QDPL = C2QDPL

    @property
    def QDPL2Score(self):
        """

        :return: la liste des scores des quadruplés
        """
        return self.__QDPL2Score

    @QDPL2Score.setter
    def QDPL2Score(self, QDPL2Score):
        """

        :param QDPL2Score: la liste des scores des quadruplés
        :return: None
        """
        self.__QDPL2Score = QDPL2Score

    @property
    def C2Score(self):
        """

        :return: la liste des scores des cases
        """
        return self.__C2Score

    @C2Score.setter
    def C2Score(self, C2Score):
        """

        :param C2Score: la liste des scores des cases
        :return: None
        """
        self.__C2Score = C2Score

    def lc2ind(self, numl, numc):
        """

        :param numl: un numéro de ligne
        :param numc: un numéro de colone
        :return: l'indice de la case (numl, numc)
        """
        return numl * self.nbc + numc

    def ind2lc(self, ind):
        """

        :param ind: un indice de case
        :return: le couple (numéro_de_ligne, numéro_de_colone) correspondant
        """
        return (ind // self.nbc, ind % self.nbc)

    def Evalc(self, ind):
        """

        :param ind: un undice de case
        :return: le score de cette case (ré-évalué)
        """
        res = 0
        for qtpl in self.C2QDPL[ind]:
            res += abs(self.QDPL2Score[qtpl])
        return res

    def Evalq(self, qtpl):
        """

        :param qtpl: un numéro de quadruplé
        :return: le score de ce quadruplé (ré-évalué)
        """
        O, X = self.sym[1], self.sym[2]
        ScoreVide, ScoreO, ScoreOO, ScoreOOO = self.scores[0], self.scores[1], self.scores[2], self.scores[3]
        ScoreOOOO, ScoreOOOOO , ScoreXXXX, ScoreXXXXX = self.scores[4], self.scores[5], self.scores[10], self.scores[11]
        ScoreOX, ScoreX, ScoreXX, ScoreXXX = self.scores[6], self.scores[7], self.scores[8], self.scores[9]
        L = []
        for c in self.QDPL[qtpl]:
            L += [self.Cases[c]]
        if O in L:
            L.remove(O)
            if X in L:
                return ScoreOX
            elif O in L:
                L.remove(O)
                if O in L:
                    L.remove(O)
                    if O in L:
                        return ScoreOOOO
                    return ScoreOOO
                return ScoreOO
            return ScoreO
        elif X in L:
            L.remove(X)
            if X in L:
                L.remove(X)
                if X in L:
                    L.remove(X)
                    if X in L:
                        return ScoreXXXX
                    return ScoreXXX
                return ScoreXX
            return ScoreX
        return ScoreVide

    def UpdateScore(self, coup):
        """
        Mets à jour les scores de cases et de quadruplés après un coup
        :param coup: l'indice d'une case où l'on vient de jouer
        :return: None
        """
        UpdateCases = set()
        for qtpl in self.C2QDPL[coup]:
            self.QDPL2Score[qtpl] = self.Evalq(qtpl)
            for case in self.QDPL[qtpl]:
                UpdateCases.add(case)
        for case in UpdateCases:
            self.C2Score[case] = self.Evalc(case)

    def CoupJouer(self):
        """

        :return: Le meilleur coup à jouer
        """
        Vide = self.sym[0]
        coup = self.Cases.index(Vide)
        Scorecoup = self.C2Score[coup]
        for i in range(len(self.Cases)):
            if self.Cases[i] != Vide:
                pass
            elif self.C2Score[i] >= Scorecoup:
                Scorecoup = self.C2Score[i]
                coup = i
        return coup

    def Affiche(self):
        """
        Affiche le damier (moche)
        :return: None
        """
        print(' ', [str(i) for i in range(self.nbc)])
        for i in range(self.nbl):
            print(i, self.Cases[self.lc2ind(i, 0):self.lc2ind(i, self.nbc)])

    def Victoire(self):
        """

        :return: Le booléen indiquant si un joueur a gagné
        """
        O, X = self.sym[1], self.sym[2]
        QDPL_C = []
        for qtpl in range(len(self.QDPL)):
            qtpl_c = []
            for case in self.QDPL[qtpl]:
                qtpl_c += [self.Cases[case]]
            QDPL_C += [qtpl_c]
        if [O, O, O, O, O] in QDPL_C:
            return 1
        elif [X, X, X, X, X] in QDPL_C:
            return 2
        return 0
