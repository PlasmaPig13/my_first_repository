##### TO ADD: indication of function when choosing to load
import pygame, math, random

def convRand(r):
    if r <= 1/highParamChance:
        out = highParamChance*r
    else:
        out = 1 - math.sqrt(highParamChance*randParamVar)/randParamVar - 1/(randParamVar*r-(randParamVar+math.sqrt(highParamChance*randParamVar))/highParamChance)
    
    if random.randint(1,2) == 2:
        out = -out
    
    return int(out*1000)/1000

def colourScale(col,a):
    return (col[0]*a,col[1]*a,col[2]*a)
    
def f(x,h):
    return h + math.sin(x) + math.sin(math.floor(abs(x)))

def display(accumulate,accTendCol=(255,255,255),fadeIntensity=0,basinBg=False):
    WIN.fill(bgCol)
    global renderedPointsL
    renderedPointsL = [0 for p in points]
    
    global pullScreen
    
    if basinBg:
        pullScreen = []
        for x in range(w):
            column = []
            for y in range(h):
                column.append([])
            pullScreen.append(column)
        
#        for i in range(numPoints):
#            currentL = pointLists[i]
#            for j in range(1,len(pointLists[i])):
#                P0 = currentL[j-1]
#                x = int((P0[0]-pos[0])*scale+w2)
#                if 0 <= x and x < w:
#                    y = int(h2-(P0[1]-pos[1])*sv)
#                    if 0 <= y and y < h:
#                        P1 = currentL[j]
#                        dist = math.sqrt((P0[0]-P1[0])**2+(P0[1]-P1[1])**2)*scale/400
#                        v = 1-1/(dist+1)
#                        pullScreen[x][y].append(colourScale(pCols[i],v))
        
#        for x0 in range(w):
#            X0 = (x0-w2)/scale+pos[0]
#            for y0 in range(h):
#                Y0 = (h2-y0)/sv+pos[1]
#                P0 = (X0,Y0)
#                for x1 in range(x0-1,x0+2):
#                    X1 = (x1-w2)/scale+pos[0]
#                    for y1 in range(y0-1,y0+2):
#                        Y1 = (h2-y1)/sv+pos[1]
#                        rawDist = math.sqrt((X0-X1)**2+(Y0-Y1)**2)
#                        P1 = (X1,Y1)
#                        n0 = f0(P0,P1)
#                        n1 = f1(P0,P1)
#                        cookedDist = math.sqrt((n0[0]-n1[0])**2+(n0[1]-n1[1])**2)
#                        diff = (cookedDist-rawDist)*scale
#                        v = 1-1/(abs(diff)+1)
#                        v1 = 1-v
#                        if diff < 0:
#                            v255 = 255*v
#                            pullScreen[x0][y0].append((int(v255+mbgCol[0]*v1),int(v255+mbgCol[1]*v1),int(v255+mbgCol[2]*v1)))
#                        else:
#                            pullScreen[x0][y0].append((int(mbgCol[0]*v1),int(mbgCol[1]*v1),int(mbgCol[2]*v1)))
        
        for x in range(w):
            for y in range(h):
                p = pullScreen[x][y]
                num = len(p)
                baseColour = (0,0,0)
                if num > 0:
                    for c in p:
                        baseColour = (baseColour[0]+c[0],baseColour[1]+c[1],baseColour[2]+c[2])
                    baseColour = (baseColour[0]//num,baseColour[1]//num,baseColour[2]//num)
                pygame.draw.rect(WIN,baseColour,(x,y,1,1))
    
    if not accumulate:
        for i in range(numPoints):
            if showPoints[i]:
                for p in pointLists[i]:
                    x = int((p[0]-pos[0])*scale+w2)
                    if 0 <= x and x < w:
                        y = int((pos[1]-p[1])*sv+h2)
                        if 0 <= y and y < h:
                            renderedPointsL[i] += 1
                            pygame.draw.rect(WIN,pCols[i],(x,y,1,1))
    
    if accumulate:
        screen = [[[] for y in range(h)] for x in range(w)]
        
        for i in range(numPoints):
            if showPoints[i]:
                for p in pointLists[i]:
                    x = int((p[0]-pos[0])*scale+w2)
                    if 0 <= x and x < w:
                        y = int((pos[1]-p[1])*sv+h2)
                        if 0 <= y and y < h:
                            screen[x][y].append(pCols[i])
        
        maxNum = 0
        for x in range(w):
            for y in range(h):
                if len(screen[x][y]) > maxNum:
                    maxNum = len(screen[x][y])
        
        for x in range(w):
            for y in range(h):
                p = screen[x][y]
                num = len(p)
                if num > 0:
                    baseColour = (0,0,0)
                    for c in p:
                        baseColour = (baseColour[0]+c[0],baseColour[1]+c[1],baseColour[2]+c[2])
                    baseColour = (baseColour[0]//num,baseColour[1]//num,baseColour[2]//num)
                    log = math.log(num*(1+fadeIntensity)-fadeIntensity)/math.log(maxNum*(1+fadeIntensity)+fadeIntensity)
                    AcCol = (int(log*accTendCol[0]+(1-log)*baseColour[0]),int(log*accTendCol[1]+(1-log)*baseColour[1]),int(log*accTendCol[2]+(1-log)*baseColour[2]))
                else:
                    AcCol = bgCol
                pygame.draw.rect(WIN,AcCol,(x,y,1,1))
    
    if zoomIn:
        pygame.draw.rect(WIN,txCol,(w120,h120,100,100))
        pygame.draw.rect(WIN,bgCol,(w-80,h-110,20,80))
        pygame.draw.rect(WIN,bgCol,(w-110,h-80,80,20))
    if zoomOut:
        pygame.draw.rect(WIN,txCol,(w240,h120,100,100))
        pygame.draw.rect(WIN,bgCol,(w-230,h-80,80,20))
    
    if squash:
        pygame.draw.rect(WIN,txCol,(20,h120,100,100))
        pygame.draw.polygon(WIN,bgCol,[(20+point[0],h120+point[1]) for point in [(50,70),(30,90),(25,85),(42.5,67.5),(42.5,32.5),(25,15),(30,10),(50,30),(70,10),(75,15),(57.5,32.5),(57.5,67.5),(75,85),(70,90)]])
    if stretch:
        pygame.draw.rect(WIN,txCol,(20,h240,100,100))
        pygame.draw.polygon(WIN,bgCol,[(20+point[0],h240+point[1]) for point in [(50,90),(25,65),(30,60),(42.5,72.5),(42.5,27.5),(30,40),(25,35),(50,10),(75,35),(70,40),(57.5,27.5),(57.5,72.5),(70,60),(75,65)]])
    
    if toggleCalc:
        pygame.draw.rect(WIN,txCol,(w120//2-50,h-275,100,100))
        if calc:
            pygame.draw.rect(WIN,bgCol,(w120//2-30,h-265,20,80))
            pygame.draw.rect(WIN,bgCol,(w120//2+10,h-265,20,80))
        else:
            pygame.draw.polygon(WIN,bgCol,[(w120//2-30,h-265),(w120//2-30,h-185),(w120//2+40,h-225)])
    
    if toggleTamper:
        pygame.draw.rect(WIN,(ltCol if recentre else dtCol),(w120//2+70,h-275,100,100))
    
    if skippable:
        pygame.draw.rect(WIN,txCol,(w120//2-170,h-275,100,100))
        pygame.draw.polygon(WIN,bgCol,[(point[0]+w120//2-170,point[1]+h-275) for point in [(20,90),(55,50),(55,90),(90,50),(55,10),(55,50),(20,10)]])
    
    if not hide:
        if bgCol[0]+bgCol[1]+bgCol[2]-382.5 < 0:
            hCol = (bgCol[0]*0.95+255*0.1,bgCol[1]*0.95+255*0.1,bgCol[2]*0.95+255*0.1)
        else:
            hCol = (bgCol[0]*0.95,bgCol[1]*0.95,bgCol[2]*0.95)
        pygame.draw.rect(WIN,hCol,(w120,20,100,100))
    
    if reset:
        pygame.draw.rect(WIN,txCol,(w240,20,100,100))
        resetText0 = smallFont.render("Reset",False,bgCol)
        resetSize0 = smallFont.size("Reset")
        resetText1 = smallFont.render("View",False,bgCol)
        resetSize1 = smallFont.size("View")
        WIN.blit(resetText0,(w240+50-resetSize0[0]//2,70-resetSize0[1]))
        WIN.blit(resetText1,(w240+50-resetSize1[0]//2,70))
    
    zoomText = font.render(str(round(scale*100)/100),False,txCol)
    zoomSize = font.size(str(round(scale*100)/100))
    if zoomIn or zoomOut:
        WIN.blit(zoomText,(w-zoomSize[0]//2-130,h-130-zoomSize[1]))
    
    if toggles:
        pygame.draw.rect(WIN,txCol,(w120,h240-zoomSize[1],100,100))
        pygame.draw.rect(WIN,(pCols[selectedToggle] if showPoints[selectedToggle] else (pCols[selectedToggle][0]//2,pCols[selectedToggle][1]//2,pCols[selectedToggle][2]//2)),(w240,h240-zoomSize[1],100,100))
        cycleToggles0Text = smallFont.render("Cycle",False,bgCol)
        cycleToggles0Size = smallFont.size("Cycle")
        cycleToggles1Text = smallFont.render("Toggles",False,bgCol)
        cycleToggles1Size = smallFont.size("Toggles")
        WIN.blit(cycleToggles0Text,(w120+50-cycleToggles0Size[0]//2,h240-zoomSize[1]+50-cycleToggles0Size[1]))
        WIN.blit(cycleToggles1Text,(w120+50-cycleToggles1Size[0]//2,h240-zoomSize[1]+50))
    
    if renderable:
        pygame.draw.rect(WIN,txCol,(w120,140,100,100))
        pygame.draw.rect(WIN,bgCol,(w120+20,140+30,10,10))
        pygame.draw.rect(WIN,bgCol,(w120+30,140+70,10,10))
        pygame.draw.rect(WIN,bgCol,(w120+60,140+20,10,10))
        pygame.draw.rect(WIN,bgCol,(w120+70,140+60,10,10))
        pygame.draw.rect(WIN,bgCol,(w120+45,140+45,10,10))
    
    if toggleAcc:
        pygame.draw.rect(WIN,txCol,(w120,260,100,100))
        pygame.draw.rect(WIN,pCols[0],(w120+20,280,30,60))
        if numPoints < 2:
            pygame.draw.rect(WIN,pCols[0],(w120+50,280,30,60))
        else:
            pygame.draw.rect(WIN,pCols[1],(w120+50,280,30,60))
        if accumulatePending:
            pygame.draw.rect(WIN,ftCol,(w120+35,295,30,30))
    
    if togglePull:
        pygame.draw.rect(WIN,txCol,(w120,380,100,100))
        if pullPending:
            pygame.draw.rect(WIN,bgCol,(w120+35,415,30,30))
    
    stretchText = font.render(str(round(vstretch*100)/100),False,txCol)
    stretchSize = font.size(str(round(vstretch*100)/100))
    if squash or stretch:
        WIN.blit(stretchText,(65-stretchSize[0]//2,h-stretchSize[1]-250))
    
    if Lcalcs > 0 and showLyapunov:
        lyapunovs = [l/Lcalcs for l in lyapunovList]
        meanLyapunov = sum(lyapunovs[:numPoints-1])/numPoints
        
        meanLyapunovstr = str(meanLyapunov)
        meanLyapunovText = font.render(meanLyapunovstr,False,txCol)
        meanLyapunovSize = font.size(meanLyapunovstr)
        WIN.blit(meanLyapunovText,(w120//2-meanLyapunovSize[0]//2,h-50))
    
    if shuffleParams:
        pygame.draw.rect(WIN,txCol,(20,20,100,100))
        shuffleParams0Text = smallFont.render("Shuffle",False,bgCol)
        shuffleParams0Size = smallFont.size("Shuffle")
        shuffleParams1Text = smallFont.render("Params",False,bgCol)
        shuffleParams1Size = smallFont.size("Params")
        WIN.blit(shuffleParams0Text,(70-shuffleParams0Size[0]//2,70-shuffleParams0Size[1]))
        WIN.blit(shuffleParams1Text,(70-shuffleParams1Size[0]//2,70))
    
    if changeIncrement:
        global incrementSize
        incrementstr = "Increment = " + str(10**increment)
        incrementText = font.render(incrementstr,False,txCol)
        incrementSize = font.size(incrementstr)
        incy = min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0
        WIN.blit(incrementText,(20,170+incy))
        pygame.draw.rect(WIN,txCol,(30+incrementSize[0],145+incrementSize[1]//2+incy,50,50))
        pygame.draw.rect(WIN,bgCol,(35+incrementSize[0],165+incrementSize[1]//2+incy,40,10))
        pygame.draw.rect(WIN,txCol,(90+incrementSize[0],145+incrementSize[1]//2+incy,50,50))
        pygame.draw.rect(WIN,bgCol,(95+incrementSize[0],165+incrementSize[1]//2+incy,40,10))
        pygame.draw.rect(WIN,bgCol,(110+incrementSize[0],150+incrementSize[1]//2+incy,10,40))
    
    allPointsstr = str(numPoints*len(pointLists[0]))
    allPointsText = font.render(allPointsstr,False,txCol)
    allPointsSize = font.size(allPointsstr)
    if pointCount:
        WIN.blit(allPointsText,(w120//2-allPointsSize[0]//2,h-2*allPointsSize[1]-40))
    
    renderedPointsstr = str(sum(renderedPointsL))
    renderedPointsText = font.render(renderedPointsstr,False,txCol)
    renderedPointsSize = font.size(renderedPointsstr)
    if pointCount:
        WIN.blit(renderedPointsText,(w120//2-renderedPointsSize[0]//2,h-3*renderedPointsSize[1]-40))
    
    if toggleParams:
        pygame.draw.rect(WIN,txCol,(140,20,100,100))
        toggleParams0Text = smallFont.render("Toggle",False,bgCol)
        toggleParams0Size = smallFont.size("Toggle")
        toggleParams1Text = smallFont.render("Params",False,bgCol)
        toggleParams1Size = smallFont.size("Params")
        WIN.blit(toggleParams0Text,(190-toggleParams0Size[0]//2,70-toggleParams0Size[1]))
        WIN.blit(toggleParams1Text,(190-toggleParams1Size[0]//2,70))
    
    if save:
        pygame.draw.rect(WIN,txCol,(260,20,100,100))
        saveText = smallFont.render("Save",False,bgCol)
        saveSize = smallFont.size("Save")
        WIN.blit(saveText,(310-saveSize[0]//2,70-saveSize[1]//2))
    
    if load:
        pygame.draw.rect(WIN,txCol,(380,20,100,100))
        loadText = smallFont.render("Load",False,bgCol)
        loadSize = smallFont.size("Load")
        WIN.blit(loadText,(430-loadSize[0]//2,70-loadSize[1]//2))
    
    if loadList:
        for option in range(len(loadFrom)):
            loadNumText = font.render(str(option),False,txCol)
            loadNumSize = font.size(str(option))
            if 132 <= 132+option*60+loadScrolledTo < 82+min(len(loadFrom),20)*60:
                WIN.blit(loadNumText,(380,140+option*60+loadScrolledTo))
    
    global maxParamSize
    if paramInfo:
        maxParamSize = 0
        for param in range(len(params)):
            paramstr = str(list(params.keys())[param]) + " = " + str(params[list(params.keys())[param]])
            paramText = font.render(paramstr,False,txCol)
            paramSize = font.size(paramstr)
            if paramSize[0] > maxParamSize:
                maxParamSize = paramSize[0]
            if 132 <= 132+param*60+paramScrolledTo < 82+min(len(params),paramScrollSize)*60:
                WIN.blit(paramText,(20,140+param*60+paramScrolledTo))
        
    if stepping:
        for param in range(len(params)):
            if 132 <= 132+param*60+paramScrolledTo < 82+min(len(params),paramScrollSize)*60:
                pygame.draw.rect(WIN,txCol,(30+maxParamSize,132+param*60+paramScrolledTo,50,50))
                pygame.draw.rect(WIN,txCol,(90+maxParamSize,132+param*60+paramScrolledTo,50,50))
                
                pygame.draw.rect(WIN,bgCol,(35+maxParamSize,152+param*60+paramScrolledTo,40,10))
                pygame.draw.rect(WIN,bgCol,(95+maxParamSize,152+param*60+paramScrolledTo,40,10))
                pygame.draw.rect(WIN,bgCol,(110+maxParamSize,137+param*60+paramScrolledTo,10,40))
    
    global funcSize
    funcstr = "Func = " + str(func)
    funcText = font.render(funcstr,False,txCol)
    funcSize = font.size(funcstr)
    if funcInfo:
        funcy = (min(len(params),paramScrollSize))*60 if paramInfo or stepping else 0
        WIN.blit(funcText,(20,230+funcy))
        if func > 0:
            pygame.draw.rect(WIN,txCol,(30+funcSize[0],205+funcSize[1]//2+funcy,50,50))
            pygame.draw.rect(WIN,bgCol,(35+funcSize[0],225+funcSize[1]//2+funcy,40,10))
        if func < len(funcNumPoints)-1:
            pygame.draw.rect(WIN,txCol,(90+funcSize[0],205+funcSize[1]//2+funcy,50,50))
            pygame.draw.rect(WIN,bgCol,(95+funcSize[0],225+funcSize[1]//2+funcy,40,10))
            pygame.draw.rect(WIN,bgCol,(110+funcSize[0],210+funcSize[1]//2+funcy,10,40))
    
    numPointsstr = "Num points = " + str(numPoints)
    numPointsText = font.render(numPointsstr,False,txCol)
    numPointsSize = font.size(numPointsstr)
    if numPointsInfo:
        WIN.blit(numPointsText,(20,290+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0)))
    
    centredstr = "Centered at " + str(pos)
    centredText = font.render(centredstr,False,txCol)
    centredSize = font.size(centredstr)
    if centreInfo:
        WIN.blit(centredText,(20,350+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0)))
    
    #WIN.blit(font.render(str(h),False,txCol),(w2,h2))
    
    if toggleInfo[0] and toggleInfo[1] and toggleInfo[2]:
        for i in range(len(toggleInfo)):
            pygame.draw.rect(WIN,txCol,(20,450+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0)+i*95,75,75))
    
    elif True in toggleInfo:
        pygame.draw.rect(WIN,txCol,(20,450+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0),75,75))
        pygame.draw.polygon(WIN,bgCol,[(p[0]*7.5+20,p[1]*7.5+450+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0)) for p in [(1,3),(3,5),(1,7),(3,9),(5,7),(7,9),(9,7),(7,5),(9,3),(7,1),(5,3),(3,1)]])
        for i in range(len(toggleInfo)):
            if toggleInfo[i]:
                if i == 0:
                    WIN.blit(font.render("Calculated points:",False,txCol),(20,545+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0)))
                    pointsPerstr = str(len(pointLists[0]))
                    pointsPerTexts = []
                    pointsPerSizes = []
                    for p in range(numPoints):
                        pointsPerTexts.append(font.render(pointsPerstr,False,pCols[p]))
                        pointsPerSizes.append(font.size(pointsPerstr))
                        WIN.blit(pointsPerTexts[p],(20,545+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0)+(p+1)*60))
                if i == 1:
                    WIN.blit(font.render("Rendered points:",False,txCol),(20,545+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0)))
                    renderedPointsstrs = []
                    renderedPointsTexts = []
                    renderedPointsSizes = []
                    for p in range(numPoints):
                        renderedPointsstrs.append(str(renderedPointsL[p]))
                        renderedPointsTexts.append(font.render(renderedPointsstrs[p],False,pCols[p]))
                        renderedPointsSizes.append(font.size(renderedPointsstrs[p]))
                        WIN.blit(renderedPointsTexts[p],(20,545+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0)+(p+1)*60))
                if i == 2:
                    WIN.blit(font.render("Point Positions:",False,txCol),(20,545+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0)))
                    pointPositionstrs = []
                    pointPositionTexts = []
                    pointPositionSizes = []
                    for p in range(numPoints):
                        pointPositionstrs.append(str(points[p]))
                        pointPositionTexts.append(font.render(pointPositionstrs[p],False,pCols[p]))
                        pointPositionSizes.append(font.size(pointPositionstrs[p]))
                        WIN.blit(pointPositionTexts[p],(20,545+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0)+(p+1)*60))
    
    pygame.display.update()

def f0(points):
    if func == 0:
        return (math.sin(params["m0"]*points[0][1])+points[1][0]*math.cos(params["m0"]*points[0][0]),
                math.sin(params["m1"]*points[0][0])+points[1][1]*math.cos(params["m1"]*points[0][1]))
    elif func == 1:
        numPoints = 2
        return (math.sin(params["m0"]*points[0][0])+points[1][0]*math.sin(params["m1"]*points[0][1]),
                math.sin(params["m0"]*points[0][1])+points[1][1]*math.sin(params["m1"]*points[0][1]))
    elif func == 2:
        numPoints = 2
        return (math.sin(params["m0"]*points[0][0])+points[1][0]*math.sin(params["m1"]*points[0][1])+params["m2"],
                math.sin(params["m0"]*points[0][1])+points[1][1]*math.sin(params["m1"]*points[0][1])+params["m2"])
    elif func == 3:
        numPoints = 2
        return (abs(abs(points[1][0])-params["m0"])/(abs(points[0][0]**2-points[0][1])+params["m1"]),
                abs(abs(points[1][1])-params["m0"])/(abs(points[0][1]**2-points[0][0])+params["m1"]))
    elif func == 4:
        numPoints = 2
        return (math.sin(params["m0"]*points[0][0])+points[1][0]*math.sin(params["m1"]*points[0][1])+params["m2"],
                math.sin(params["m0"]*points[0][1])+points[1][1]*math.sin(params["m1"]*points[0][0])+params["m2"])
    elif func == 5:
        numPoints = 3
        return (math.sin(params["m0"]*points[0][0])+points[1][0]*math.sin(params["m1"]*points[2][1])+params["m2"],
                math.sin(params["m0"]*points[0][1])+points[1][1]*math.sin(params["m1"]*points[2][0])+params["m2"])
    elif func == 6:
        numPoints = 3
        return (math.sin(params["m0"]*points[0][0])+points[1][0]*math.sin(params["m1"]*points[2][1])+params["m2"],
                math.sin(params["m3"]*points[0][1])+points[1][1]*math.sin(params["m4"]*points[2][0])+params["m5"])
    elif func == 7:
        numPoints = 1
        return (abs(points[0][0])**(params["m0"]-math.floor(params["m0"]*math.log(abs(points[0][0])))/math.log(abs(points[0][0])))-params["m1"]*points[0][1],
                abs(points[0][1])**(params["m0"]-math.floor(params["m0"]*math.log(abs(points[0][1])))/math.log(abs(points[0][1])))-params["m2"]*points[0][0])
    elif func == 8:
        return ((params["m0"]*points[0][0] + params["m1"]*points[0][1] + params["m2"]*points[1][0] + params["m3"]*points[1][1] + params["m4"]*points[2][0] + params["m5"]*points[2][1] + params["m6"])*math.sin(params["m7"]*points[0][0] + params["m8"]*points[0][1] + params["m9"]*points[1][0] + params["m10"]*points[1][1] + params["m11"]*points[2][0] + params["m12"]*points[2][1] + params["m13"]),
                (params["m14"]*points[0][0] + params["m15"]*points[0][1] + params["m16"]*points[1][0] + params["m17"]*points[1][1] + params["m18"]*points[2][0] + params["m19"]*points[2][1] + params["m20"])*math.sin(params["m21"]*points[0][0] + params["m22"]*points[0][1] + params["m23"]*points[1][0] + params["m24"]*points[1][1] + params["m25"]*points[2][0] + params["m26"]*points[2][1] + params["m27"]))
    elif func == 9:
        return (params["m0"]*math.sin(params["m1"]*points[0][0] + params["m2"]*points[0][1] + params["m3"]*points[1][0] + params["m4"]*points[1][1] + params["m5"]*points[2][0] + params["m6"]*points[2][1] + params["m7"])+params["m8"]*math.cos(params["m9"]*points[0][0] + params["m10"]*points[0][1] + params["m11"]*points[1][0] + params["m12"]*points[1][1] + params["m13"]*points[2][0] + params["m14"]*points[2][1] + params["m15"]),
                params["m16"]*math.sin(params["m17"]*points[0][0] + params["m18"]*points[0][1] + params["m19"]*points[1][0] + params["m20"]*points[1][1] + params["m21"]*points[2][0] + params["m22"]*points[2][1] + params["m23"])+params["m24"]*math.cos(params["m25"]*points[0][0] + params["m26"]*points[0][1] + params["m27"]*points[1][0] + params["m28"]*points[1][1] + params["m29"]*points[2][0] + params["m30"]*points[2][1] + params["m31"]))
    elif func == 10:
        return (params["m0"]*f(points[0][0],params["m1"])+params["m2"]*f(points[0][1],params["m3"])+params["m4"]*f(points[1][0],params["m5"])+params["m6"]*f(points[1][1],params["m7"])+params["m8"]*f(points[2][0],params["m9"])+params["m10"]*f(points[2][1],params["m11"]),
                params["m12"]*f(points[0][0],params["m13"])+params["m14"]*f(points[0][1],params["m15"])+params["m16"]*f(points[1][0],params["m17"])+params["m18"]*f(points[1][1],params["m19"])+params["m20"]*f(points[2][0],params["m21"])+params["m22"]*f(points[2][1],params["m23"]))
    elif func == 11:
        return ((params["m0"]*points[0][0] + params["m1"]*points[0][1] + params["m2"]*points[1][0] + params["m3"]*points[1][1] + params["m4"]*points[2][0] + params["m5"]*points[2][1] + params["m6"])*math.sin(params["m7"]*points[0][0] + params["m8"]*points[0][1] + params["m9"]*points[1][0] + params["m10"]*points[1][1] + params["m11"]*points[2][0] + params["m12"]*points[2][1] + params["m13"]),
                (params["m14"]*points[0][0] + params["m15"]*points[0][1] + params["m16"]*points[1][0] + params["m17"]*points[1][1] + params["m18"]*points[2][0] + params["m19"]*points[2][1] + params["m20"])*math.sin(params["m21"]*points[0][0] + params["m22"]*points[0][1] + params["m23"]*points[1][0] + params["m24"]*points[1][1] + params["m25"]*points[2][0] + params["m26"]*points[2][1] + params["m27"]))
    #elif func = 
    else:
        return points[0]

def f1(points):
    if func == 0:
        return (math.sin(params["m0"]*points[1][1])+points[0][0]*math.cos(params["m0"]*points[1][0]),
                math.sin(params["m1"]*points[1][0])+points[0][1]*math.cos(params["m1"]*points[1][1]))
    elif func == 1:
        return (math.sin(params["m0"]*points[1][0])+points[0][0]*math.sin(params["m1"]*points[1][1]),
                math.sin(params["m0"]*points[1][1])+points[0][1]*math.sin(params["m1"]*points[1][0]))
    elif func == 2:
        return (math.sin(params["m0"]*points[1][0])+points[0][0]*math.sin(params["m1"]*points[1][1])+params["m2"],
                math.sin(params["m0"]*points[1][1])+points[0][1]*math.sin(params["m1"]*points[1][0])+params["m2"])
    elif func == 3:
        return (abs(abs(points[0][0])-params["m0"])/(abs(points[1][0]**2-points[1][1])+params["m1"]),
                abs(abs(points[0][1])-params["m0"])/(abs(points[1][1]**2-points[1][0])+params["m1"]))
    elif func == 4:
        return (abs(abs(points[0][0])-params["m0"])/(abs(points[1][0]**2-points[1][1])+params["m1"]),
                abs(abs(points[0][1])-params["m0"])/(abs(points[1][1]**2-points[1][0])+params["m1"]))
    elif func == 5:
        return (abs(abs(points[0][0])-params["m0"])/(abs(points[1][0]**2-points[2][1])+params["m1"]),
                abs(abs(points[0][1])-params["m0"])/(abs(points[1][1]**2-points[2][0])+params["m1"]))
    elif func == 6:
        return (abs(abs(points[0][0])-params["m6"])/(abs(points[1][0]**2-points[2][1])+params["m7"]),
                abs(abs(points[0][1])-params["m8"])/(abs(points[1][1]**2-points[2][0])+params["m9"]))
    elif func == 8:
        return ((params["m28"]*points[0][0] + params["m29"]*points[0][1] + params["m30"]*points[1][0] + params["m31"]*points[1][1] + params["m32"]*points[2][0] + params["m33"]*points[2][1] + params["m34"])*math.sin(params["m35"]*points[0][0] + params["m36"]*points[0][1] + params["m37"]*points[1][0] + params["m38"]*points[1][1] + params["m39"]*points[2][0] + params["m40"]*points[2][1] + params["m41"]),
                (params["m42"]*points[0][0] + params["m43"]*points[0][1] + params["m44"]*points[1][0] + params["m45"]*points[1][1] + params["m46"]*points[2][0] + params["m47"]*points[2][1] + params["m48"])*math.sin(params["m49"]*points[0][0] + params["m50"]*points[0][1] + params["m51"]*points[1][0] + params["m52"]*points[1][1] + params["m53"]*points[2][0] + params["m54"]*points[2][1] + params["m55"]))
    elif func == 9:
        return (params["m32"]*math.sin(params["m33"]*points[0][0] + params["m34"]*points[0][1] + params["m35"]*points[1][0] + params["m36"]*points[1][1] + params["m37"]*points[2][0] + params["m38"]*points[2][1] + params["m39"])+params["m40"]*math.cos(params["m41"]*points[0][0] + params["m42"]*points[0][1] + params["m43"]*points[1][0] + params["m44"]*points[1][1] + params["m45"]*points[2][0] + params["m46"]*points[2][1] + params["m47"]),
                params["m48"]*math.sin(params["m49"]*points[0][0] + params["m50"]*points[0][1] + params["m51"]*points[1][0] + params["m52"]*points[1][1] + params["m53"]*points[2][0] + params["m54"]*points[2][1] + params["m55"])+params["m56"]*math.cos(params["m57"]*points[0][0] + params["m58"]*points[0][1] + params["m59"]*points[1][0] + params["m60"]*points[1][1] + params["m61"]*points[2][0] + params["m62"]*points[2][1] + params["m63"]))
    elif func == 10:
        return (params["m24"]*f(points[0][0],params["m25"])+params["m26"]*f(points[0][1],params["m27"])+params["m28"]*f(points[1][0],params["m29"])+params["m30"]*f(points[1][1],params["m31"])+params["m32"]*f(points[2][0],params["m33"])+params["m34"]*f(points[2][1],params["m35"]),
                params["m36"]*f(points[0][0],params["m37"])+params["m38"]*f(points[0][1],params["m39"])+params["m40"]*f(points[1][0],params["m41"])+params["m42"]*f(points[1][1],params["m43"])+params["m44"]*f(points[2][0],params["m45"])+params["m46"]*f(points[2][1],params["m47"]))
    elif func == 11:
        return (params["m28"]*math.sin(params["m29"]*points[0][0] + params["m30"]*points[0][1] + params["m31"]*points[1][0] + params["m32"]*points[1][1] + params["m33"]*points[2][0] + params["m34"]*points[2][1] + params["m35"])+params["m36"]*math.cos(params["m37"]*points[0][0] + params["m38"]*points[0][1] + params["m39"]*points[1][0] + params["m40"]*points[1][1] + params["m41"]*points[2][0] + params["m42"]*points[2][1] + params["m43"]),
                params["m44"]*math.sin(params["m45"]*points[0][0] + params["m46"]*points[0][1] + params["m47"]*points[1][0] + params["m48"]*points[1][1] + params["m49"]*points[2][0] + params["m50"]*points[2][1] + params["m51"])+params["m52"]*math.cos(params["m53"]*points[0][0] + params["m54"]*points[0][1] + params["m55"]*points[1][0] + params["m56"]*points[1][1] + params["m57"]*points[2][0] + params["m58"]*points[2][1] + params["m59"]))
    else:
        return points[1]

def f2(points):
    if func == 5:
        return ((params["m0"]*abs(math.sin(params["m1"]*points[0][0]))-params["m3"]*points[1][1]**2+params["m2"])/(points[2][0]**2+1),
                (params["m0"]*abs(math.sin(params["m1"]*points[0][1]))-params["m3"]*points[1][0]**2+params["m2"])/(points[2][1]**2+1))
    if func == 6:
        return ((params["m10"]*abs(math.sin(params["m11"]*points[0][0]))-params["m12"]*points[1][1]**2+params["m13"])/(points[2][0]**2+params["m14"]),
                (params["m15"]*abs(math.sin(params["m16"]*points[0][1]))-params["m17"]*points[1][0]**2+params["m18"])/(points[2][1]**2+params["m19"]))
    elif func == 8:
        return ((params["m56"]*points[0][0] + params["m57"]*points[0][1] + params["m58"]*points[1][0] + params["m59"]*points[1][1] + params["m60"]*points[2][0] + params["m61"]*points[2][1] + params["m62"])*math.sin(params["m63"]*points[0][0] + params["m64"]*points[0][1] + params["m65"]*points[1][0] + params["m66"]*points[1][1] + params["m67"]*points[2][0] + params["m68"]*points[2][1] + params["m69"]),
                (params["m70"]*points[0][0] + params["m71"]*points[0][1] + params["m72"]*points[1][0] + params["m73"]*points[1][1] + params["m74"]*points[2][0] + params["m75"]*points[2][1] + params["m76"])*math.sin(params["m77"]*points[0][0] + params["m78"]*points[0][1] + params["m79"]*points[1][0] + params["m80"]*points[1][1] + params["m81"]*points[2][0] + params["m82"]*points[2][1] + params["m83"]))
    elif func == 9:
        return (params["m64"]*math.sin(params["m65"]*points[0][0] + params["m66"]*points[0][1] + params["m67"]*points[1][0] + params["m68"]*points[1][1] + params["m69"]*points[2][0] + params["m70"]*points[2][1] + params["m71"])+params["m72"]*math.cos(params["m73"]*points[0][0] + params["m74"]*points[0][1] + params["m75"]*points[1][0] + params["m76"]*points[1][1] + params["m77"]*points[2][0] + params["m78"]*points[2][1] + params["m79"]),
                params["m80"]*math.sin(params["m81"]*points[0][0] + params["m82"]*points[0][1] + params["m83"]*points[1][0] + params["m84"]*points[1][1] + params["m85"]*points[2][0] + params["m86"]*points[2][1] + params["m87"])+params["m88"]*math.cos(params["m89"]*points[0][0] + params["m90"]*points[0][1] + params["m91"]*points[1][0] + params["m92"]*points[1][1] + params["m93"]*points[2][0] + params["m94"]*points[2][1] + params["m95"]))
    elif func == 10:
        return (params["m48"]*f(points[0][0],params["m49"])+params["m50"]*f(points[0][1],params["m51"])+params["m52"]*f(points[1][0],params["m53"])+params["m54"]*f(points[1][1],params["m55"])+params["m56"]*f(points[2][0],params["m57"])+params["m58"]*f(points[2][1],params["m59"]),
                params["m60"]*f(points[0][0],params["m61"])+params["m62"]*f(points[0][1],params["m63"])+params["m64"]*f(points[1][0],params["m65"])+params["m66"]*f(points[1][1],params["m67"])+params["m68"]*f(points[2][0],params["m69"])+params["m70"]*f(points[2][1],params["m71"]))
    elif func == 11:
        return (params["m60"]*f(points[0][0],params["m61"])+params["m62"]*f(points[0][1],params["m63"])+params["m64"]*f(points[1][0],params["m65"])+params["m66"]*f(points[1][1],params["m67"])+params["m68"]*f(points[2][0],params["m69"])+params["m70"]*f(points[2][1],params["m71"]),
                params["m72"]*f(points[0][0],params["m73"])+params["m74"]*f(points[0][1],params["m75"])+params["m76"]*f(points[1][0],params["m77"])+params["m78"]*f(points[1][1],params["m79"])+params["m80"]*f(points[2][0],params["m81"])+params["m82"]*f(points[2][1],params["m83"]))
    else:
        return points[2]

funcList = [f0,f1,f2]
funcNumPoints = [2,2,2,2,2,3, 3,1, 3, 3, 3, 3]
funcNumParams = [2,2,3,2,3,4,20,3,84,96,72,84]

def hideAll():
    global zoomOut
    global zoomIn
    global toggles
    global squash
    global stretch
    global skippable
    global toggleCalc
    global toggleTamper
    global stepping
    global pointCount
    global currentPoints
    global paramInfo
    global changeIncrement
    global funcInfo
    global funcButtons
    global numPointsInfo
    global centreInfo
    global recentre
    global renderable
    global toggleAcc
    global togglePull
    global toggleInfo
    global toggleParams
    global shuffleParams
    global showLyapunov
    global save
    global load
    global reset
    global hide
    
    if hide:
        zoomOut = True
        zoomIn = True
        toggles = True
        squash = True
        stretch = True
        skippable = True
        toggleCalc = True
        toggleTamper = True
        pointCount = True
        currentPoints = True
        changeIncrement = True
        funcInfo = True
        funcButtons = True
        numPointsInfo = True
        centreInfo = True
        recentre = True
        renderable = True
        toggleAcc = True
        togglePull = True
        toggleInfo = [True for b in toggleInfo]
        toggleParams = True
        shuffleParams = True
        showLyapunov = True
        save = True
        load = True
        reset = True
    else:
        zoomOut = False
        zoomIn = False
        toggles = False
        squash = False
        stretch = False
        skippable = False
        toggleCalc = False
        toggleTamper = False
        stepping = False
        pointCount = False
        currentPoints = False
        paramInfo = False
        changeIncrement = False
        funcInfo = False
        funcButtons = False
        numPointsInfo = False
        centreInfo = False
        recentre = False
        renderable = False
        toggleAcc = False
        togglePull = False
        toggleInfo = [False for b in toggleInfo]
        toggleParams = False
        shuffleParams = False
        showLyapunov = False
        save = False
        load = False
        loadList = False
        reset = False
    
    hide = not hide

scale = 100

vstretch = 1

sv = scale*vstretch

pointsPerFrame = 2000

preferredNumPoints = 400000

initialNumPoints = 20000

leeway = 3000

eta = 0.0001

increment = -3

highParamChance = 1.1

func = 7

numPoints = funcNumPoints[func]

paramsFunc4ScannedTo = {"m0": 2
                       ,"m1": -0.4
                       ,"m2": 0
                       }

params = {"m0":6
         ,"m1":-1
         ,"m2":-2}

lenparams = len(params)
if lenparams < funcNumParams[func]:
    paramstoadd = funcNumParams[func]-lenparams
    for i in range(paramstoadd):
        params["m"+str(lenparams+i)] = 1

colPreset = "test"

pygame.init()
pygame.font.init()
WIN = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
w = pygame.display.Info().current_w
h = pygame.display.Info().current_h
w2 = w//2
h2 = h//2
h120 = h-120
w120 = w-120
h240 = h-240
w240 = w-240
font = pygame.font.SysFont("couriernew",30)
smallFont = pygame.font.SysFont("couriernew",20)

points = [(0.1,1.05),(1,0.1),(0.9,0.95)]
startingpoints = [p for p in points]
pointsNew = ["" for p in points]

pointLists = [[] for p in points]
lyapunovList = [0 for p in points]

pos = (0,0)

pCols = [(255,115,105),(74,152,120),(105,74,255)]
bgCol = (213,224,254)
ftCol = (0,0,0)

if colPreset == "Aar":
    pCols[0] = (203,89,75)
    pCols[1] = (219,179,195)
    bgCol = (23,10,21)
    ftCol = (255,255,255)

if colPreset == "Emax0":
    pCols[0] = (255,162,56)
    pCols[1] = (255,60,56)
    bgCol = (0,0,0)
    ftCol = (255,116,0)
    
if colPreset == "test":
    pCols[0] = (255,0,116)
    pCols[1] = (255,74,255)
    bgCol = (23,10,21)
    ftCol = (255,255,0)
    

txCol = (0,0,0)
for pCol in pCols[:numPoints]:
    txCol = (txCol[0]+pCol[0],txCol[1]+pCol[1],txCol[2]+pCol[2])
txCol = (txCol[0]//numPoints,txCol[1]//numPoints,txCol[2]//numPoints)

lightScale = 3*195/(txCol[0]+txCol[1]+txCol[2])
ltCol = (min(255,int(lightScale*txCol[0])),min(255,int(lightScale*txCol[1])),min(255,int(lightScale*txCol[2])))
darkScale = 3*60/(txCol[0]+txCol[1]+txCol[2])
dtCol = (min(255,int(darkScale*txCol[0])),min(255,int(darkScale*txCol[1])),min(255,int(darkScale*txCol[2])))

if bgCol[0]+bgCol[1]+bgCol[2] == 0:
    mbgCol = (127,127,127)
else:
    mediumBgScale = 3*127.5/(bgCol[0]+bgCol[1]+bgCol[2])
    mbgCol = (min(255,int(mediumBgScale*bgCol[0])),min(255,int(mediumBgScale*bgCol[1])),min(255,int(mediumBgScale*bgCol[2])))

randParamVar = highParamChance/((49.999-1)**2) \
             + highParamChance/((highParamChance-1)**2) \
             - 2*highParamChance/((49.999-1)*(highParamChance-1))

global renderedPointsL

showPoints = [True for p in points]

calc = True

global recentre
recentre = True

paused0 = False
paused1 = False

skip = False
skipto = 0
comparedTo = 0

global zoomOut
global zoomIn
global toggles
global squash
global stretch
global skippable
global toggleCalc
global toggleTamper
global stepping
global pointCount
global currentPoints
global paramInfo
global changeIncrement
global funcInfo
global funcButtons
global numPointsInfo
global centreInfo
global renderable
global toggleAcc
global togglePull
global toggleInfo
global toggleParams
global shuffleParams
global showLyapunov
global save
global load
global loadList
global reset
global hide

zoomOut = True
zoomIn = True
toggles = True
squash = True
stretch = True
skippable = True
toggleCalc = True
toggleTamper = True
stepping = False
pointCount = True
currentPoints = True
paramInfo = False
changeIncrement = True
funcInfo = True
funcButtons = True
numPointsInfo = True
centreInfo = True
renderable = True
toggleAcc = True
togglePull = True
toggleInfo = [True,True,True]
toggleParams = True
shuffleParams = True
showLyapunov = False
save = True
load = True
loadList = False
reset = True
hide = False

global calcLyapunov
global Lcalcs
calcLyapunov = False
Lcalcs = 0

selectedToggle = 0
showCalcCounts = False
showRenderCounts  = False

accumulate = False
accumulatePending = False
basinPull = False
pullPending = False

global paramScroll
global paramStartY
global paramScrolledTo
global paramScrollStart
global paramScrollSize
paramScroll = False
paramStartY = 0
paramScrolledTo = 0
paramScrollStart = 0
paramScrollSize = 15

global loadScroll
global loadStartY
global loadScrolledTo
global loadScrollStart
potentialLoadScroll = False
loadScroll = False
loadStartY = 0
loadScrolledTo = 0
loadScrollStart = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            if stepping or paramInfo:
                if mousePos[0] < maxParamSize and 127 < mousePos[1] < 127+60*min(len(params),paramScrollSize):
                    paramScroll = True
                    paramStartY = mousePos[1]
                    paramScrollStart = paramScrolledTo
            if loadList:
                if 380 < mousePos[0] < 380 + max(120,font.size("0")[0]*(math.log(len(loadFrom)-1,10)+1)) and 127 < mousePos[1] < 127+60*min(len(loadFrom),20):
                    potentialLoadScroll = True
                    loadStartY = mousePos[1]
                    loadScrollStart = loadScrolledTo
        if event.type == pygame.MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()
            if paramScroll:
                paramScrolledTo = min(0,max(60*(paramScrollSize-len(params)),paramScrollStart+mousePos[1]-paramStartY))
            if potentialLoadScroll:
                loadScroll = True
                potentialLoadScroll = False
            if loadScroll:
                loadScrolledTo = min(0,max(60*(20-len(loadFrom)),loadScrollStart+mousePos[1]-loadStartY))
        if event.type == pygame.MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos()
            if paramScroll:
                paramScrolledTo = min(0,max(60*(paramScrollSize-len(params)),paramScrollStart+mousePos[1]-paramStartY))
                paramScroll = False
            elif loadScroll:
                loadScrolledTo = min(0,max(60*(20-len(loadFrom)),loadScrollStart+mousePos[1]-loadStartY))
                loadScroll = False
                potentialLoadScroll = False
            else:
                buttoned = False
                potentialLoadScroll = False
                funcy = (min(len(params),paramScrollSize))*60 if paramInfo or stepping else 0
                
                if zoomOut:
                    if w-260 < mousePos[0] < w-130 and h-145 < mousePos[1]:
                        scale = scale/1.1
                        sv = scale*vstretch
                        
                        buttoned = True
                
                if zoomIn:
                    if w-130 < mousePos[0] and h-145 < mousePos[1]:
                        scale = scale*1.1
                        sv = scale*vstretch
                        
                        buttoned = True
                
                if toggles:
                    if w-130 < mousePos[0] and h-290 < mousePos[1] < h-145:
                        selectedToggle = (selectedToggle + 1) % numPoints
                        
                        buttoned = True
                    
                    if w-260 < mousePos[0] < w-130 and h-290 < mousePos[1] < h-145:
                        showPoints[selectedToggle] = not showPoints[selectedToggle]
                        
                        buttoned = True
                
                if squash:
                    if 120 > mousePos[0] and h-130 < mousePos[1]:
                        vstretch = vstretch/1.1
                        sv = scale*vstretch
                        
                        buttoned = True
                
                if stretch:
                    if 120 > mousePos[0] and h-260 < mousePos[1] < h-130:
                        vstretch = vstretch*1.1
                        sv = scale*vstretch
                        
                        buttoned = True
                
                if skippable:
                    if w120//2-190 < mousePos[0] < w120//2-60 and h-295 < mousePos[1] < h-155 and True in showPoints:
                        skip = True
                        currentCalculated = 0
                        for i in range(numPoints):
                            currentCalculated += len(pointLists[i]) if showPoints[i] else 0
                        comparedTo = []
                        for i in range(numPoints):
                            if showPoints[i]:
                                comparedTo.append(i)
                        renderedPoints = 0
                        for i in range(numPoints):
                            renderedPoints += renderedPointsL[i] if showPoints[i] else 0
                        skipto = preferredNumPoints*currentCalculated//renderedPoints
                        showPoints = [False for p in points]
                        recentre = False
                        calc = True
                        
                        buttoned = True
                
                if toggleCalc:
                    if w120//2-60 < mousePos[0] < w120//2+60 and h-295 < mousePos[1] < h-155:
                        calc = not calc
                        
                        buttoned = True
                
                if toggleTamper:
                    if w120//2+60 < mousePos[0] < w120//2+190 and h-295 < mousePos[1] < h-155:
                        recentre = not recentre
                        
                        buttoned = True
                
                if stepping:
                    if 25+maxParamSize < mousePos[0] < 145+maxParamSize and 127 < mousePos[1] < 127+60*min(len(params),paramScrollSize):
                        for param in range(len(params)):
                            if 127+param*60+paramScrolledTo < mousePos[1] < 187+param*60+paramScrolledTo:
                                index = list(params.keys())[param]
                                if mousePos[0] < 85+maxParamSize:
                                    params[index] -= 10**increment
                                else:
                                    params[index] += 10**increment
                                params[index] = round(params[index]*10000)/10000
                                
                                calc = True
                                pointLists = [[] for p in points]
                                points = [p for p in startingpoints]
                                pointsNew = ["" for p in points]
                                lyapunov = [0 for p in points]
                                Lcalcs = 0
                                paused0 = False
                                paused1 = False
                                skip = False
                                
                                buttoned = True
                
                if funcButtons:
                    if func > 0:
                        if 25+funcSize[0] < mousePos[0] < 85+funcSize[0] and 200+funcSize[1]//2+funcy < mousePos[1] < 260+funcSize[1]//2+funcy:
                            func -= 1
                            numPoints = funcNumPoints[func]
                            newParams = {}
                            for i in range(funcNumParams[func]):
                                if "m"+str(i) in list(params.keys()):
                                    newParams["m"+str(i)] = params["m"+str(i)]
                                else:
                                    newParams["m"+str(i)] = 1
                            params = {}
                            for i in range(funcNumParams[func]):
                                params["m"+str(i)] = newParams["m"+str(i)]
                            scale = 100
                            vstretch = 1
                            sv = 100
                            pos = (0,0)
                            recentre = True
                            calc = True
                            pointLists = [[] for p in points]
                            points = [p for p in startingpoints]
                            pointsNew = ["" for p in points]
                            lyapunov = [0 for p in points]
                            Lcalcs = 0
                            paused0 = False
                            paused1 = False
                            skip = False
                            loadFrom = []
                            loadList = False
                            
                            txCol = (0,0,0)
                            for pCol in pCols[:numPoints]:
                                txCol = (txCol[0]+pCol[0],txCol[1]+pCol[1],txCol[2]+pCol[2])
                            txCol = (txCol[0]//numPoints,txCol[1]//numPoints,txCol[2]//numPoints)
                            
                            lightScale = 3*195/(txCol[0]+txCol[1]+txCol[2])
                            ltCol = (min(255,int(lightScale*txCol[0])),min(255,int(lightScale*txCol[1])),min(255,int(lightScale*txCol[2])))
                            darkScale = 3*60/(txCol[0]+txCol[1]+txCol[2])
                            dtCol = (min(255,int(darkScale*txCol[0])),min(255,int(darkScale*txCol[1])),min(255,int(darkScale*txCol[2])))
                            
                            buttoned = True
                    
                    if func < len(funcNumPoints)-1:
                        if 85+funcSize[0] < mousePos[0] < 145+funcSize[0] and 200+funcSize[1]//2+funcy < mousePos[1] < 260+funcSize[1]//2+funcy:
                            func += 1
                            numPoints = funcNumPoints[func]
                            newParams = {}
                            for i in range(funcNumParams[func]):
                                if "m"+str(i) in list(params.keys()):
                                    newParams["m"+str(i)] = params["m"+str(i)]
                                else:
                                    newParams["m"+str(i)] = 1
                            params = {}
                            for i in range(funcNumParams[func]):
                                params["m"+str(i)] = newParams["m"+str(i)]
                            scale = 100
                            vstretch = 1
                            sv = 100
                            pos = (0,0)
                            recentre = True
                            calc = True
                            pointLists = [[] for p in points]
                            points = [p for p in startingpoints]
                            pointsNew = ["" for p in points]
                            lyapunov = [0 for p in points]
                            Lcalcs = 0
                            paused0 = False
                            paused1 = False
                            skip = False
                            loadFrom = []
                            loadList = False
                            
                            txCol = (0,0,0)
                            for pCol in pCols[:numPoints]:
                                txCol = (txCol[0]+pCol[0],txCol[1]+pCol[1],txCol[2]+pCol[2])
                            txCol = (txCol[0]//numPoints,txCol[1]//numPoints,txCol[2]//numPoints)
                            
                            lightScale = 3*195/(txCol[0]+txCol[1]+txCol[2])
                            ltCol = (min(255,int(lightScale*txCol[0])),min(255,int(lightScale*txCol[1])),min(255,int(lightScale*txCol[2])))
                            darkScale = 3*60/(txCol[0]+txCol[1]+txCol[2])
                            dtCol = (min(255,int(darkScale*txCol[0])),min(255,int(darkScale*txCol[1])),min(255,int(darkScale*txCol[2])))
                            
                            buttoned = True
                
                if loadList:
                    if 370 < mousePos[0] < 370+max(120,font.size("0")[0]*(math.log(len(loadFrom)-1,10)+1)) and 127 < mousePos[1] < 127+60*min(len(loadFrom),20):
                        for option in range(len(loadFrom)):
                            if 127+option*60+loadScrolledTo < mousePos[1] < 187+option*60+loadScrolledTo:
                                loaded = loadFrom[option]
                                loadParts = loaded.split("{")
                                
                                func = int(loadParts[0])
                                numPoints = funcNumPoints[func]
                                rawParams = loadParts[1].split(",")
                                params = {}
                                for i in range(len(rawParams)):
                                    if i == 0:
                                        params[rawParams[i].split(":")[0][1:-1]] = float(rawParams[i].split(":")[1])
                                    else:
                                        params[rawParams[i].split(":")[0][2:-1]] = float(rawParams[i].split(":")[1])
                                
                                scale = 100
                                vstretch = 1
                                sv = 100
                                pos = (0,0)
                                recentre = True
                                calc = True
                                pointLists = [[] for p in points]
                                points = [p for p in startingpoints]
                                pointsNew = ["" for p in points]
                                lyapunov = [0 for p in points]
                                Lcalcs = 0
                                paused0 = False
                                paused1 = False
                                skip = False
                                loadFrom = []
                                loadList = False
                                
                                txCol = (0,0,0)
                                for pCol in pCols[:numPoints]:
                                    txCol = (txCol[0]+pCol[0],txCol[1]+pCol[1],txCol[2]+pCol[2])
                                txCol = (txCol[0]//numPoints,txCol[1]//numPoints,txCol[2]//numPoints)
                                
                                lightScale = 3*195/(txCol[0]+txCol[1]+txCol[2])
                                ltCol = (min(255,int(lightScale*txCol[0])),min(255,int(lightScale*txCol[1])),min(255,int(lightScale*txCol[2])))
                                darkScale = 3*60/(txCol[0]+txCol[1]+txCol[2])
                                dtCol = (min(255,int(darkScale*txCol[0])),min(255,int(darkScale*txCol[1])),min(255,int(darkScale*txCol[2])))
                            
                                buttoned = True
                
                if w-130 < mousePos[0] and 130 < mousePos[1] < 250:
                    hideAll()
                    if hide:
                        accumulate = accumulatePending
                        basinPull = pullPending
                    else:
                        accumulate = False
                        basinPull = False
                    calc = False
                        
                    buttoned = True
                
                if reset:
                    if w-250 < mousePos[0] < w-130 and mousePos[1] < 130:
                        pos = (0,0)
                        vstretch = 1
                        scale = 100
                        sv = 100
                        recentre = True
                        
                        buttoned = True
                
                if toggleAcc:
                    if w-130 < mousePos[0] and 250 < mousePos[1] < 370:
                        accumulatePending = not accumulatePending
                        
                        buttoned = True
                
                if togglePull:
                    if w-130 < mousePos[0] and 370 < mousePos[1] < 490:
                        pullPending = not pullPending
                        
                        buttoned = True
                
                if w-130 < mousePos[0] and mousePos[1] < 130:
                    hideAll()
                    
                    buttoned = True
                
                if toggleInfo[0] and toggleInfo[1] and toggleInfo[2]:
                    if mousePos[0] < 105 and 440+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0) < mousePos[1] < 535+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0):
                        toggleInfo[1] = not toggleInfo[1]
                        toggleInfo[2] = not toggleInfo[2]
                        
                        buttoned = True
                        
                    if mousePos[0] < 105 and 535+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0) < mousePos[1] < 630+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0):
                        toggleInfo[0] = not toggleInfo[0]
                        toggleInfo[2] = not toggleInfo[2]
                        
                        buttoned = True
                    
                    if mousePos[0] < 105 and 630+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0) < mousePos[1] < 725+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0):
                        toggleInfo[0] = not toggleInfo[0]
                        toggleInfo[1] = not toggleInfo[1]
                        
                        buttoned = True
                
                elif True in toggleInfo:
                    if mousePos[0] < 105 and 440+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0) < mousePos[1] < 535+(min(len(params),paramScrollSize)*60 if paramInfo or stepping else 0):
                        toggleInfo = [True for b in toggleInfo]
                        
                        buttoned = True
                
                if shuffleParams:
                    if mousePos[0] < 130 and mousePos[1] < 130:
                        for param in list(params.keys()):
                            params[param] = convRand(random.random())
                        calc = True
                        pointLists = [[] for p in points]
                        points = [p for p in startingpoints]
                        pointsNew = ["" for p in points]
                        lyapunov = [0 for p in points]
                        Lcalcs = 0
                        paused0 = False
                        paused1 = False
                        skip = False
                        
                        buttoned = True
                
                if toggleParams:
                    if 130 < mousePos[0] < 250 and mousePos[1] < 130:
                        paramInfo = not paramInfo
                        stepping = not stepping
                        
                        buttoned = True
                
                if save:
                    if 250 < mousePos[0] < 370 and mousePos[1] < 130:
                        fh = open("attractorSaveFile.txt","a")
                        fh.write(str(func)+str(params)[:-1]+"\n")
                        fh.close()
                        
                        buttoned = True
                        
                if load:
                    if 370 < mousePos[0] < 490 and mousePos[1] < 130:
                        if not loadList:
                            fh = open("attractorSaveFile.txt","r")
                            loadFrom = fh.readlines()
                            fh.close()
                        loadList = not loadList
                        
                        buttoned = True
                
                if changeIncrement:
                    if 25+incrementSize[0] < mousePos[0] < 85+incrementSize[0] and 140+incrementSize[1]//2+funcy < mousePos[1] < 200+incrementSize[1]//2+funcy:
                        increment -= 1
                        buttoned = True
                    if 85+incrementSize[0] < mousePos[0] < 145+incrementSize[0] and 140+incrementSize[1]//2+funcy < mousePos[1] < 200+incrementSize[1]//2+funcy:
                        increment += 1
                        buttoned = True
                
                if not buttoned:
                    if recentre:
                        pos = ((mousePos[0]-w2)/scale+pos[0],(h2-mousePos[1])/sv+pos[1])
    
    if not skip and not paused0 and len(pointLists[0]) == initialNumPoints:
        paused0 = True
        calc = False
    
    if not skip and not paused1 and len(pointLists[0])%preferredNumPoints == 0 and not len(pointLists[0]) == 0 and calc:
        paused1 = True
        calc = False
        recentre = False
    else:
        paused1 = False
    
    if skip:
        sumPoints = 0
        for i in range(numPoints):
            sumPoints += len(pointLists[i]) if i in comparedTo else 0
        if sumPoints == skipto:
            skip = False
            calc = False
            for i in range(numPoints):
                if i in comparedTo:
                    showPoints[i] = True
    
    if calc:
        try:
            if initialNumPoints > len(pointLists[0]) >= leeway and calcLyapunov:
                Delta = [(eta+p[0],eta+p[1]) for p in points]
                for i in range(5):
                    Delta = [function(Delta) for function in funcList]
                
                Base = [p for p in points]
                for i in range(5):
                    Base = [function(Base) for function in funcList]
                
                distOld = [math.sqrt(2)*eta for i in range(numPoints)]
                distNew = [math.sqrt((Delta[i][0]-Base[i][0])**2+(Delta[i][1]-Base[i][1])**2) for i in range(numPoints)]
                
                for i in range(numPoints):
                    if distNew[i]/distOld[i] > 0:
                        lyapunovList[i] += math.log(distNew[i]/distOld[i],2)/5
                Lcalcs += 1
            
            for i in range(numPoints):
                pointLists[i].append(points[i])
            
            pointsNew = [function(points) for function in funcList]
            
            test = [(int((p[0]-pos[0])*scale+w2),int((pos[1]-p[1])*sv+h2)) for p in pointsNew]
            
            points = [p for p in pointsNew]
        except ValueError:
            for param in list(params.keys()):
                params[param] = convRand(random.random())
            calc = True
            pointLists = [[] for p in points]
            points = [(convRand(random.random()),convRand(random.random())) for p in startingpoints]
            pointsNew = ["" for p in points]
            lyapunov = [0 for p in points]
            paused0 = False
            paused1 = False
            skip = False
        except OverflowError:
            for param in list(params.keys()):
                params[param] = convRand(random.random())
            calc = True
            pointLists = [[] for p in points]
            points = [(convRand(random.random()),convRand(random.random())) for p in startingpoints]
            pointsNew = ["" for p in points]
            lyapunov = [0 for p in points]
            paused0 = False
            paused1 = False
            skip = False
        except ZeroDivisionError:
            for param in list(params.keys()):
                params[param] = convRand(random.random())
            calc = True
            pointLists = [[] for p in points]
            points = [(convRand(random.random()),convRand(random.random())) for p in startingpoints]
            pointsNew = ["" for p in points]
            lyapunov = [0 for p in points]
            paused0 = False
            paused1 = False
            skip = False
    
    if len(pointLists[0])%pointsPerFrame == 0 or not calc:
        display(accumulate,ftCol,0,basinPull)