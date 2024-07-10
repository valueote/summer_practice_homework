from numpy import *
import time
from texttable import Texttable
class CF:
    def __init__(self, movies, ratings, k=5, n=10):
        self.movies = movies
        self.ratings = ratings
        self.k = k
        self.n = n
        self.userDict = {}
        self.itemUser = {}
        self.neighbors = []
        self.recList = []
        self.cost = 0.0

    def recBaseUser(self, userId):
        self.formatRate()
        self.n = len(self.userDict[userId])
        self.getAdjacent(userId)
        self.getrecList(userId)

    def getrecList(self, userId):
        self.recList = []
        recDict = {}
        for neighbor in self.neighbors:
            movies = self.userDict[neighbor[1]]
            for movie in movies:
                if(movie[0] in recDict):
                    recDict[movie[0]] += neighbor[0]
                else:
                    recDict[movie[0]] = neighbor[0]
        for key in recDict:
            self.recList.append([recDict[key], key])
        self.recList.sort(reverse=True)
        self.recList = self.recList[:self.n]

    def formatRate(self):
        self.userDict = {}
        self.itemUser = {}
        for i in self.ratings:
            temp = (i[1], float(i[2]) / 5)
            if(i[0] in self.userDict):
                self.userDict[i[0]].append(temp)
            else:
                self.userDict[i[0]] = [temp]
            if(i[1] in self.itemUser):
                self.itemUser[i[1]].append(i[0])
            else:
                self.itemUser[i[1]] = [i[0]]

    def getAdjacent(self, userId):
        neighbors = []
        self.neighbors = []
        
        for i in self.userDict[userId]:
            for j in self.itemUser[i[0]]:
                if(j != userId and j not in neighbors):
                    neighbors.append(j) 
        for i in neighbors:
            dist = self.getCost(userId, i)
            self.neighbors.append([dist, i])
        self.neighbors.sort(reverse=True)
        self.neighbors = self.neighbors[:self.k]
            

    def formatUserDict(self, userId, l):
        user = {}
        for i in self.userDict[userId]:
            user[i[0]] = [i[1], 0]

        for j in self.userDict[l]:
            if(j[0] not in user):
                user[j[0]] = [0, j[1]]
            else:
                user[j[0]][1] = j[1]
        return user

    def getCost(self, userId, l):
        user = self.formatUserDict(userId, l)
        x = 0.0
        y = 0.0
        z = 0.0
        for k, v in user.items():
            x += float(v[0]) * float(v[0])
            y += float(v[1]) * float(v[1])
            z += float(v[0]) * float(v[1])
        if(z == 0.0):
            return 0
        return z / sqrt(x * y)

    def showTable(self):
        neighbors_id = [i[1] for i in self.neighbors]
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(["t", "t", "t", "t"])
        table.set_cols_align(["l", "l", "l", "l"])
        rows = []
        rows.append([u"movie ID", u"Name", u"release", u"from userID"])
        for item in self.recList:
            fromID = []
            for i in self.movies:
                if i[0] == item[1]:
                    movie = i
                    break
            for i in self.itemUser[item[1]]:
                if i in neighbors_id:
                    fromID.append(i)
            movie.append(fromID)
            rows.append(movie)
        table.add_rows(rows)
        print(table.draw())

def readFile(filename):
    files = open(filename, "r", encoding="iso-8859-15")
    data = []
    for line in files.readlines():
        item = line.strip().split("::")
        data.append(item)
    return data

movies = readFile("/home/vivy/linear/15/data/movies.txt")
ratings = readFile("/home/vivy/linear/15/data/ratings.txt")
demo = CF(movies, ratings, k=20)
demo.recBaseUser("600")
print("推荐列表为：")
demo.showTable()
print("处理%d 条数据：" % (len(demo.ratings)))