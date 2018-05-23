######################
#    François Oder   #
#   Roxan Pulicani   #
#  Cyrielle Canezza  #
#     morpion.py     #
#     10/05/2018     #
# fonctions de base  #
#  pour le morpion   #
######################


class IA_morpion:
    def_sym = [0, 1, -1]
    def_scores = [1, 4, 80, 1500, 20000, 1000000, 0, -2, -40, -180, -10000, -1000000]

    def __init__(self, nbl, nbc, Symboles= def_sym, Scores=def_scores):
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
        # les quintuplés
        self.QTPL = []
        qtpl = 0
        # les quintuplés qui contiennent la case
        self.C2QTPL = [[] for _ in range(nbl * nbc)]
        # quintuplés horizontaux
        for i in range(nbl):
            for j in range(nbc - 4):
                self.QTPL += [(self.lc2ind(i, j), self.lc2ind(i, j + 1), self.lc2ind(i, j + 2), self.lc2ind(i, j + 3),
                               self.lc2ind(i, j + 4))]
                self.C2QTPL[self.lc2ind(i, j)] += [qtpl]
                self.C2QTPL[self.lc2ind(i, j + 1)] += [qtpl]
                self.C2QTPL[self.lc2ind(i, j + 2)] += [qtpl]
                self.C2QTPL[self.lc2ind(i, j + 3)] += [qtpl]
                self.C2QTPL[self.lc2ind(i, j + 4)] += [qtpl]
                qtpl += 1
        # quintuplés verticaux
        for j in range(nbc):
            for i in range(nbl - 4):
                self.QTPL += [(self.lc2ind(i, j), self.lc2ind(i + 1, j), self.lc2ind(i + 2, j), self.lc2ind(i + 3, j),
                               self.lc2ind(i + 4, j))]
                self.C2QTPL[self.lc2ind(i, j)] += [qtpl]
                self.C2QTPL[self.lc2ind(i + 1, j)] += [qtpl]
                self.C2QTPL[self.lc2ind(i + 2, j)] += [qtpl]
                self.C2QTPL[self.lc2ind(i + 3, j)] += [qtpl]
                self.C2QTPL[self.lc2ind(i + 4, j)] += [qtpl]
                qtpl += 1
        # quintuplés diagonaux, vers le bas à droite
        for i in range(nbl - 4):
            for j in range(nbc - 4):
                self.QTPL += [(self.lc2ind(i, j), self.lc2ind(i + 1, j + 1), self.lc2ind(i + 2, j + 2),
                               self.lc2ind(i + 3, j + 3), self.lc2ind(i + 4, j + 4))]
                self.C2QTPL[self.lc2ind(i, j)] += [qtpl]
                self.C2QTPL[self.lc2ind(i + 1, j + 1)] += [qtpl]
                self.C2QTPL[self.lc2ind(i + 2, j + 2)] += [qtpl]
                self.C2QTPL[self.lc2ind(i + 3, j + 3)] += [qtpl]
                self.C2QTPL[self.lc2ind(i + 4, j + 4)] += [qtpl]
                qtpl += 1
        # quintuplés diagonaux, vers le bas à gauche
        for i in range(nbl - 4):
            for j in range(4, nbc):
                self.QTPL += [(self.lc2ind(i, j), self.lc2ind(i + 1, j - 1), self.lc2ind(i + 2, j - 2),
                               self.lc2ind(i + 3, j - 3), self.lc2ind(i + 4, j - 4))]
                self.C2QTPL[self.lc2ind(i, j)] += [qtpl]
                self.C2QTPL[self.lc2ind(i + 1, j - 1)] += [qtpl]
                self.C2QTPL[self.lc2ind(i + 2, j - 2)] += [qtpl]
                self.C2QTPL[self.lc2ind(i + 3, j - 3)] += [qtpl]
                self.C2QTPL[self.lc2ind(i + 4, j - 4)] += [qtpl]
                qtpl += 1
        # les scores des quintuplés
        self.QTPL2Score = [ScoreVide for _ in range(len(self.QTPL))]
        self.C2Score = [self.Evalc(i) for i in range(nbl * nbc)]

    @property
    def nbl(self):
        return self.__nbl

    @nbl.setter
    def nbl(self, nbl):
        self.__nbl = nbl

    @property
    def nbc(self):
        return self.__nbc

    @nbc.setter
    def nbc(self, nbc):
        self.__nbc = nbc

    @property
    def sym(self):
        return self.__sym

    @sym.setter
    def sym(self, Symboles):
        self.__sym = Symboles

    @property
    def scores(self):
        return self.__scores

    @scores.setter
    def scores(self, Scores):
        self.__scores = Scores

    @property
    def Cases(self):
        return self.__Cases

    @Cases.setter
    def Cases(self, Cases):
        self.__Cases = Cases

    @property
    def QTPL(self):
        return self.__QTPL

    @QTPL.setter
    def QTPL(self, QTPL):
        self.__QTPL = QTPL

    @property
    def C2QTPL(self):
        return self.__C2QTPL

    @C2QTPL.setter
    def C2QTPL(self, C2QTPL):
        self.__C2QTPL = C2QTPL

    @property
    def QTPL2Score(self):
        return self.__QTPL2Score

    @QTPL2Score.setter
    def QTPL2Score(self, QTPL2Score):
        self.__QTPL2Score = QTPL2Score

    @property
    def C2Score(self):
        return self.__C2Score

    @C2Score.setter
    def C2Score(self, C2Score):
        self.__C2Score = C2Score

    def lc2ind(self, numl, numc):
        """

        :param numl:
        :param numc:
        :return:
        """
        return numl * self.nbc + numc

    def ind2lc(self, ind):
        """

        :param ind:
        :return:
        """
        return (ind // self.nbc, ind % self.nbc)

    def Evalc(self, ind):
        """

        :param ind:
        :return:
        """
        res = 0
        for qtpl in self.C2QTPL[ind]:
            res += abs(self.QTPL2Score[qtpl])
        return res

    def Evalq(self, qtpl):
        """

        :param qtpl:
        :return:
        """
        O, X = self.sym[1], self.sym[2]
        ScoreVide, ScoreO, ScoreOO, ScoreOOO = self.scores[0], self.scores[1], self.scores[2], self.scores[3]
        ScoreOOOO, ScoreOOOOO , ScoreXXXX, ScoreXXXXX = self.scores[4], self.scores[5], self.scores[10], self.scores[11]
        ScoreOX, ScoreX, ScoreXX, ScoreXXX = self.scores[6], self.scores[7], self.scores[8], self.scores[9]
        L = []
        for c in self.QTPL[qtpl]:
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
                        L.remove(O)
                        if O in L:
                            return ScoreOOOOO
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
                        L.remove(X)
                        if X in L:
                            return ScoreXXXXX
                        return ScoreXXXX
                    return ScoreXXX
                return ScoreXX
            return ScoreX
        return ScoreVide

    def UpdateScore(self, coup):
        """

        :param coup:
        :return:
        """
        UpdateCases = set()
        for qtpl in self.C2QTPL[coup]:
            self.QTPL2Score[qtpl] = self.Evalq(qtpl)
            for case in self.QTPL[qtpl]:
                UpdateCases.add(case)
        for case in UpdateCases:
            self.C2Score[case] = self.Evalc(case)

    def CoupJouer(self):
        """

        :return:
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

        :return:
        """
        print(' ', [str(i) for i in range(self.nbc)])
        for i in range(self.nbl):
            print(i, self.Cases[self.lc2ind(i, 0):self.lc2ind(i, self.nbc)])

    def Victoire(self):
        """

        :return:
        """
        O, X = self.sym[1], self.sym[2]
        QTPL_C = []
        for qtpl in range(len(self.QTPL)):
            qtpl_c = []
            for case in self.QTPL[qtpl]:
                qtpl_c += [self.Cases[case]]
            QTPL_C += [qtpl_c]
        if [O, O, O, O, O] in QTPL_C:
            return 1
        elif [X, X, X, X, X] in QTPL_C:
            return 1
        return 0
