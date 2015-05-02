# Tian Zhang, Jingyao Qin
# 2015 May

import csv
import c45
from random import randint
import sys

if __name__ == "__main__":
    if sys.argv[1] == "train":
        if ((len(sys.argv) == 6) and (sys.argv[2] == "unpru")) or ((len(sys.argv) == 7) and (sys.argv[2] == "pru")):
            ratio = float(sys.argv[4])
            trainObjects = []
            trainResult = []
            formatting = []
            with open("./" + sys.argv[5], 'rU') as csvfile:
                formatReader = csv.reader(csvfile)
                formatReader.next()
                temp = formatReader.next()
                for attribute in temp:
                    formatting.append(attribute)
            with open("./" + sys.argv[3], 'rU') as csvfile:
                rowCount = sum(1 for row in csvfile)
                begin = randint(0, int(rowCount * (1 - ratio)))
                end = begin + int(rowCount * ratio)
                print("Data range: from row " + str(begin) + " to row " + str(end))
            with open("./" + sys.argv[3], 'rU') as csvfile1:
                i = -1
                trainReader = csv.reader(csvfile1)
                for trainContent in trainReader:
                    i += 1
                    if i ==0 or (i >= begin and i <= end):
                        trainObjects.append(trainContent[:-1])
                        trainResult.append(trainContent[-1:])
                    else:
                        continue
            c45.train(trainObjects, trainResult, "unprunedTree.xml", formatting)

            unpruneSplits = c45.countSplits("unprunedTree.xml")
            print("Splits of the unpruned tree:" + str(unpruneSplits))

            c45.outPut_unpruned()

            if sys.argv[2] == "pru":
                validateObjects_Pruned = []; result_Pruned = [];
                with open("./" + sys.argv[6], 'rU') as csvfile2:
                    validateReader_Pruned = csv.reader(csvfile2)
                    for validateContent_Pruned in validateReader_Pruned:
                        #Record the objects for validation
                        validateObjects_Pruned.append(validateContent_Pruned[:-1])
                        #record the results which is used for validation
                        result_Pruned.append(validateContent_Pruned[-1])
                    result_Pruned.pop(0)
                c45.prune("unprunedTree.xml", validateObjects_Pruned,result_Pruned)

                prunedSplits = c45.countSplits("prunedTree.xml")
                print ("Splits of the pruned tree:" + str(prunedSplits))

                c45.outPut_pruned()
        else:
            c45.error()
    elif sys.argv[1] == "validate":
        if len(sys.argv) != 4:
            c45.error()
        else:
            print "Validating..."
            validateObjects_Pruned = []
            result_Pruned = []
            with open("./" + sys.argv[3], 'rU') as csvfile3:
                validateReader_Pruned = csv.reader(csvfile3)
                for validateContent_Pruned in validateReader_Pruned:
                    #Record the objects for validation
                    validateObjects_Pruned.append(validateContent_Pruned[:-1])
                    #record the results which is used for validation
                    result_Pruned.append(validateContent_Pruned[-1])
                result_Pruned.pop(0)

            validatePrediction_Pruned = c45.predict(sys.argv[2],validateObjects_Pruned)
            wrongResult_Pruned = 0
            for a in range(len(result_Pruned)):
                if not result_Pruned[a] == validatePrediction_Pruned[a]:
                    wrongResult_Pruned += 1
            print "Accuracy =", round((1-float(wrongResult_Pruned) / len(validatePrediction_Pruned)) * 100, 2), "%"

    elif sys.argv[1] == "predict":
        if len(sys.argv) != 4:
            c45.error()
        else:
            print "Predicting..."
            testObjects = []; testAnswer = [];
            with open("./" + sys.argv[3], 'rU') as csvfile4:
                testReader = csv.reader(csvfile4)
                for testContent in testReader:
                    #Record the objects for test
                    testObjects.append(testContent[:-1])
                    #Record the results which is used for test
                    testAnswer.append(testContent[-1])
                testAnswer.pop(0)

            testPrediction=c45.predict(sys.argv[2],testObjects)
            writer=csv.writer(open("predict.csv", 'wb'))
            testPrediction.insert(0, "group")
            for a in range(len(testPrediction)):
                testObjects[a].append(testPrediction[a])
            writer.writerows(testObjects)
    else:
        c45.error()
