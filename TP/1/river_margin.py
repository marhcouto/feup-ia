from distutils.log import error


class BoatError(Exception):
    pass

class RiverMargin:

    def __init__(self, CB, MB, CA, MA, margin, parent):
        self.CB = CB
        self.CA = CA
        self.MB = MB
        self.MA = MA
        self.margin = margin
        self.parent = parent

    def cannibalsAB(self):
        if (self.CB + 2 <= self.MB or self.MB == 0) and self.CA >= 2 and self.margin == 'A':
            return RiverMargin(self.CB + 2, self.MB, self.CA - 2, self.MA, 'B', self)
        else:
            raise BoatError()

    def cannibalsBA(self):
        if (self.CA + 2 <= self.MA or self.MA == 0) and self.CB >= 2 and self.margin == 'B':
            return RiverMargin(self.CB - 2, self.MB, self.CA + 2, self.MA, 'A', self)
        else:
            raise BoatError()

    def missionariesAB(self):
        if (self.CA <= self.MA - 2 or self.MA == 2) and self.MA >= 2 and self.margin == 'A':
            return RiverMargin(self.CB, self.MB + 2, self.CA, self.MA - 2, 'B', self)
        else:
            raise BoatError()

    def missionariesBA(self):
        if (self.CB <= self.MB - 2 or self.MB == 2) and self.MB >= 2 and self.margin == 'B':
            return RiverMargin(self.CB, self.MB - 2, self.CA, self.MA + 2, 'A', self)
        else:
            raise BoatError()

    def cannibalAB(self):
        if (self.CB + 1 <= self.MB or self.MB == 0) and self.CA >= 1 and self.margin == 'A':
            return RiverMargin(self.CB + 1, self.MB, self.CA - 1, self.MA, 'B', self)
        else:
            raise BoatError()

    def cannibalBA(self):
        if (self.CA + 1 <= self.MA or self.MA == 0) and self.CB >= 1 and self.margin == 'B':
            return RiverMargin(self.CB - 1, self.MB, self.CA + 1, self.MA, 'A', self)
        else:
            raise BoatError()

    def missionaryAB(self):
        if (self.CA <= self.MA - 1 or self.MA == 1) and self.MA >= 1 and self.margin == 'A':
            return RiverMargin(self.CB, self.MB + 1, self.CA, self.MA - 1, 'B', self)
        else:
            raise BoatError()

    def missionaryBA(self):
        if (self.CB <= self.MB - 1 or self.MB == 1) and self.MB >= 1 and self.margin == 'B':
            return RiverMargin(self.CB, self.MB - 1, self.CA, self.MA + 1, 'A', self)
        else:
            raise BoatError()
        
    def mixedAB(self):
        if self.MA >= 1 and self.CA >= 1 and self.MB >= self.CB and self.margin == 'A':
            return RiverMargin(self.CB + 1, self.MB + 1, self.CA - 1, self.MA - 1, 'B', self)
        else:
            raise BoatError()

    def mixedBA(self):
        if self.MB >= 1 and self.CB >= 1 and self.MA >= self.CA and self.margin == 'B':
            return RiverMargin(self.CB - 1, self.MB - 1, self.CA + 1, self.MA + 1, 'A', self)
        else:
            raise BoatError()

    def __eq__(self, other):
        return self.CA == other.CA and self.CB == other.CB and self.MA == other.MA and self.MB == other.MB and self.margin == other.margin

    def __hash__(self):
        return hash((self.CA, self.CB, self.MA, self.MB, self.margin))

    def __str__(self):
        return "CB:{}|MB:{}|CA:{}|MA:{}|Margin:{}".format(self.CB, self.MB, self.CA, self.MA, self.margin)
    