from distutils.command.build import build


# Build dictionary that associates pairs of disciplines with students in common
def incompatibilityTableGenerator(disciplineDict):
    
    res = dict()

    for i in range(0, len(disciplineDict)):
        for j in range(i + 1, len(disciplineDict)):
            disc1, students1 = list(disciplineDict.items())[i]
            disc2, students2 = list(disciplineDict.items())[j]
            res[(disc1, disc2)] = len(students1.intersection(students2))

    return res


# Builds the dictionary that assigns classes to students enrolled
def dictionaryBuilder():

    with open("data.txt", "r") as f:
        lines = f.readlines()

    lines = list(map(lambda s: set(map(int, s[:-1].split())), lines))

    res = dict()

    for i in range(1, len(lines)):
        res[i] = lines[i]

    return res



def overlappingStudents(incompatibilityTable, possibleSolution):

    noOverlapping = 0

    for i in range(0, len(possibleSolution)):
        for j in range(i + 1, len(possibleSolution)):
            if possibleSolution[i] == possibleSolution[j]:
                noOverlapping += incompatibilityTable[(i, j)]

    return noOverlapping



if __name__ == "__main__":

    discStudentDictionary = dictionaryBuilder()
    print("Disciplines-Students dictionary:\n", discStudentDictionary)
    incompatibilityTable = incompatibilityTableGenerator(discStudentDictionary)
    print("\nIncompatibility Table:\n", incompatibilityTable) 



