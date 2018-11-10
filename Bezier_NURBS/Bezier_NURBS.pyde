"""
Author: color·sky
Date  : 2018/11/10
Reference : https://mp.weixin.qq.com/s/kBZUqAsGnTCsIvJnJXsBCQ
Special Thanks: ElementMo, hi347
"""
from Points import Points
global mode; mode = 'Bezier'
global globalData, clickedItem
globalData = Points()
clickedItem = None

def setup():
    size(1000, 800)
    noCursor()

def draw():
    global globalData, clickedItem, mode
    background(255,240,240) if mode == 'Bezier' else background(240,240,255)
    DisplayCursor()
    textSize(height/20);textAlign(CENTER); fill(0); 
    if mode == 'Bezier':
        text(mode+'(n=3)', width/2, height/6)
    else: text(mode+'(n={0})'.format(len(globalData.pointType['Anchor'])), width/2, height/6)
    globalData.ShowPoints(mode)
    globalData.ShowCurve(mode)
    globalData.ShowPointLists()

def DisplayCursor():
    pushMatrix()
    fill(0);stroke(0)
    line(mouseX - 10, mouseY, mouseX + 10, mouseY);
    line(mouseX, mouseY - 10, mouseX, mouseY + 10);
    fill(255); ellipse(mouseX, mouseY, 5, 5);
    popMatrix()
    
def mousePressed():
    global globalData, clickedItem
    clickedItem = globalData.ClickTest(mouseX, mouseY)
    if clickedItem is None:
        globalData.AddPoint(PVector(mouseX, mouseY), "Anchor")
    
def mouseDragged():
    global globalData, clickedItem
    if clickedItem is not None:
        cursor(HAND)
        globalData.UpdatePosition(clickedItem, mouseX, mouseY)
    else: 
        globalData.AddPoint(PVector(mouseX, mouseY), "CtrlIN")

def mouseReleased():
    global clickedItem
    clickedItem = None
    noCursor()
    
def keyPressed():
    global globalData, mode
    if key == BACKSPACE or keyCode == 90:
        globalData.RemoveLastPoint()
    if key == ' ':
        mode = 'Bezier' if mode == 'B-Spline' else 'B-Spline'
        
        
        
        
        
