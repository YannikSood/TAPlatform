import random
from time import sleep
import sys
import csv
import matplotlib.pyplot as plt
class node():
    def __init__(self,math,nodes):
        self.result = 0
        self.scale_factor = 1
        self.math = math
        self.nodes = nodes
class ML():
    def __init__(self,params=[]):
        ######################################################################################################
        NODE_COUNT = 6  #CHANGE THIS NUMBER ####################
        ######################################################################################################
        self.status = True
        self.x_axis = []
        self.y_axis = []
        self.x_axis_hold = []
        self.x2_axis_change = []
        if params == []:
            self.file_source = "people1.csv"
            self.csv_len = 6
        else:
            self.create_csv(params)
            self.file_source = "temp.csv"

    
        f = open(self.file_source,"r")
        csv_file = csv.reader(f, delimiter=',')
        i = 0
        self.column_avg = []
        
        for data in csv_file:
            if i == 0:
                for item in data:
                    try:
                        self.column_avg.append(int(float(item)*100))
                    except:
                        continue
            
            else:
                c = 0
                for item in data:
                    try:
                        self.column_avg[c] += int(float(item)*100)
                    except:
                        continue
                    c += 1
            self.y_axis.append(i)
            self.x_axis.append(0)
            self.x2_axis_change.append(0)
            self.x_axis_hold.append(0)
            i+=1
        self.column_avg = [x / i for x in self.column_avg]  
       
        f.close()


        self.count = 0
        self.node_arr = []
        for i in range(NODE_COUNT):
            self.node_arr.append([])
        self.revert_count = 1
        self.names = ["0: Sentiment","1: Bull Bear","2: Mentions","3: Bull","4: Bear"]
        self.result = 100000000000
        self.dif = 100
        for c in range(1,len(self.node_arr)):
            for i in range(10):
                if c == 1:
                    
                    self.node_arr[c].append(node("A",list(range(self.csv_len))))
                else:
                    self.node_arr[c].append(node("A",[0,1,2,3,4,5,6,7,8,9]))
        while abs(self.dif) > 10:
            self.dif = 0
            self.learn()
            #print(self.revert_count)
            if (self.revert_count % (1000)) == 0 and self.revert_count != 0:
                print(int(self.revert_count)/1000)
            if self.revert_count > 1000:     
                self.node_arr[self.layer][self.node_num] = self.old_node
               
                self.dump()
            #    for i in range(len(self.y_axis)):
            #        plt.plot([i,i],[self.x_axis[i],self.x2_axis_change[i]]) 
            #    plt.plot(self.y_axis,self.x_axis,"ro")
            #    plt.plot(self.y_axis,self.x2_axis_change,"bo")
                
                #plt.show()

                self.status = False
                
                break

    def learn(self):
    
        f = open(self.file_source,"r")
        csv_file = csv.reader(f, delimiter=',')
        data = []
        for dhold in csv_file:
            data.append(dhold)
        f.close()
        self.data_len = len(data)
        
        for i in range(len(data)):
            if len(self.node_arr[0]) == 0:
                
                
                for c in range(1,len(data[i])-2):
                    nhold = node("XX",[])
                    nhold.result = int(float(data[i][c])*100/self.column_avg[c-1]) - 50
                    self.node_arr[0].append(nhold)
              
                self.change = float(data[i][-1].split(" ")[0])
                
            else:    

                for c in range(1,len(data[i])-2):
                    self.node_arr[0][c-1].result = int(float(data[i][c])*100/self.column_avg[c-1]) - 50
         
                
                self.change = int(float(data[i][-1].split(" ")[0])*100)
               
            self.compute(i)
       
        self.compare()
        
        self.change_d()
      
        
        
    def change_d(self):
        m_arr = ["A","S","M","D","N"]
        self.layer = random.randint(1,len(self.node_arr)-1)
        self.node_num = random.randint(0,len(self.node_arr[1])-1)
        m_num = random.randint(2,len(self.node_arr[self.layer-1])-1)
        in_arr = []
        for i in range(m_num):
            in_arr.append(random.randint(0,len(self.node_arr[self.layer-1])-1))
        math_num = random.randint(0,len(m_arr)-1)
        self.old_node = self.node_arr[self.layer][self.node_num]
        self.node_arr[self.layer][self.node_num] = node(m_arr[math_num],in_arr)

    def compute(self, i_send):
        d_sum = 0
        for i in range(1,len(self.node_arr)):
            for c in range(len(self.node_arr[i])):
                if self.node_arr[i][c].math == "A":
                    self.node_arr[i][c].result = self.node_arr[i-1][self.node_arr[i][c].nodes[0]].result
                    for x in range(1,len(self.node_arr[i][c].nodes)):
                        
                        self.node_arr[i][c].result += self.node_arr[i-1][self.node_arr[i][c].nodes[x]].result
                elif self.node_arr[i][c].math == "S":
                    self.node_arr[i][c].result = self.node_arr[i-1][self.node_arr[i][c].nodes[0]].result
                    for x in range(1,len(self.node_arr[i][c].nodes)):
                        self.node_arr[i][c].result -= self.node_arr[i-1][self.node_arr[i][c].nodes[x]].result
                elif self.node_arr[i][c].math == "M":
                    self.node_arr[i][c].result = self.node_arr[i-1][self.node_arr[i][c].nodes[0]].result
                    for x in range(1,len(self.node_arr[i][c].nodes)):
                        self.node_arr[i][c].result *= self.node_arr[i-1][self.node_arr[i][c].nodes[x]].result
                elif self.node_arr[i][c].math == "D":
                    self.node_arr[i][c].result = self.node_arr[i-1][self.node_arr[i][c].nodes[0]].result
                    for x in range(1,len(self.node_arr[i][c].nodes)):
                        try:
                            self.node_arr[i][c].result /= self.node_arr[i-1][self.node_arr[i][c].nodes[x]].result
                        except:
                            self.node_arr[i][c].result = 0
                elif self.node_arr[i][c] == "N":
                    self.node_arr[i][c].result = 0
        
        for c in range(len(self.node_arr[-1])):
            d_sum += self.node_arr[i][c].result 
        self.dif += abs(d_sum-self.change)
        self.x_axis_hold[i_send] = d_sum/100
        self.x2_axis_change[i_send] = self.change/100
        
        
   
    def compare(self):
        node_tot = 0
        
        for i in range(len(self.node_arr[-1])):
            node_tot += self.node_arr[-1][i].result
        
        if self.result <= self.dif:
            
            self.node_arr[self.layer][self.node_num] = self.old_node
          
            self.revert_count +=1
        else:
            self.result = self.dif
            
            print(str(self.result/(100*float(self.data_len)))[:5])
            self.count += 1
            self.x_axis = self.x_axis_hold[:]
        
            self.revert_count = 0

    def dump(self):
        print(self.names)
        for c in range(len(self.node_arr[1])):
            for i in range(1, len(self.node_arr)):
                self.print_node(self.node_arr[i][c])
            print("")
            
    def print_node(self, node_obj):
        print(str(node_obj.math) + " " + str(node_obj.scale_factor)[:4] + " " + str(node_obj.nodes) + " " + str(node_obj.result)[:5]+"\t\t\t", end="")

    def create_csv(self,parmas):
        
        HT = {  "S":1,
                "A":2,
                "M":3,
                "B":4,
                "E":5,
                "G":6,
                "V":7
        }
        row_array = [0]
        for character in params:
            row_array.append(HT[character])
        
        f = open('people1.csv',"r")
        csv_file = csv.reader(f, delimiter=',')
        
        csvFile = open('temp.csv', 'w+')
        writer = csv.writer(csvFile)
        for data in csv_file:
            hold = []
            for r_loc in row_array:
                hold.append(data[r_loc])
            hold.append(data[-2])
            hold.append(data[-1])
            writer.writerow(hold)
            
        f.close()
        csvFile.close()
        self.csv_len = len(hold) - 3
        

def columna():
    try:
        f = open("temp.csv","r")
    except:
        f = open("people1.csv","r")

    csv_file = csv.reader(f, delimiter=',')
    i = 0
    column_avg = []
        
    for data in csv_file:
        if i == 0:
            for item in data:
                try:
                    column_avg.append(int(float(item)*100))
                except:
                    continue
            
        else:
            c = 0
            for item in data:
                try:
                    column_avg[c] += int(float(item)*100)
                except:
                    continue
                c += 1
       
        i+=1
    column_avg = [x / i for x in column_avg]  
    f.close()
    return column_avg
        

def calculate():
    column_avg = columna()
    f = open("LOAD.txt","r")
    nodes = f.readlines()
    f.close()
    f = open("TEST.txt","r")
    test_data = f.readlines()
    f.close()
    node_arr = []
    node_arr.append([])
    for b in range(len(test_data)):
        nhold = node("XX",[])
        nhold.result = int(float(test_data[b].split(" ")[-1][:-1])*100/column_avg[b]) - 50
        node_arr[0].append(nhold)


    for i in range(len(nodes)):
        line = nodes[i].split(".")
        node_arr.append([])
        for c in range(len(line)-1):
            arr = line[c][3:-2]
            arr = arr.split(",")
            n_arr = []
            for x in range(len(arr)):
                n_arr.append(int(arr[x]))
            node_arr[i+1].append(node(line[c][1],n_arr))

    for i in range(1,len(node_arr)):
        #print(i)
        for c in range(len(node_arr[i])):
            if node_arr[i][c].math == "A":
                node_arr[i][c].result = node_arr[i-1][node_arr[i][c].nodes[0]].result
                for x in range(1,len(node_arr[i][c].nodes)):
                    node_arr[i][c].result += node_arr[i-1][node_arr[i][c].nodes[x]].result
            elif node_arr[i][c].math == "S":
                node_arr[i][c].result = node_arr[i-1][node_arr[i][c].nodes[0]].result
                for x in range(1,len(node_arr[i][c].nodes)):
                    node_arr[i][c].result -= node_arr[i-1][node_arr[i][c].nodes[x]].result
            elif node_arr[i][c].math == "M":
                node_arr[i][c].result = node_arr[i-1][node_arr[i][c].nodes[0]].result
                for x in range(1,len(node_arr[i][c].nodes)):
                    node_arr[i][c].result *= node_arr[i-1][node_arr[i][c].nodes[x]].result
            elif node_arr[i][c].math == "D":
                node_arr[i][c].result = node_arr[i-1][node_arr[i][c].nodes[0]].result
                for x in range(1,len(node_arr[i][c].nodes)):
                    try:
                        node_arr[i][c].result /= node_arr[i-1][node_arr[i][c].nodes[x]].result
                    except:
                        node_arr[i][c].result = 0
            elif node_arr[i][c] == "N":
                node_arr[i][c].result = 0
           
    d_sum = 0

    for c in range(len(node_arr[-1])):
        d_sum += node_arr[-1][c].result 
    print(float(d_sum/100))
    #dump(node_arr)
def dump(node_arr):
  
    for c in range(len(node_arr[1])):
        for i in range(1, len(node_arr)):
            print_node(node_arr[i][c])
        print("")
            
def print_node(node_obj):
    print(str(node_obj.math) + " " +str(node_obj.nodes) + " " + str(node_obj.result)[:5]+"\t\t\t", end="")

if __name__=="__main__":
    
    hold = 1000000
    best = ''
    i = 1
    cla = ''
    params = ''
    try:    
        cla = sys.argv[1]
        params = sys.argv[2]
    except:
        pass
   
    if cla == "l":
        calculate()
        exit(0)
    if params == '':
        ml_obj = ML()
    else:
        ml_obj = ML(params=params)
    if ml_obj.result < hold:
            print(str(ml_obj.result/float(ml_obj.data_len))[:5])
            print(str(ml_obj.result))
            ml_obj.dump()
            
            hold = ml_obj.result
            best = ml_obj.node_arr
    
    while not ml_obj.status:
        if i > 0:
            break

        if params == '':
            ml_obj = ML()
        else:
            ml_obj = ML(params=params)
        if ml_obj.result < hold:
            print(str(ml_obj.result/float(ml_obj.data_len))[:5])
            print(str(ml_obj.result))
            ml_obj.dump()
            
            hold = ml_obj.result
            best = ml_obj.node_arr
        
        i+=1
    
    if cla == '':
        exit(0)
      
    if sys.argv[1] == "s":
        print("store")
        f = open("LOAD.txt","w")
        for i in range(1,len(best)):
            for c in range(len(best[i])):
                f.write("[" + str(best[i][c].math) + str(best[i][c].nodes) + "].")
            f.write('\n')
        f.close()
    
    
 
