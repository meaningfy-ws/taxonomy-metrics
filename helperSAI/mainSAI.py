import json, os, csv

def Remove(duplicate):
    final = []
    for num in duplicate:
        if num not in final:
            final.append(num)
    return final

def readJson(names):
    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/helperSAI/jana json")

    f = open(name)
    data = json.load(f)
    f.close()

    listJson = []
    for cl in data:
        try:
            for sub in data[cl]["results"]["bindings"]:
                listJson.append((cl, sub['property']['value'], sub['subject_count']['value'], sub['class_instance_count']['value'], sub['object_count']['value'], sub['min']['value'], sub['max']['value'], sub['avg']['value'], sub['property_types']['value'], sub['object_types']['value']))
        except Exception:
            pass

    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/helperSAI/jana csv")
    with open(str(name) + '.csv', 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['subject_class', 'property', 'subject_count', 'class_instance_count', 'object_count', 'min', 'max', 'avg', 'property_types', 'object_types'])
        for row in listJson:
            csv_out.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
    os.chdir("C:/Users/USER/PycharmProjects/EuroStat/helperSAI/")


if __name__=="__main__":
    names = os.listdir("C:/Users/USER/PycharmProjects/EuroStat/helperSAI/jana json")
    for name in names:
        listProblem = readJson(name)