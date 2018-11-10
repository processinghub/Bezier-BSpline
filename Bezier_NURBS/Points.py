from Point import Point
import copy

class Points:
    def __init__(self):
        self.pointType = {
        'Anchor' : [] , # List of anchor points
        'CtrlIN' : [] , # List of control points
        'CtrlOUT' : []   # List of control points at an inverted position 
        }
        
    def GetPoint(self, name, index):
        return self.pointType[name][index]
    
    def AddPoint(self, position, label):
        if label == 'Anchor':
            self.pointType['Anchor'].append(Point(position, label))
            self.pointType['CtrlIN'].append(Point(position, label)) # The control point is right on the anchor point by Default
            self.pointType['CtrlOUT'].append(Point(self.GetOut(len(self.pointType['Anchor']) - 1), 'CtrlOUT'))
        elif label == 'CtrlIN' and self.pointType[label]:
            self.pointType['CtrlIN'].pop()
            self.pointType['CtrlOUT'].pop()
            self.pointType['CtrlIN'].append(Point(position, label))
            self.pointType['CtrlOUT'].append(Point(self.GetOut(len(self.pointType['Anchor']) - 1), 'CtrlOUT'))
            
    def RemoveLastPoint(self):
        if len(self.pointType['Anchor']) != len(self.pointType['CtrlIN']):
            # There should be as many control point pairs as anchor points
            raise Exception("Anchor({0}) != CtrlIN({1})".format(len(self.pointType['Anchor']), len(self.pointType['CtrlIN'])))
        elif self.pointType['Anchor'] and self.pointType['CtrlIN']: # Pop end if both lists aren't empty
            for keyword in self.pointType:
                self.pointType[keyword].pop()
        
    def GetOut(self, index):
        """
        Create a list of inversed control point
            x3 = x1 - (x2 - x1) = 2x1 - x2
            y3 = y1 - (y2 - y1) = 2y1 - y2
        """
        pAnchor = copy.deepcopy(self.GetPoint('Anchor', index).position)
        pCtrlIN = copy.deepcopy(self.GetPoint('CtrlIN', index).position)
        newPosi = PVector.sub(pAnchor.mult(2), pCtrlIN)
        return newPosi
            
    
    def ShowPointLists(self):
        def ShowList(pointType, name, x, y):
            string = str([ p.GetPosition() for p in pointType[name] ])
            textAlign(RIGHT); text(str(name) + " : ", x + 50, y)
            textAlign(LEFT); text(string[1:-1], x + 60, y)
        pushMatrix()
        yGap = 12
        textSize(10);fill(0);noStroke()
        ShowList(self.pointType, 'Anchor', 5, height - yGap * 3)
        ShowList(self.pointType, 'CtrlIN', 5, height - yGap * 2)
        ShowList(self.pointType, 'CtrlOUT', 5, height - yGap * 1)
        popMatrix()
        
        
    def ShowPoints(self, mode = 'Bezier'):
        """
        The display order must be ordered, but since the dict() type is a hashtable,
        there's gonna be some redundant coding. Yeah, OrderedDict is a good idea,
        but it's gonna take a huge revision of the whole program(I'm a lazy bottom)
        """
        def DisplayPoints(pointList, colorfill):
            for p in pointList: 
                if not p.label == 'Anchor':
                    # Link the control points to Anchor points
                    stroke(0, 100)
                    index = pointList.index(p)
                    pAnchor = self.pointType['Anchor'][pointList.index(p)]
                    if mode == 'Bezier': 
                        line(p.position.x, p.position.y, pAnchor.position.x, pAnchor.position.y)
                p.Display(colorfill)
                    
        pushMatrix()
        if mode == 'Bezier':
            DisplayPoints(self.pointType['CtrlOUT'], color(255, 240, 0))
            DisplayPoints(self.pointType['CtrlIN'], color(0, 0, 255))
        DisplayPoints(self.pointType['Anchor'], color(0))
        popMatrix()
        
    def ClickTest(self, x, y):
        """
        Returns the item been clicked, None if no such item
        """
        def ClickedItem(pointList, x, y):
            for p in pointList:
                if dist(p.position.x, p.position.y, x, y) <= p.radius + 1 :
                    return [p.label, pointList.index(p)]
            return None
        result_1 = ClickedItem(self.pointType['CtrlIN'], x, y)
        result_2 = ClickedItem(self.pointType['CtrlOUT'], x, y)
        result_3 = ClickedItem(self.pointType['Anchor'], x, y)
        if result_1 is not None:
            return result_1
        elif result_2 is not None:
            return result_2
        else:
            return result_3
    
    def UpdatePosition(self, p, x, y):
        if p[0] == 'Anchor':
            pAnchor = self.pointType['Anchor'][p[1]]
            displacement = PVector.sub(PVector(x,y), pAnchor.position)
            self.pointType['Anchor'][p[1]].position = PVector(x, y)
            self.pointType['CtrlIN'][p[1]].position.add(displacement)
            self.pointType['CtrlOUT'][p[1]].position.add(displacement)
        elif p[0] == 'CtrlIN':
            self.pointType['CtrlIN'][p[1]].position = PVector(x, y)
            self.pointType['CtrlOUT'][p[1]].position = self.GetOut(p[1])
        else:
            self.pointType['CtrlOUT'][p[1]].position = PVector(x, y)
        
    def ShowCurve(self, mode):
        import math
        listLength = len(self.pointType['Anchor'])
        def ShowCurveBetween(points):
            """
            P(t) = Sigma(P_i * B_(i,n)(t)) from i = 0 to n
            B_(i,n)(t) = C(n,i) * t^i * (1-t)^(n-i)
            """
            n = len(points)
            t = 0.0
            P_t = PVector(0,0)
            pP_t = None
            while t <= 1.02:
                P_t = Sigma(points, n, t)
                if pP_t != None:
                    line(P_t.x, P_t.y, pP_t.x, pP_t.y)
                pP_t = P_t
                t += 0.05
        def Sigma(points, n, t):
            result = PVector(0, 0)
            for i in range(n):
                temp = copy.deepcopy(points[i].position)
                temp.mult(B(i,n - 1,t))
                result.add(temp)
            return result
        def C(n, i):
            return math.factorial(n) / math.factorial(i) / math.factorial(n - i)
        def B(i,n,t):
            return C(n, i) * pow(t,i) * pow(1.0 - t, n - i)
        def ShowBezier():
            for i in range(listLength - 1):
                p1 = self.GetPoint('Anchor', i)
                p2 = self.GetPoint('CtrlIN', i)
                p3 = self.GetPoint('CtrlOUT', i + 1)
                p4 = self.GetPoint('Anchor', i + 1)
                ShowCurveBetween([p1,p2,p3,p4])
            
        def ShowBSpline():
            ShowCurveBetween([self.GetPoint('Anchor', i) for i in range(listLength)])

        if mode == 'Bezier':
            ShowBezier()
        else:
            ShowBSpline()        
        
        
        
        
        
        
        
        
        
        
        
