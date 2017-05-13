import csv
import math
from decimal import *
from multiprocessing import Process, Lock,Queue


class Decision:
    "Loads The CSV and perform Rule Extraction...."

    def __init__(self):
        # VARABLE DECLERATION
        self.k = 5
        self.l = Lock()
        self.bestPerfomance = []
        # LOAD THE DATA
        self.loadedList = self.load()
        # No Of collections and number genes in each collection
        self.testData = self.loadedList[0:10]
        self.loadedList = self.loadedList[10:62]
        self.length = len(self.loadedList)
        self.genes = len(self.loadedList[0]) - 1

    def load(self):
        # LOAD CSV AND RETUEN A LIST
        line = csv.reader(open("colonTumor.data", "r"))
        datas = list(line)
        #convert str to nums
        temp = []
        for i in range(len(datas)):
            temp.append([Decimal(datas[i][j])for j in range(len(datas[0])-1)])
            temp[i].append(datas[i][-1])
        return temp

    def __call__(self):
        # Iterate Through 2000 genes as i and inside iterate through same
        # values as j
        q =Queue()
        q.put([])
        for i in range(self.genes):
            print("Gene : ",i)
            #STart Processing
            pone = Process(target=self.ruleChecking, args=(i,[0,500],q))
            ptwo = Process(target=self.ruleChecking, args=(i,[500,1000],q))
            pthree = Process(target=self.ruleChecking, args=(i,[1000,1500],q))
            pfour = Process(target=self.ruleChecking, args=(i,[1500,2000],q))
            pone.start()
            ptwo.start()
            pthree.start()
            pfour.start()
            pone.join()
            ptwo.join()
            pthree.join()
            pfour.join()
        self.bestPerfomance = q.get()
        self.predict()

    def ruleChecking(self,i,iterlist,q):
         for j in range(iterlist[0],iterlist[1]):
             # if value of ithh gene > jth index gene its positive else negative
             # where i != j
             if i != j :
                perfomance = self.findPerfomance(i, j)
                self.l.acquire()
                bestPerfomance = q.get()
                if len(bestPerfomance) < self.k:
                    bestPerfomance.append([i, j, perfomance])
                else:
                    insert = [i, j, perfomance]
                    for i in range(self.k):
                        if bestPerfomance[i][-1] < insert[-1]:
                            insert, bestPerfomance[i] = bestPerfomance[i], insert
                q.put(bestPerfomance)
                self.l.release()

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

    def predict(self):
        correct = 0
        #THE STRING IS USED FOR WRITING TO FILE
        result = str()
        #for each testData
        for row in self.testData:
            pos,neg = self.calcs(row)
            #check TOTAL POSITIVE AND NEGATIVE DECISIONS TO DECIDE WHETHER THE RESULT
            if pos > neg :
                if row[-1] == 'positive':
                    correct += 1
                result += "positive, "+row[-1]+"\n"
            else:
                if row[-1] == 'negative':
                    correct += 1
                result += "negative, "+row[-1]+"\n"
        print(result)
        #wRITE TO FILE
        with open("result.csv","w") as fpointer:
            fpointer.write(result)
        print(float(correct)/10*100)

    def calcs(self,row):
         neg = 0
         pos = 0
         #ECHECK ALL DECISION RULE FOR POSITIVE OR NEGATOVE
         for x in range(self.k):
            if row[self.bestPerfomance[x][0]] > row[self.bestPerfomance[x][1]]:
                pos += 1
            else:
                neg += 1
         return pos,neg

    
    def run(self,filename):
        #predict for unlabeled data
        line = csv.reader(open(filename, "r"))
        datas = list(line)
        #FOE EACH ROW IN INPUT FILE predict
        for i in range(len(datas)):
           data = [Decimal(datas[i][j])for j in range(len(datas[i]))]
           pos,neg = self.calcs(data)
           if pos > neg:
                print(i,": positive")
           else:
                print(i,": negative")
            
def main():
    #TRain with part of datas
    clf = Decision()
    #FIND THE Accuracy
    clf()
    #predict for data that is in another csv file (unlabeled)
    choice = int(input("1 For classifying data:"))
    if choice == 1 :
        clf.run("test.csv")

if __name__ == "__main__":
    main()
