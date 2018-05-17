######################
#    François Oder   #
#   Roxan Pulicani   #
#  Cyrielle Canezza  #
#     morpion.py     #
#     10/05/2018     #
# fonctions de base  #
#  pour le morpion   #
######################


# Les scores pris en compte, que vous pouvez modifier
Vide = 0
O = 1
X = -1
ScoreVide = 1
ScoreOX = 0
ScoreO = 4
ScoreOO = 80
ScoreOOO = 1500
ScoreOOOO = 20000
ScoreOOOOO = 1000000
ScoreX = -2
ScoreXX = -40
ScoreXXX = -180
ScoreXXXX = -10000
ScoreXXXXX = -1000000


"""
Les scores normaux, quasiment imbatables (bonne chance)
Vide = 0
O = 1
X = -1
ScoreVide = 1
ScoreOX = 0
ScoreO = 4
ScoreOO = 80
ScoreOOO = 1500
ScoreOOOO = 20000
ScoreOOOOO = 1000000
ScoreX = -2
ScoreXX = -40
ScoreXXX = -180
ScoreXXXX = -10000
ScoreXXXXX = -1000000
"""


def lc2ind(numl, numc, nbl, nbc):
    """retourne l'indice de la case sotuée à la ligne l et la colone c"""
    return numl*nbc + numc


def ind2lc(ind, nbl, nbc):
    """retourne la ligne et la colone corespondant à la case d'indice ind"""
    return (ind//nbc, ind%nbc)


def Create(nbl, nbc):
    """crée toutes les structures de données nécessaires à jouer au morpion avec un damier ayant nbl lignes et nbc colones"""
    global Vide, ScoreVide
    #les cases
    Cases = [Vide for i in range(nbl*nbc)]
    #les quintuplés
    QTPL = []
    qtpl = 0
    #les quintuplés qui contiennent la case
    C2QTPL = [[] for i in range(nbl*nbc)]
    #quintuplés horizontaux
    for i in range(nbl):
        for j in range(nbc-4):
            QTPL += [(lc2ind(i, j, nbl, nbc), lc2ind(i, j+1, nbl, nbc), lc2ind(i, j+2, nbl, nbc), lc2ind(i, j+3, nbl, nbc), lc2ind(i, j+4, nbl, nbc))]
            C2QTPL[lc2ind(i, j, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i, j+1, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i, j+2, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i, j+3, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i, j+4, nbl, nbc)] += [qtpl]
            qtpl += 1
    #quintuplés verticaux
    for j in range(nbc):
        for i in range(nbl-4):
            QTPL += [(lc2ind(i, j, nbl, nbc), lc2ind(i+1, j, nbl, nbc), lc2ind(i+2, j, nbl, nbc),lc2ind(i+3, j, nbl, nbc), lc2ind(i+4, j, nbl, nbc))]
            C2QTPL[lc2ind(i, j, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i+1, j, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i+2, j, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i+3, j, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i+4, j, nbl, nbc)] += [qtpl]
            qtpl += 1
    #quintuplés diagonaux, vers le bas à droite
    for i in range(nbl-4):
        for j in range(nbc-4):
            QTPL += [(lc2ind(i, j, nbl, nbc), lc2ind(i+1, j+1, nbl, nbc), lc2ind(i+2, j+2, nbl, nbc), lc2ind(i+3, j+3, nbl, nbc), lc2ind(i+4, j+4, nbl, nbc))]
            C2QTPL[lc2ind(i, j, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i+1, j+1, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i+2, j+2, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i+3, j+3, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i+4, j+4, nbl, nbc)] += [qtpl]
            qtpl += 1
    #quintuplés diagonaux, vers le bas à gauche
    for i in range(nbl-4):
        for j in range(4, nbc):
            QTPL += [(lc2ind(i, j, nbl, nbc), lc2ind(i+1, j-1, nbl, nbc), lc2ind(i+2, j-2, nbl, nbc), lc2ind(i+3, j-3, nbl, nbc), lc2ind(i+4, j-4, nbl, nbc))]
            C2QTPL[lc2ind(i, j, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i+1, j-1, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i+2, j-2, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i+3, j-3, nbl, nbc)] += [qtpl]
            C2QTPL[lc2ind(i+4, j-4, nbl, nbc)] += [qtpl]
            qtpl += 1
    #les scores des quintuplés
    QTPL2Score = [ScoreVide for i in range(len(QTPL))]
    C2Score = [Evalc(i, C2QTPL, QTPL2Score) for i in range(nbl*nbc)]
    return Cases, QTPL, C2QTPL, QTPL2Score, C2Score


def Evalq(qtpl, QTPL, Cases):
    """retourne la note du quintuplé d'indice qtpl"""
    global O, X, ScoreO, ScoreOO, ScoreOOO, ScoreOOOO, ScoreOOOOO, ScoreOX, ScoreVide, ScoreX, ScoreXX, ScoreXXX, ScoreXXXX, ScoreXXXXX
    L = []
    for c in QTPL[qtpl]:
        L += [Cases[c]]
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


def Evalc(ind, C2QTPL, QTPL2Score):
    """retourne la note de la case d'indice ind"""
    res = 0
    for qtpl in C2QTPL[ind]:
        res += abs(QTPL2Score[qtpl])
    return res


def UpdateScore(coup, Cases, QTPL, C2QTPL, QTPL2Score, C2Score):
    """après un coup (modification du contenu de la case d'indice coup), mets à jour tous les scores impactés par ce coup"""
    UpdateCases = set()
    for qtpl in C2QTPL[coup]:
        QTPL2Score[qtpl] = Evalq(qtpl, QTPL, Cases)
        for case in QTPL[qtpl]:
            UpdateCases.add(case)
    for case in UpdateCases:
        C2Score[case] = Evalc(case, C2QTPL, QTPL2Score)
    return QTPL2Score, C2Score


def CoupJouer(Cases, C2Score):
    """détermine le meilleur coup à jouer"""
    global Vide
    coup = Cases.index(Vide)
    Scorecoup = C2Score[coup]
    for i in range(len(Cases)):
        if Cases[i] != Vide:
            pass
        elif C2Score[i] >= Scorecoup:
            Scorecoup = C2Score[i]
            coup = i
    return coup


def Affiche(Cases, nbl, nbc):
    """affiche le damier"""
    print(' ', [str(i) for i in range(nbc)])
    for i in range(nbl):
        print(i,Cases[lc2ind(i, 0, nbl, nbc):lc2ind(i, nbc, nbl, nbc)])


def Victoire(Cases, QTPL):
    """détermine si un joueur a gagngé (5 symboles identiques alignés)"""
    global O, X
    QTPL_C = []
    for qtpl in range(len(QTPL)):
        qtpl_c = []
        for case in QTPL[qtpl]:
            qtpl_c += [Cases[case]]
        QTPL_C += [qtpl_c]
    if [O, O, O, O, O] in QTPL_C:
        return 1
    elif [X, X, X, X, X] in QTPL_C:
        return 1
    return 0
