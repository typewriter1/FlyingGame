"""
About .mission files:

They contain the locations model files should be loaded at and placed on the
terrain.bam model.

Note that .egg/.bam extensions can be ommited.
"""


class Item(object):
    def __init__(self, modelName, modelPos):
        self.modelName = modelName
        self.modelPos = modelPos

    def __repr__(self):
        return self.modelName + " at " + str(self.modelPos)

def parseMissionFile(filename):
    f = open(filename, "r")
    file = f.read()
    f.close()
    models = []  #model name: pos

    for line in file.split("\n"):  #go through each line
        lineContents = line.split(":")
        pos = lineContents[1].split(",")
        models.append(Item(modelName = lineContents[0], modelPos = (float(pos[0]), float(pos[1]), float(pos[2]))))

    return models

if __name__ == "__main__":
    print(str(parseMissionFile("models/m1.mission")))
