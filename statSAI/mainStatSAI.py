import os, csv

def Remove(duplicate):
    final = []
    for num in duplicate:
        if num not in final:
            final.append(num)
    return final

def readJson(names):

    listClasses = ['MappedCode', 'CorporateBodyClassification', 'XlNotation', 'XlNote', 'Concept', 'Label', 'Corporate', 'Country', 'Membership', 'Currency',
                   'Language', 'MembershipClassification', 'Place', 'SpatialThing', 'Site', 'Address']
    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/statSAI/statCSV")
    helperList = []
    for name in names:
        with open(str(name)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            count, ct = 0, 0
            for row in csv_reader:
                for cl in listClasses:
                    if cl in str(row[0]):
                        helperList.append((row[0], row[1], row[7], "Usage: " + str(row[2]) + " out of " + str(row[3]), name))
                        ct += 1
                count += 1
            #print("Number of Lines: " + str(count), "|| Number of properties for desired classes: " + str(ct))

    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/statSAI")
    return helperList

def createOutput(listProblem):

    finalHash, helper = {}, ['corporate-body-classification-skos-ap-act.csv', 'corporatebodies-skos-ap-act.csv', 'countries-skos-ap-act.csv', 'currencies-skos-ap-act.csv',
                             'languages-skos-ap-act.csv', 'membership-classification-skos-.csv', 'places-skos-ap-act.csv', 'sites-skos-ap-act.csv']
    for line in listProblem:
        if finalHash.get(str(line[0]) + "***" + str(line[1])) == None:
            finalHash.setdefault(str(line[0]) + "***" + str(line[1]), []).append((float(line[2]), line[4]))
        else:
            finalHash[str(line[0]) + "***" + str(line[1])].append((float(line[2]), line[4]))

    final = {}
    for pr in finalHash:
        tempFirst = []
        for name in finalHash[pr]:
            tempFirst.append(name[1])
        tempSecond = []
        for h in helper:
            if h not in tempFirst:
                tempSecond.append((0.0, h))
        final[pr] = finalHash[pr] + tempSecond
        final[pr] = Remove(final[pr])
        # if len(final[pr]) != 8:
        #     print(pr, final[pr], len(final[pr]))
        final[pr].sort(key=lambda a: a[1])
    return final

def generate(final):
    for f in final:
        print(final[f])
        break
    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/statSAI/results")
    with open('average.csv', 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Class', 'Property', 'Corporate Body Classification', 'Corporate Body', 'Country', 'Currencies', 'Languages', 'Membership', 'Places', 'Sites'])
        for row in final:
            h = row.split("***")
            csv_out.writerow([h[0], h[1], final[row][0][0], final[row][1][0], final[row][2][0], final[row][3][0], final[row][4][0], final[row][5][0], final[row][6][0], final[row][7][0]])
    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/statSAI")

    return 1

def createOutputUsage(listProblem):

    finalHash, helper = {}, ['corporate-body-classification-skos-ap-act.csv', 'corporatebodies-skos-ap-act.csv', 'countries-skos-ap-act.csv', 'currencies-skos-ap-act.csv',
                             'languages-skos-ap-act.csv', 'membership-classification-skos-.csv', 'places-skos-ap-act.csv', 'sites-skos-ap-act.csv']
    for line in listProblem:
        if finalHash.get(str(line[0]) + "***" + str(line[1])) == None:
            finalHash.setdefault(str(line[0]) + "***" + str(line[1]), []).append((line[3], line[4]))
        else:
            finalHash[str(line[0]) + "***" + str(line[1])].append((line[3], line[4]))

    final = {}
    for pr in finalHash:
        tempFirst = []
        for name in finalHash[pr]:
            tempFirst.append(name[1])
        tempSecond = []
        for h in helper:
            if h not in tempFirst:
                tempSecond.append(("Not used", h))
        final[pr] = finalHash[pr] + tempSecond
        final[pr] = Remove(final[pr])
        # if len(final[pr]) != 8:
        #     print(pr, final[pr], len(final[pr]))
        final[pr].sort(key=lambda a: a[1])
    return final

def generateUsage(final):
    for f in final:
        print(final[f])
        break
    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/statSAI/results")
    with open('usage.csv', 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Class', 'Property', 'Corporate Body Classification', 'Corporate Body', 'Country', 'Currencies', 'Languages', 'Membership', 'Places', 'Sites'])
        for row in final:
            h = row.split("***")
            csv_out.writerow([h[0], h[1], final[row][0][0], final[row][1][0], final[row][2][0], final[row][3][0], final[row][4][0], final[row][5][0], final[row][6][0], final[row][7][0]])
    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/statSAI")

    return 1

def findMissing(listProblem):
    finalHash, helper = {}, ['corporate-body-classification-skos-ap-act.csv', 'corporatebodies-skos-ap-act.csv', 'countries-skos-ap-act.csv', 'currencies-skos-ap-act.csv',
                             'languages-skos-ap-act.csv', 'membership-classification-skos-.csv', 'places-skos-ap-act.csv', 'sites-skos-ap-act.csv']

    for line in listProblem:
        if finalHash.get(str(line[1])) == None:
            finalHash.setdefault(str(line[1]), []).append(("Used", line[4]))
        else:
            finalHash[str(line[1])].append(("Used", line[4]))

    finalClass = {}
    for line in listProblem:
        if finalClass.get(str(line[1])) == None:
            finalClass.setdefault(str(line[1]), []).append((line[0]))
        else:
            finalClass[str(line[1])].append((line[0]))

    final = {}
    for pr in finalHash:
        tempFirst = []
        for name in finalHash[pr]:
            tempFirst.append(name[1])
        tempSecond = []
        for h in helper:
            if h not in tempFirst:
                tempSecond.append(("Not used", h))
        final[pr] = finalHash[pr] + tempSecond
        final[pr] = Remove(final[pr])
        final[pr].sort(key=lambda a: a[1])

    # for pr in final:
    #     print(final[pr], len(final[pr]))

    return final, finalClass

def missingOutput(final):
    for f in final:
        print(final[f])
        break
    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/statSAI/results")
    with open('missing.csv', 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Property', 'Corporate Body Classification', 'Corporate Body', 'Country', 'Currencies', 'Languages', 'Membership', 'Places', 'Sites'])
        for row in final:
            csv_out.writerow([row, final[row][0][0], final[row][1][0], final[row][2][0], final[row][3][0], final[row][4][0], final[row][5][0], final[row][6][0], final[row][7][0]])
    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/statSAI")

def usedIn(finalClass):
    # for f in finalClass:
    #     print(finalClass[f])
    #     break
    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/statSAI/results")
    with open('usedIn.csv', 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Property', 'UsedIn'])
        for row in finalClass:
            tempList = [row]
            tempList.extend(finalClass[row])
            csv_out.writerow(tempList)
    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/statSAI")

if __name__=="__main__":
    names = os.listdir("C:/Users/USER/PycharmProjects/EuroStat/statSAI/statCSV")
    listProblem = readJson(names)
    # final = createOutput(listProblem)
    # flagGenerate = generate(final)
    # final = createOutputUsage(listProblem)
    # flagGenerate = generateUsage(final)
    final, finalClass = findMissing(listProblem)
    #flagMissing = missingOutput(final)
    flagUsedIn = usedIn(finalClass)