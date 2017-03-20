import csv
import math


class Decision:
    "Loads The CSV and perform Rule Extraction...."

    def __init__(self):
        # VARABLE DECLERATION
        self.k = 7
        self.bestPerfomance = []
        # LOAD THE DATA
        self.loadedList = self.load()
        # No Of collections and number genes in each collection
        self.length = len(self.loadedList)
        self.genes = len(self.loadedList[0]) - 1
        # THE Negatives and positives are seperated and stored in a dict
        self.seperated = {}
        self.seperated['positive'] = []
        self.seperated['negative'] = []
        for row in self.loadedList:
            if row[-1] == "positive":
                self.seperated['positive'].append(row[:-1])
            else:
                self.seperated['negative'].append(row[:-1])

    def load(self):
        # LOAD CSV AND RETUEN A LIST
        line = csv.reader(open("colonTumor.data", "rb"))
        datas = list(line)
        return datas

    def __call__(self):
        # Iterate Through 2000 genes as i and inside iterate through same
        # values as j
        for i in range(self.genes):
            # if value of ithh gene > jth index gene its positive else negative
            # where i != j
            for j in range(self.genes):
                if i != j :
                    perfomance = self.findPerfomance(i, j)
                    self.addToArray(perfomance, i, j)
        print(self.bestPerfomance)

    def findPerfomance(self, i, j):
        # true/false positive/negative
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        # Counting true/false positive/negative
        for row in self.loadedList:
            if row[i] > row[j]:
                if row[-1] == "positive":
                    tp += 1
                else:
                    fp += 1
            else:
                if row[-1] == "negative":
                    tn += 1
                else:
                    fn += 1
        # Calculate Accuracy,precision,recall (float is used since 0 is
        # produced instead of 0.)
        try :
            accuracy = float(tp + tn) / self.length
        except ZeroDivisionError:
            return 0
        try :
            precision = float(tp) / (tp + fp)
        except ZeroDivisionError:
            return 0
        try :
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
            insert = [i,j,perfomance]
            temp = []
            for i in range(self.k):
                if self.bestPerfomance[i][-1] < insert[-1]:
                    temp = self.bestPerfomance[i]
                    self.bestPerfomance[i] = insert
                    insert = temp

def main():
    object = Decision()
    object()

if __name__ == "__main__":
    main()
