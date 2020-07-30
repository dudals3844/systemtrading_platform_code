class Screen():
    def setName(self):
        self.dict = {
            'Tr':'1000'
        }

    def getName(self, name):
        self.setName()
        return self.dict[name]
