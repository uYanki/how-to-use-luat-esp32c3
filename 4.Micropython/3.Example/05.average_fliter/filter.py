class AverageFliter:
    def __init__(self,lenth = 10):
        self.lenth = lenth
        self.data = []
    def update(self,value):
        if(len(self.data)<self.lenth):
            self.data.append(value)
        else:
            self.data.pop(0)
            self.data.append(value)
    def value(self):
        if(len(self.data)<self.lenth):
            return sum(self.data)/len(self.data)
        else:
            return sum(self.data)-/self.lenth