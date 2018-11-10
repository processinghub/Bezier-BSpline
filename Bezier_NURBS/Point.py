class Point:
    def __init__(self, position, label):
        self.position = position
        self.label = label
        self.radius = 10 if label == 'Anchor' else 7
    def __repr__(self):
        return "({0},{1},\"{2}\")".format(self.position.x, self.position.y, self.label)
    def GetPosition(self):
        return (int(self.position.x), int(self.position.y))
    def Display(self, colorfill):
        x, y = int(self.position.x), int(self.position.y)
        fill(180); textSize(10)
        text(str((x, y)), x, y - 8)
        fill(colorfill); 
        if self.label == 'Anchor':
            ellipseMode(CENTER); ellipse(x, y, self.radius, self.radius)
        else:
            rectMode(CENTER); rect(x, y, self.radius, self.radius)
        
