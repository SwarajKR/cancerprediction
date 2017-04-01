import csv
import math
from decimal import *

class Decision:
    "Loads The CSV and perform Rule Extraction...."

    def __init__(self):
        # VARABLE DECLERATION
        self.k = 7
        self.bestPerfomance = []
        # LOAD THE DATA
        self.loadedList = self.load()
        # No Of collections and number genes in each collection
        self.testData = self.loadedList[0:8]
        self.loadedList = self.loadedList[8:73]
        self.testData.extend(self.loadedList[57:64])
        self.loadedList = self.loadedList[0:57]
        self.length = len(self.loadedList)
        self.genes = len(self.loadedList[0]) - 1

    def load(self):
        # LOAD CSV AND RETUEN A LIST
        line = csv.reader(open("/home/oem/Documents/train_test_merge.csv", "r"))
        datas = list(line)
        del datas[0]
        #convert str to nums
        temp = []
        for i in range(len(datas)):
            temp.append([Decimal(datas[i][j])for j in range(len(datas[0])-1)])
            temp[i].append(datas[i][-1])
        return temp

    def __call__(self):
        # Iterate Through 2000 genes as i and inside iterate through same
        # values as j
        for i in range(self.genes):
            # if value of ithh gene > jth index gene its positive else negative
            # where i != j
            print("Gene ",i)
            for j in range(self.genes):
                if i != j :
                    perfomance = self.findPerfomance(i, j)
                    self.addToArray(perfomance, i, j)
        print(self.bestPerfomance)
        self.predict()

    def findPerfomance(self, i, j):
        # true/false all/aml
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        # Counting true/false all/aml
        for row in self.loadedList:
            if row[i] > row[j]:
                if row[-1] == "ALL":
                    tp += 1
                else:
                    fp += 1
            else:
                if row[-1] == "AML":
                    tn += 1
                else:
                    fn += 1
        # Calculate Accuracy,precision,recall (float is used since 0 is
        # produced instead of 0.) for py 2.7
        try:
            accuracy = float(tp + tn) / self.length
        except ZeroDivisionError:
            return 0
        try:
            precision = float(tp) / (tp + fp)
        except ZeroDivisionError:
            return 0
        try:
            recall = float(tp) / (tp + fn)
        except ZeroDivisionError:
            return 0
        try:
            tnr = float(tn) / (tn + fp)
        except ZeroDivisionError:
            return 0
        # FMEASURE AND  GMEAN ARE CALCULATED USING THE ABOVE
        try:
            fMeasure = (2 * precision * recall) / (precision + recall)
        except ZeroDivisionError:
            return 0
        try:
            gMean = math.sqrt(recall * tnr)
        except ZeroDivisionError:
            return 0
        # calculate peromance alpha,beta,gamma are given value 1/3 directly
        peromance = ((1.0 / 3) * accuracy + (1.0 / 3)
                     * fMeasure + (1.0 / 3) * gMean)
        return peromance

    def addToArray(self, perfomance, i, j):
        if len(self.bestPerfomance) < self.k:
            self.bestPerfomance.append([i, j, perfomance])
        else:
            insert = [i, j, perfomance]
            for i in range(self.k):
                if self.bestPerfomance[i][-1] < insert[-1]:
                    insert, self.bestPerfomance[i] = self.bestPerfomance[i], insert

    def predict(self):
        correct = 0
        for row in self.testData:
            all = 0
            aml = 0
            for x in range(self.k):
                if row[self.bestPerfomance[x][0]] > row[self.bestPerfomance[x][1]]:
                    all += 1
                else:
                    aml += 1
            if all > aml and row[-1] == 'ALL':
                correct +=1
            elif row[-1] == 'AML':
                correct += 1
        print(float(correct)/15*100)
            
def main():
    clf = Decision()
    clf()

if __name__ == "__main__":
    main()