from cmu_112_graphics import *
import random, math, copy, time, webbrowser
from itertools import permutations


def appStarted(app):
    app.mode = 'homescreen'

    # CITATION: From https://www.pngall.com/rubiks-cube-png
    app.cubeImage = app.loadImage('cube.png')
    # CITATION: From https://cstimer.net/
    app.virtualControlsImage = app.loadImage('virtual controls.png')
    app.OLLImage = app.loadImage('https://www.speedsolving.com/wiki/images/3/37/OLLinfo.png')
    app.PLLImage = app.loadImage('https://www.speedsolving.com/wiki/images/7/75/PLLinfo.jpg')
    app.F2L = app.loadImage('https://www.speedsolving.com/wiki/images/f/fe/F2Linfo.png')
    app.F2LImage = app.scaleImage(app.F2L, 5/6)

    app.timerDelay = 1

    # Default colors
    app.background = 'gray'
    app.rColor = 'red'
    app.uColor = 'white'
    app.fColor = 'green'
    app.lColor = 'orange'
    app.dColor = 'yellow'
    app.bColor = 'blue'

    # 2D 3x3 cube in practice mode
    app.rows = 9
    app.cols = 12
    app.cellSize = 20
    app.leftRightMargin = (app.width - app.cols*app.cellSize) // 2
    app.topMargin = 40
    app.rFace = [ [app.rColor for i in range(3)] for i in range(3) ]
    app.uFace = [ [app.uColor for i in range(3)] for i in range(3) ]
    app.fFace = [ [app.fColor for i in range(3)] for i in range(3) ]
    app.lFace = [ [app.lColor for i in range(3)] for i in range(3) ]
    app.dFace = [ [app.dColor for i in range(3)] for i in range(3) ]
    app.bFace = [ [app.bColor for i in range(3)] for i in range(3) ]
    app.cubeNet = []
    for i in range(3):
        app.cubeNet += [['' for i in range(3)] + app.uFace[i] + ['' for i in range(6)]]
    for i in range(3):
        app.cubeNet += [app.lFace[i] + app.fFace[i] + app.rFace[i] + app.bFace[i]]
    for i in range(3):
        app.cubeNet += [['' for i in range(3)] + app.dFace[i] + ['' for i in range(6)]]

    # Practice mode variables
    app.isCubeSolved = True
    app.solveTime = 0
    app.firstMoveApplied = False
    app.moveCount = 0
    app.timeList = ''
    app.moveCountList = ''
    app.scrambleApplied = False
    app.startTime = 0

    # Homescreen buttons
    app.buttonCoords = [(50,300,175,350), (225,300,350,350), (50,400,175,450), (225,400,350,450), ((app.width-200)/2,500,(app.width+200)/2,550)]
    app.buttonText = ['Input', 'Practice', 'Trainer', 'Learn', 'Optimal 2x2 Solver']
    app.buttonColors = ['red', 'yellow', 'orange', 'blue', 'green']
    
    # Input mode
    app.manualInputColors = { 'white':  ( 35, 300, 115, 380), 
                              'green':  (160, 300, 240, 380), 
                              'red':    (285, 300, 365, 380), 
                              'blue':   ( 35, 405, 115, 485), 
                              'orange': (160, 405, 240, 485), 
                              'yellow': (285, 405, 365, 485) }
    app.currColor = ''

    # Sticker coordinates in standard xyz graph
    ufr = [ [0,0,0], [1,0,0], [1,0,1], [0,0,1] ]
    uf  = [ [1,0,0], [2,0,0], [2,0,1], [1,0,1] ]
    ulf = [ [2,0,0], [3,0,0], [3,0,1], [2,0,1] ]
    ur  = [ [0,0,1], [1,0,1], [1,0,2], [0,0,2] ]
    u   = [ [1,0,1], [2,0,1], [2,0,2], [1,0,2] ]
    ul  = [ [2,0,1], [3,0,1], [3,0,2], [2,0,2] ]
    urb = [ [0,0,2], [1,0,2], [1,0,3], [0,0,3] ]
    ub  = [ [1,0,2], [2,0,2], [2,0,3], [1,0,3] ]
    ubl = [ [2,0,2], [3,0,2], [3,0,3], [2,0,3] ]
    ruf = [ [0,0,0], [0,1,0], [0,1,1], [0,0,1] ]
    rf  = [ [0,1,0], [0,2,0], [0,2,1], [0,1,1] ]
    rfd = [ [0,2,0], [0,3,0], [0,3,1], [0,2,1] ]
    ru  = [ [0,0,1], [0,1,1], [0,1,2], [0,0,2] ]
    r   = [ [0,1,1], [0,2,1], [0,2,2], [0,1,2] ]
    rd  = [ [0,2,1], [0,3,1], [0,3,2], [0,2,2] ]
    rbu = [ [0,0,2], [0,1,2], [0,1,3], [0,0,3] ]
    rb  = [ [0,1,2], [0,2,2], [0,2,3], [0,1,3] ]
    rdb = [ [0,2,2], [0,3,2], [0,3,3], [0,2,3] ]
    fru = [ [0,0,0], [1,0,0], [1,1,0], [0,1,0] ]
    fu  = [ [1,0,0], [2,0,0], [2,1,0], [1,1,0] ]
    ful = [ [2,0,0], [3,0,0], [3,1,0], [2,1,0] ]
    fr  = [ [0,1,0], [1,1,0], [1,2,0], [0,2,0] ]
    f   = [ [1,1,0], [2,1,0], [2,2,0], [1,2,0] ]
    fl  = [ [2,1,0], [3,1,0], [3,2,0], [2,2,0] ]
    fdr = [ [0,2,0], [1,2,0], [1,3,0], [0,3,0] ]
    fd  = [ [1,2,0], [2,2,0], [2,3,0], [1,3,0] ]
    fld = [ [2,2,0], [3,2,0], [3,3,0], [2,3,0] ]
    app.stickers = [ubl, ub, urb, ul, u, ur, ulf, uf, ufr, ful, fu, fru, fl, f, fr, fld, fd, fdr, ruf, ru, rbu, rf, r, rb, rfd, rd, rdb]

    # Convert 3x1 matrices to 1x3 for the sake of multiplication
    for i in app.stickers:
        for j in i:
            for k in range(len(j)):
                j[k] *= 42
    app.stickerVectors = []
    for s in app.stickers:
        for v in s:
            app.stickerVectors.append([[v[0]], [v[1]], [v[2]]])
    
    # Rotation angles and corresponding matrices for isometric graphics
    app.rotAngle1 = 5*math.pi/4
    app.rotMatrix1 = [ [math.cos(app.rotAngle1), 0, -math.sin(app.rotAngle1)],
                       [0, 1, 0],
                       [math.sin(app.rotAngle1), 0, math.cos(app.rotAngle1)] ]
    app.rotAngle2 = math.asin(math.tan(math.pi/6))
    app.rotMatrix2 = [ [1, 0, 0],
                       [0, math.cos(app.rotAngle2), math.sin(app.rotAngle2)],
                       [0, -math.sin(app.rotAngle2), math.cos(app.rotAngle2)] ]

    # Multiply vectors by the rotation matrices, then by [[1,0,0],[0,1,0],[0,0,0]] to convert to 2D coordinates
    app.cubeCoordsRot = []
    for v in app.stickerVectors:
        app.cubeCoordsRot.append(matrixMultiply(app.rotMatrix2, matrixMultiply(app.rotMatrix1, v)))
    app.cubeCoordsIso = []
    for coord in app.cubeCoordsRot:
        app.cubeCoordsIso.append(matrixMultiply([[1,0,0],[0,1,0],[0,0,0]], coord))
    
    # Coordinates for showing hidden sides with isometric graphics
    app.hiddenSidesCoords = []
    for i in range(len(app.cubeCoordsIso)):
        coord = copy.deepcopy(app.cubeCoordsIso[i])
        if i in range(36):
            coord[1][0] += 210
            app.hiddenSidesCoords.append(coord)
        elif i in range(72):
            coord[0][0] += 210*math.cos(math.pi/6)
            coord[1][0] -= 210*math.sin(math.pi/6)
            app.hiddenSidesCoords.append(coord)
        elif i in range(108):
            coord[0][0] -= 210*math.cos(math.pi/6)
            coord[1][0] -= 210*math.sin(math.pi/6)
            app.hiddenSidesCoords.append(coord)

    app.hiddenSidesRevealed = False

    app.cubeIsSolvable = True
    app.prevX, app.prevY, app.currX, app.currY = None, None, None, None

    app.isoGraphics = False

    # Optimal 2x2 solver mode, the net is compiled by only using the corners of the 3x3 net
    app.scramble = ''
    app.sol = None
    app.allSols = None
    app.rows2x2 = 6
    app.cols2x2 = 8
    app.cellSize2x2 = 27.5
    app.leftRightMargin2x2 = (app.width - app.cols2x2*app.cellSize2x2) // 2
    app.topMargin2x2 = 40
    app.cubeNet2x2 = [ ['' for i in range(2)] + [app.uFace[0][0], app.uFace[0][2]] + ['' for i in range(4)],
                       ['' for i in range(2)] + [app.uFace[2][0], app.uFace[2][2]] + ['' for i in range(4)],
                       [app.lFace[0][0], app.lFace[0][2], app.fFace[0][0], app.fFace[0][2], app.rFace[0][0], app.rFace[0][2], app.bFace[0][0], app.bFace[0][2]],
                       [app.lFace[2][0], app.lFace[2][2], app.fFace[2][0], app.fFace[2][2], app.rFace[2][0], app.rFace[2][2], app.bFace[2][0], app.bFace[2][2]],
                       ['' for i in range(2)] + [app.dFace[0][0], app.dFace[0][2]] + ['' for i in range(4)],
                       ['' for i in range(2)] + [app.dFace[2][0], app.dFace[2][2]] + ['' for i in range(4)] ]


###################
### Home Screen ###
###################
# Contains buttons for each mode of the program

def homescreen_mousePressed(app, event):
    x, y = event.x, event.y
    if x in range(50, 175):
        if y in range(300, 350):
            app.mode = 'manualInput'
        elif y in range(400, 450):
            app.mode = 'trainer'
    elif x in range(225, 350):
        if y in range(300, 350):
            app.mode = 'practice'
        elif y in range(400, 450):
            webbrowser.open('https://www.youtube.com/watch?v=1t1OL2zN0LQ')
    if x in range((app.width-200)//2,(app.width+200)//2) and y in range(500,550):
        app.scramble = app.getUserInput('Input a scramble\nValid moves are: R, R\', R2, U, U\', U2, F, F\', F2\nMake sure there are no spaces before or after the scramble and each move is separated by one space')
        if app.scramble == None:
            return
        else:
            for move in app.scramble.split(' '):
                if move not in ['U', "U'", 'U2', 'F', "F'", 'F2', 'R', "R'", 'R2']:
                    app.showMessage('This scramble is invalid, please double check it')
                    return
        applyScramble(app, app.scramble)
        updateCube(app)
        app.mode = 'solver2x2'

def homescreen_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.background)
    canvas.create_image(app.width/2, 170, image=ImageTk.PhotoImage(app.cubeImage))
    canvas.create_text(app.width/2, 30, text='Welcome to PyCube!', font='Arial 28 bold')
    drawButtons(app, canvas)


#####################
### Practice Mode ###
#####################
# Use the keyboard to control a virtual cube shown in either 2D or 2.5D
# Times and move counts of each solve in practice mode are tracked

def practice_keyPressed(app, event):
    moveKeybinds(app, event)
    if event.key == 'Escape':
        timeList, moveCountList = app.timeList, app.moveCountList
        resetCube(app)
        app.isCubeSolved = True
        app.solveTime = 0
        app.firstMoveApplied = False
        app.moveCount = 0
        app.scrambleApplied = False
        app.timeList, app.moveCountList = timeList, moveCountList
    elif event.key == 'Space':
        scramble = generateScramble()
        applyScramble(app, scramble)
        app.scrambleApplied = True

def practice_mousePressed(app, event):
    returnToHome(app, event)

def practice_timerFired(app):
    updateCube(app)
    isCubeSolved(app)
    if app.isCubeSolved and app.firstMoveApplied and app.scrambleApplied:
        app.solveTime = time.time() - app.startTime
        resetTimer(app)

def practice_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.background)
    drawReturnToHomeButton(app, canvas)
    if not app.isoGraphics:
        drawCube(app, canvas)
        drawMoves(app, canvas)
        drawTimeList(app, canvas)
        drawMoveCountList(app, canvas)
        canvas.create_image(0, 2*app.topMargin + app.rows*app.cellSize, anchor=NW, image=ImageTk.PhotoImage(app.virtualControlsImage))
    elif app.isoGraphics:
        drawCube3D(app, canvas)
        if app.hiddenSidesRevealed:
            drawHiddenSides(app, canvas)
        drawMoves(app, canvas)
        canvas.create_text(320, 420, anchor=NE, text=('Times' + app.timeList))
        canvas.create_text(330, 420, anchor=NW, text=('Move Count' + app.moveCountList))
        canvas.create_image(0, 420, anchor=NW, image=ImageTk.PhotoImage(app.scaleImage(app.virtualControlsImage,2.15/3)))
        drawShowSides(app, canvas)
    drawToggle3D(app, canvas)
    drawInstructions(app, canvas)


####################
### Trainer Mode ###
####################
# User can choose to train F2L, OLL, or PLL (last three steps of CFOP method)
# F2L, OLL, and PLL algorithms for each case are stored in dictionaries
# AUF simply turns the top face and is added to OLL and PLL so the same cases aren't always seen from the same angle

preAUF = ['U ', "U' ", 'U2 ', '']
postAUF = [' U', " U'", ' U2', '']

PLL = { 'Aa':"x R' U R' D2 R U' R' D2 R2 x'",
        'Ab':"x R2 D2 R U R' D2 R U' R x'",
        'E':"x' R U' R' D R U R' D' R U R' D R U' R' D' x",
        'F':"R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R",
        'Ga':"R2 U R' U R' U' R U' R2 D U' R' U R D' U",
        'Gb':"R' U' R U D' R2 U R' U R U' R U' R2 U' D",
        'Gc':"R2 U' R U' R U R' U R2 D' U R U' R' D U'",
        'Gd':"R U R' U' D R2 U' R U' R' U R' U R2 U D'",
        'H':"M2 U M2 U2 M2 U M2",
        'Ja':"R' U L' U2 R U' R' U2 R L U'",
        'Jb':"R U R' F' R U R' U' R' F R2 U' R' U'",
        'Na':"R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'",
        'Nb':"Rw' D' F Rw U' Rw' F' D Rw2 U Rw' U' Rw' F Rw F'",
        'Ra':"R U' R' U' R U R D R' U' R D' R' U2 R' U'",
        'Rb':"R' U2 R' D' R U' R' D R U R U' R' U' R U'",
        'T':"R U R' U' R' F R2 U' R' U' R U R' F'",
        'Ua':"R U' R U R U R U' R' U' R2",
        'Ub':"R2 U R U R' U' R' U' R' U R'",
        'V':"R' U R U' R' Fw' U' R U2 R' U' R U' R' Fw R",
        'Y':"F R U' R' U' R U R' F' R U R' U' R' F R F'",
        'Z':"M' U M2 U M2 U M' U2 M2 U'" }

OLL = { 1:"R U2 R2 F R F' U2 R' F R F'",
        2:"R U' R2 D' Rw U Rw' D R2 U R'",
        3:"Fw R U R' U' Fw' U' F R U R' U' F'",
        4:"F U R U' R' F' U' F R U R' U' F'",
        5:"Rw' U2 R U R' U Rw",
        6:"Rw U2 R' U' R U' Rw'",
        7:"Rw U R' U R U2 Rw'",
        8:"Rw' U' R U' R' U2 Rw",
        9:"R U R' U' R' F R2 U R' U' F'",
        10:"R U R' U R' F R F' R U2 R'",
        11:"Rw' R2 U R' U R U2 R' U M'",
        12:"Rw R2 U' R U' R' U2 R U' M",
        13:"F U R U2 R' U' R U R' F'",
        14:"R' F R U R' F' R F U' F'",
        15:"Rw' U' Rw R' U' R U Rw' U Rw",
        16:"Rw U Rw' R U R' U' Rw U' Rw'",
        17:"R U R' U R' F R F' U2 R' F R F'",
        18:"Rw U R' U R U2 Rw2 U' R U' R' U2 Rw",
        19:"M U R U R' U' M' R' F R F'",
        20:"M U R U R' U' M2 U R U' Rw'",
        21:"R U R' U R U' R' U R U2 R'",
        22:"R U2 R2 U' R2 U' R2 U2 R",
        23:"R2 D' R U2 R' D R U2 R",
        24:"Rw U R' U' Rw' F R F'",
        25:"F R' F' Rw U R U' Rw'",
        26:"R' U' R U' R' U2 R",
        27:"R U R' U R U2 R'",
        28:"Rw U R' U' M U R U' R'",
        29:"Rw2 D' Rw U Rw' D Rw2 U' Rw' U' Rw",
        30:"Rw' D' Rw U' Rw' D Rw2 U' Rw' U Rw U Rw'",
        31:"R' U' F U R U' R' F' R",
        32:"R U B' U' R' U R B R'",
        33:"R U R' U' R' F R F'",
        34:"R U R2 U' R' F R U R U' F'",
        35:"R U2 R2 F R F' R U2 R'",
        36:"R U R' F' R U R' U' R' F R U' R' F R F'",
        37:"F R' F' R U R U' R'",
        38:"R U R' U R U' R' U' R' F R F'",
        39:"L F' L' U' L U F U' L'",
        40:"R' F R U R' U' F' U R",
        41:"R U R' U R U2 R' F R U R' U' F'",
        42:"R' U' R U' R' U2 R F R U R' U' F'",
        43:"R' U' F' U F R",
        44:"F U R U' R' F'",
        45:"F R U R' U' F'",
        46:"R' U' R' F R F' U R",
        47:"F' L' U' L U L' U' L U F",
        48:"F R U R' U' R U R' U' F'",
        49:"Rw U' Rw2 U Rw2 U Rw2 U' Rw",
        50:"Rw' U Rw2 U' Rw2 U' Rw2 U Rw'",
        51:"F U R U' R' U R U' R' F'",
        52:"R U R' U R U' B U' B' R'", }

F2L = { 1:"U R U' R'",
        2:"F R' F' R",
        3:"F' U' F",
        4:"R U R'",
        5:"U' R U R' U2 R U' R'",
        6:"U' Rw U' R' U R U Rw'",
        7:"U' R U2 R' U2 R U' R'",
        8:"U F' U2 F U2 F' U F",
        9:"U' R U' R' U F' U' F",
        10:"U2 R U' R' U' R U R'",
        11:"U' R U2 R' U F' U' F",
        12:"R' U2 R2 U R2 U R",
        13:"U F' U F U' F' U' F",
        14:"U' R U' R' U R U R'",
        15:"F' U F U2 R U R'",
        16:"R U' R' U2 F' U' F",
        17:"R U2 R' U' R U R'",
        18:"F' U2 F U F' U' F",
        19:"U R U2 R' U R U' R'",
        20:"U' F' U2 F U' F' U F",
        21:"R U' R' U2 R U R'",
        22:"F' L' U2 L F",
        23:"U R U' R' U' R U' R' U R U' R'",
        24:"F U R U' R' F' R U' R'",
        25:"U' R' F R F' R U R'",
        26:"U R U' R' F R' F' R",
        27:"R U' R' U R U' R'",
        28:"R U R' U' F R' F' R",
        29:"F' U' F U F' U' F",
        30:"R U R' U' R U R'",
        31:"U' R' F R F' R U' R'",
        32:"U R U' R' U R U' R' U R U' R'",
        33:"U' R U' R' U2 R U' R'",
        34:"U R U R' U2 R U R'",
        35:"U' R U R' U F' U' F",
        36:"U F' U' F U' R U R'",
        37:"R2 U2 F R2 F' U2 R' U R'",
        38:"R U' R' U' R U R' U2 R U' R'",
        39:"R U' R' U R U2 R' U R U' R'",
        40:"R U' R' U' R U' R' U F' U' F",
        41:"R U R' U' R U' R' U2 F' U' F" }

def trainer_mousePressed(app, event):
    returnToHome(app, event)
    x, y = event.x, event.y
    if x in range(0, 200) and y in range(60, 260):
        app.mode = 'trainerOLL'
        makeMove(app, 'Z2') # Doing z2 puts yellow on top which is the most common orientation that people do OLL from
        app.lFace[0], app.fFace[0], app.rFace[0], app.bFace[0] = (['silver' for i in range(3)] for _ in range(4)) # Stickers not applicable to OLL are grayed out
    elif x in range(200, 400) and y in range(60, 260):
        app.mode = 'trainerPLL'
        makeMove(app, 'Z2') # Same thing as OLL
    elif x in range(100,300) and y in range(290,490):
        app.mode = 'trainerF2L'
        makeMove(app, 'Z2') # Same thing as OLL
        app.uFace = [ ['silver' for i in range(3)] for _ in range(3) ]
        app.lFace[0], app.fFace[0], app.rFace[0], app.bFace[0] = (['silver' for i in range(3)] for _ in range(4)) # Stickers not applicable to F2L are grayed out

def trainer_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.background)
    canvas.create_text(app.width/2, 30, text='Choose a step to practice below', font='Arial 16 bold')
    canvas.create_image(0, 60, image=ImageTk.PhotoImage(app.OLLImage), anchor=NW)
    canvas.create_image(200, 60, image=ImageTk.PhotoImage(app.PLLImage), anchor=NW)
    canvas.create_image(100, 290, image=ImageTk.PhotoImage(app.F2LImage), anchor=NW)
    canvas.create_rectangle(0, 60, 200, 260, outline='black', width=2)
    canvas.create_rectangle(200, 60, 400, 260, outline='black', width=2)
    canvas.create_rectangle(100, 290, 300, 490, outline='black', width=2)
    canvas.create_text(100, 275, text='OLL', font='Arial 14 bold')
    canvas.create_text(300, 275, text='PLL', font='Arial 14 bold')
    canvas.create_text(200, 505, text='F2L', font='Arial 14 bold')
    drawReturnToHomeButton(app, canvas)


###################
### OLL Trainer ###
###################

def trainerOLL_mousePressed(app, event):
    returnToHome(app, event)

def trainerOLL_keyPressed(app, event):
    moveKeybinds(app, event)
    if event.key == 'Escape':
        resetCube(app)
        makeMove(app, 'Z2')
        app.lFace[0], app.fFace[0], app.rFace[0], app.bFace[0] = ['silver' for i in range(3)], ['silver' for i in range(3)], ['silver' for i in range(3)], ['silver' for i in range(3)]
    elif event.key == 'Space':
        ollNum = random.choice(list(OLL))
        ollAlg = OLL[ollNum]
        applyScramble(app, random.choice(preAUF) + inverseScramble(ollAlg) + random.choice(postAUF))

def trainerOLL_timerFired(app):
    updateCube(app)

def trainerOLL_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.background)
    drawReturnToHomeButton(app, canvas)
    if not app.isoGraphics:
        drawCube(app, canvas)
        canvas.create_image(0, 2*app.topMargin + app.rows*app.cellSize, anchor=NW, image=ImageTk.PhotoImage(app.virtualControlsImage))
    elif app.isoGraphics:
        drawCube3D(app, canvas)
        if app.hiddenSidesRevealed:
            drawHiddenSides(app, canvas)
        canvas.create_image(0, 420, anchor=NW, image=ImageTk.PhotoImage(app.scaleImage(app.virtualControlsImage,2.15/3)))
        drawShowSides(app, canvas)
    drawToggle3D(app, canvas)
    drawInstructions(app, canvas)


###################
### PLL Trainer ###
###################

def trainerPLL_mousePressed(app, event):
    returnToHome(app, event)

def trainerPLL_keyPressed(app, event):
    moveKeybinds(app, event)
    if event.key == 'Escape':
        resetCube(app)
        makeMove(app, 'Z2')
    elif event.key == 'Space':
        pllCase = random.choice(list(PLL))
        pllAlg = PLL[pllCase]
        applyScramble(app, random.choice(preAUF) + inverseScramble(pllAlg) + random.choice(postAUF))

def trainerPLL_timerFired(app):
    updateCube(app)

def trainerPLL_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.background)
    drawReturnToHomeButton(app, canvas)
    if not app.isoGraphics:
        drawCube(app, canvas)
        canvas.create_image(0, 2*app.topMargin + app.rows*app.cellSize, anchor=NW, image=ImageTk.PhotoImage(app.virtualControlsImage))
    elif app.isoGraphics:
        drawCube3D(app, canvas)
        if app.hiddenSidesRevealed:
            drawHiddenSides(app, canvas)
        canvas.create_image(0, 420, anchor=NW, image=ImageTk.PhotoImage(app.scaleImage(app.virtualControlsImage,2.15/3)))
        drawShowSides(app, canvas)
    drawToggle3D(app, canvas)
    drawInstructions(app, canvas)


###################
### F2L Trainer ###
###################

def trainerF2L_mousePressed(app, event):
    returnToHome(app, event)

def trainerF2L_keyPressed(app, event):
    moveKeybinds(app, event)
    if event.key == 'Escape':
        resetCube(app)
        makeMove(app, 'Z2')
        app.uFace = [ ['silver' for i in range(3)] for _ in range(3) ]
        app.lFace[0], app.fFace[0], app.rFace[0], app.bFace[0] = (['silver' for i in range(3)] for _ in range(4))
    elif event.key == 'Space':
        f2lCase = random.choice(list(F2L))
        f2lAlg = F2L[f2lCase]
        applyScramble(app, inverseScramble(f2lAlg) + random.choice(postAUF))

def trainerF2L_timerFired(app):
    updateCube(app)

def trainerF2L_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.background)
    drawReturnToHomeButton(app, canvas)
    if not app.isoGraphics:
        drawCube(app, canvas)
        canvas.create_image(0, 2*app.topMargin + app.rows*app.cellSize, anchor=NW, image=ImageTk.PhotoImage(app.virtualControlsImage))
    elif app.isoGraphics:
        drawCube3D(app, canvas)
        if app.hiddenSidesRevealed:
            drawHiddenSides(app, canvas)
        canvas.create_image(0, 420, anchor=NW, image=ImageTk.PhotoImage(app.scaleImage(app.virtualControlsImage,2.15/3)))
        drawShowSides(app, canvas)
    drawToggle3D(app, canvas)
    drawInstructions(app, canvas)


####################
### Manual Input ###
####################
# User inputs their own cube based on the stickers
# The cube will get put into practice mode if it is entered correctly and solvable

def manualInput_mousePressed(app, event):
    returnToHome(app, event)
    x, y = event.x, event.y
    if x in range((app.width-125)//2, (app.width+125)//2) and y in range(app.height-125, app.height-75):
        if stickersAreValid(app) and cubeIsSolvable(app):
            app.mode = 'practice'
            app.scrambleApplied = True
            app.cubeIsSolvable = True
        else:
            app.cubeIsSolvable = False
    for color in app.manualInputColors:
        x0, y0, x1, y1 = app.manualInputColors[color]
        if x in range(x0,x1) and y in range(y0,y1):
            app.currColor = color
    for r in range(len(app.cubeNet)):
        for c in range(len(app.cubeNet[0])):
            if app.cubeNet[r][c] != '':
                x0, y0, x1, y1 = getCellBounds(app, r, c)
                if x in range(x0, x1) and y in range(y0, y1) and app.currColor != '':
                    app.cubeNet[r][c] = app.currColor
    app.cubeNet[1][4] = 'white'
    app.cubeNet[4][1] = 'orange'
    app.cubeNet[4][4] = 'green'
    app.cubeNet[4][7] = 'red'
    app.cubeNet[4][10] = 'blue'
    app.cubeNet[7][4] = 'yellow'

def manualInput_timerFired(app):
    for i in range(3):
        for j in range(3):
            if i != 1 or j != 1:
                app.uFace[i][j] = app.cubeNet[i][j+3]
                app.dFace[i][j] = app.cubeNet[i+6][j+3]
                app.lFace[i][j] = app.cubeNet[i+3][j]
                app.fFace[i][j] = app.cubeNet[i+3][j+3]
                app.rFace[i][j] = app.cubeNet[i+3][j+6]
                app.bFace[i][j] = app.cubeNet[i+3][j+9]

def manualInput_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.background)
    drawReturnToHomeButton(app, canvas)
    drawCube(app, canvas)
    drawColorButtons(app, canvas)
    drawGoToPractice(app, canvas)
    if not app.cubeIsSolvable:
        canvas.create_text(app.width/2, app.height-150, text='Your cube is entered incorrectly, please double check it', font='Arial 10')


##########################
### Optimal 2x2 Solver ###
##########################
# The cube is defined as a class here instead of colors in a 2D list
# Each piece is represented as a 2D list
# piece[0] represents which piece it is; 0=wbo, 1=wbr, 2=wgr, 3=wgo, 4=ybr, 5=ygr, 6=ygo (letters correspond to colors, ybo is fixed)
# piece[1] represents orientation where oriented means that either white/yellow is on top/bottom; 0=oriented, 1=clockwise twist from oriented, 2=counterclockwise twist from oriented
class Cube2x2(object):

    # Initializes the cube in its solved state unless otherwise specified
    def __init__(self, piece0=[0,0], piece1=[1,0], piece2=[2,0], piece3=[3,0], piece4=[4,0], piece5=[5,0], piece6=[6,0]):
        self.pieces = [piece0, piece1, piece2, piece3, piece4, piece5, piece6]

    def isSolved(self):
        return self.pieces == [[0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0]]

    # Move functions
    def U(self):
        self.pieces[0], self.pieces[1], self.pieces[2], self.pieces[3] = self.pieces[3], self.pieces[0], self.pieces[1], self.pieces[2]
    def Ui(self):
        for i in range(3):
            self.U()
    def U2(self):
        for i in range(2):
            self.U()
    def R(self):
        self.pieces[1][0], self.pieces[2][0], self.pieces[4][0], self.pieces[5][0] = self.pieces[2][0], self.pieces[5][0], self.pieces[1][0], self.pieces[4][0]
        self.pieces[1][1], self.pieces[2][1], self.pieces[4][1], self.pieces[5][1] = (self.pieces[2][1]+1)%3, (self.pieces[5][1]+2)%3, (self.pieces[1][1]+2)%3, (self.pieces[4][1]+1)%3
    def Ri(self):
        for i in range(3):
            self.R()
    def R2(self):
        for i in range(2):
            self.R()
    def F(self):
        self.pieces[2][0], self.pieces[3][0], self.pieces[5][0], self.pieces[6][0] = self.pieces[3][0], self.pieces[6][0], self.pieces[2][0], self.pieces[5][0]
        self.pieces[2][1], self.pieces[3][1], self.pieces[5][1], self.pieces[6][1] = (self.pieces[3][1]+1)%3, (self.pieces[6][1]+2)%3, (self.pieces[2][1]+2)%3, (self.pieces[5][1]+1)%3
    def Fi(self):
        for i in range(3):
            self.F()
    def F2(self):
        for i in range(2):
            self.F()

    # Applies a sequence of moves to the cube
    def applyAlg(self, alg):
        if alg == '':
            return
        for move in alg.split(' '):
            if move[-1] == "'":
                eval('self.' + move[0] + 'i()')
            else:
                eval('self.' + move + '()')
    
    # Finds one optimal solution to the cube
    def optimalSolve(self):
        if self.isSolved():
            return "The cube is already solved"
        scram = copy.deepcopy(self.pieces)
        solvedCube = Cube2x2([0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0])
        moves = ['U', "U'", 'U2', 'R', "R'", 'R2', 'F', "F'", 'F2']
        algs = { 0:[''], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[] } # algs[i] stores all sequences of moves (algorithms/algs) of length i
        checkedStates = dict() # Stores each cube state reached from the scrambled state along with the (shortest) alg used to reach it
        # The maximum number of moves needed to solve any 2x2 state is 11, so we can efficiently semi-brute-force check this
        # By checking algs applied to both the scrambled cube and solved cube, we only need to check algs up to length 5 on the scrambled cube and up to length 6 on the solved cube
        # Once an alg of length n (1) on to the scrambled cube reaches the same state as another alg of length either n or n+1 (2) on the solved cube, the solution is simply
        # (1), (2)' where (2)' is the inverse of (2)
        # This works because if the scrambled state is A, the solved state is B, and the intermediate state is C, we want to find A->C->B; (1) is A->C and (2) is B->C
        for i in range(6):
            for alg in algs[i]:
                # Reset cube to scrambled state, check all algs of length i, add new states to checkedStates dictionary
                eval('self.__init__' + str(tuple(scram)))
                self.applyAlg(alg)
                currState = tuple([tuple(piece) for piece in self.pieces])
                checkedStates[currState] = checkedStates.get(currState, alg)
                # Generate all algs of length i+1 by taking all algs of length i and adding every possible next move that doesn't turn the same side twice in a row
                for move in moves:
                    if alg == '':
                        algs[i+1].append(move)
                    elif alg.split(' ')[-1][0] != move[0]:
                        algs[i+1].append(alg + ' ' + move)
            # Check algs of length i and i+1 from a solved cube to see if they match any state reached from the scrambled cube
            for alg2 in algs[i] + algs[i+1]:
                solvedCube.applyAlg(alg2)
                stateFromSolved = tuple([tuple(piece) for piece in solvedCube.pieces])
                if stateFromSolved in checkedStates:
                    self.__init__([0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0])
                    if checkedStates[stateFromSolved] == '':
                        return inverseScramble(alg2)
                    else:
                        return checkedStates[stateFromSolved] + ' ' + inverseScramble(alg2)
                solvedCube.__init__([0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0])
    
    # Finds every optimal solution to the cube in the same manner as above, this just keeps going instead of stopping after one solution
    def allOptimalSols(self):
        if self.isSolved():
            return "The cube is already solved"
        scram = copy.deepcopy(self.pieces)
        solvedCube = Cube2x2([0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0])
        moves = ['U', "U'", 'U2', 'R', "R'", 'R2', 'F', "F'", 'F2']
        algs = { 0:[''], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[] }
        checkedStates = dict()
        sols = []
        minLength = 11
        for i in range(6):
            for alg in algs[i]:
                eval('self.__init__' + str(tuple(scram)))
                self.applyAlg(alg)
                currState = tuple([tuple(piece) for piece in self.pieces])
                checkedStates[currState] = checkedStates.get(currState, alg)
                for move in moves:
                    if alg == '':
                        algs[i+1].append(move)
                    elif alg.split(' ')[-1][0] != move[0]:
                        algs[i+1].append(alg + ' ' + move)
            for alg2 in algs[i] + algs[i+1]:
                solvedCube.applyAlg(alg2)
                stateFromSolved = tuple([tuple(piece) for piece in solvedCube.pieces])
                if stateFromSolved in checkedStates:
                    if checkedStates[stateFromSolved] == '':
                        sol = inverseScramble(alg2)
                        n = len(sol.split(' '))
                        if n <= minLength:
                            minLength = n
                            sols.append(sol)
                    else:
                        sol = checkedStates[stateFromSolved] + ' ' + inverseScramble(alg2)
                        n = len(sol.split(' '))
                        if n <= minLength:
                            minLength = n
                            sols.append(sol)
                solvedCube.__init__([0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0])
        self.__init__([0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0])
        solSet = set()
        for sol in sols:
            solSet.add(sol)
        return solSet

    def __repr__(self):
        return str(self.pieces)

def solver2x2_mousePressed(app, event):
    returnToHome(app, event)
    x, y = event.x, event.y
    if x in range(50, 350):
        if y in range(260, 310):
            c = Cube2x2([0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0])
            c.applyAlg(app.scramble)
            app.sol = c.optimalSolve()
            app.allSols = None
        elif y in range(335, 385):
            c = Cube2x2([0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0])
            c.applyAlg(app.scramble)
            app.allSols = c.allOptimalSols()
            for sol in app.allSols:
                print(sol)
            app.sol = None

def solver2x2_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.background)
    canvas.create_text(app.width/2, 35, text=f'The scramble you entered was:\n{app.scramble}', font='Arial 14')
    canvas.create_rectangle(50, 260, 350, 310, fill='red')
    canvas.create_rectangle(50, 335, 350, 385, fill='orange')
    canvas.create_text(200, 285, text='Generate one optimal solution')
    canvas.create_text(200, 360, text='Generate all optimal solutions')
    if app.sol != None:
        canvas.create_text(app.width/2, 410, text=f'Solution: {app.sol}', font='Arial 12')
    elif app.allSols != None:
        s = ''
        canvas.create_text(app.width/2, 410, text='Solutions (If they don\'t fit here they\'re in the console):', anchor=N, font='Arial 12')
        for sol in app.allSols:
            s += sol + '\n'
        canvas.create_text(app.width/2, 427, text=s, anchor=N, font='Arial 12')
    drawCube2x2(app, canvas)
    drawReturnToHomeButton(app, canvas)


######################
### Move Functions ###
######################
# Each move function either moves the stickers that change when the move is made or uses other moves to reach the same state

def makeMove(app, move):
    direction = 1
    if move[-1] == '\'':
        direction = 3
    elif move[-1] == '2':
        direction = 2
    for i in range(direction):
        if len(move) > 1 and move[1] == 'w':
            eval('makeMove' + move[0:2] + '(app)')
        else:
            eval('makeMove' + move[0] + '(app)')
    if not (move[0] == 'X' or move[0] == 'Y' or move[0] == 'Z') and app.scrambleApplied:
        if not app.firstMoveApplied:
            app.firstMoveApplied = True
            app.startTime = time.time()
        app.moveCount += 1

def makeMoveR(app):
    rotateFace(app.rFace)
    ( app.fFace[0][2], app.dFace[0][2], app.bFace[0][0], app.uFace[0][2],
      app.fFace[1][2], app.dFace[1][2], app.bFace[1][0], app.uFace[1][2],
      app.fFace[2][2], app.dFace[2][2], app.bFace[2][0], app.uFace[2][2] ) = \
    ( app.dFace[0][2], app.bFace[2][0], app.uFace[2][2], app.fFace[0][2],
      app.dFace[1][2], app.bFace[1][0], app.uFace[1][2], app.fFace[1][2],
      app.dFace[2][2], app.bFace[0][0], app.uFace[0][2], app.fFace[2][2] )

def makeMoveU(app):
    rotateFace(app.uFace)
    ( app.fFace[0], app.rFace[0], app.bFace[0], app.lFace[0] ) = \
    ( app.rFace[0], app.bFace[0], app.lFace[0], app.fFace[0] )

def makeMoveF(app):
    rotateFace(app.fFace)
    ( app.uFace[2][0], app.lFace[0][2], app.dFace[0][0], app.rFace[0][0],
      app.uFace[2][1], app.lFace[1][2], app.dFace[0][1], app.rFace[1][0],
      app.uFace[2][2], app.lFace[2][2], app.dFace[0][2], app.rFace[2][0]) = \
    ( app.lFace[2][2], app.dFace[0][0], app.rFace[2][0], app.uFace[2][0],
      app.lFace[1][2], app.dFace[0][1], app.rFace[1][0], app.uFace[2][1],
      app.lFace[0][2], app.dFace[0][2], app.rFace[0][0], app.uFace[2][2] )

def makeMoveL(app):
    rotateFace(app.lFace)
    ( app.fFace[0][0], app.uFace[0][0], app.bFace[0][2], app.dFace[0][0],
      app.fFace[1][0], app.uFace[1][0], app.bFace[1][2], app.dFace[1][0],
      app.fFace[2][0], app.uFace[2][0], app.bFace[2][2], app.dFace[2][0] ) = \
    ( app.uFace[0][0], app.bFace[2][2], app.dFace[2][0], app.fFace[0][0],
      app.uFace[1][0], app.bFace[1][2], app.dFace[1][0], app.fFace[1][0],
      app.uFace[2][0], app.bFace[0][2], app.dFace[0][0], app.fFace[2][0] )

def makeMoveD(app):
    rotateFace(app.dFace)
    ( app.fFace[2], app.lFace[2], app.bFace[2], app.rFace[2] ) = \
    ( app.lFace[2], app.bFace[2], app.rFace[2], app.fFace[2] )

def makeMoveB(app):
    rotateFace(app.bFace)
    ( app.uFace[0][0], app.rFace[0][2], app.dFace[2][0], app.lFace[0][0],
      app.uFace[0][1], app.rFace[1][2], app.dFace[2][1], app.lFace[1][0],
      app.uFace[0][2], app.rFace[2][2], app.dFace[2][2], app.lFace[2][0]) = \
    ( app.rFace[0][2], app.dFace[2][2], app.lFace[0][0], app.uFace[0][2],
      app.rFace[1][2], app.dFace[2][1], app.lFace[1][0], app.uFace[0][1],
      app.rFace[2][2], app.dFace[2][0], app.lFace[2][0], app.uFace[0][0] )

def makeMoveM(app):
    ( app.fFace[0][1], app.uFace[0][1], app.bFace[0][1], app.dFace[0][1],
      app.fFace[1][1], app.uFace[1][1], app.bFace[1][1], app.dFace[1][1],
      app.fFace[2][1], app.uFace[2][1], app.bFace[2][1], app.dFace[2][1] ) = \
    ( app.uFace[0][1], app.bFace[2][1], app.dFace[2][1], app.fFace[0][1],
      app.uFace[1][1], app.bFace[1][1], app.dFace[1][1], app.fFace[1][1],
      app.uFace[2][1], app.bFace[0][1], app.dFace[0][1], app.fFace[2][1] )

def makeMoveE(app):
    app.rFace[1], app.fFace[1], app.lFace[1], app.bFace[1] = \
    app.fFace[1], app.lFace[1], app.bFace[1], app.rFace[1]

def makeMoveS(app):
    ( app.uFace[1][0], app.lFace[0][1], app.dFace[1][0], app.rFace[0][1],
      app.uFace[1][1], app.lFace[1][1], app.dFace[1][1], app.rFace[1][1],
      app.uFace[1][2], app.lFace[2][1], app.dFace[1][2], app.rFace[2][1]) = \
    ( app.lFace[2][1], app.dFace[1][0], app.rFace[2][1], app.uFace[1][0],
      app.lFace[1][1], app.dFace[1][1], app.rFace[1][1], app.uFace[1][1],
      app.lFace[0][1], app.dFace[1][2], app.rFace[0][1], app.uFace[1][2] )

def makeMoveX(app):
    makeMoveR(app)
    for i in range(3):
        makeMoveM(app)
        makeMoveL(app)

def makeMoveY(app):
    makeMoveU(app)
    for i in range(3):
        makeMoveE(app)
        makeMoveD(app)

def makeMoveZ(app):
    makeMoveF(app)
    makeMoveS(app)
    for i in range(3):
        makeMoveB(app)

def makeMoveRw(app):
    makeMoveR(app)
    for i in range(3):
        makeMoveM(app)

def makeMoveUw(app):
    makeMoveU(app)
    for i in range(3):
        makeMoveE(app)

def makeMoveFw(app):
    makeMoveF(app)
    makeMoveS(app)

def makeMoveLw(app):
    makeMoveL(app)
    makeMoveM(app)

def makeMoveDw(app):
    makeMoveD(app)
    makeMoveE(app)

def makeMoveBw(app):
    makeMoveB(app)
    for i in range(3):
        makeMoveS(app)

def rotateFace(face):
    (face[0][0], face[0][1], face[0][2], face[1][0], face[1][2], face[2][0], face[2][1], face[2][2]) =\
    (face[2][0], face[1][0], face[0][0], face[2][1], face[0][1], face[2][2], face[1][2], face[0][2])


########################
### Helper Functions ###
########################
# Various helper functions used throughout the project, not in any particular order

# CITATION: Adapted from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, row, col):
    x0 = app.leftRightMargin + col * app.cellSize
    x1 = app.leftRightMargin + (col+1) * app.cellSize
    y0 = app.topMargin + row * app.cellSize
    y1 = app.topMargin + (row+1) * app.cellSize
    return (x0, y0, x1, y1)

# CITATION: Adapted from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds2x2(app, row, col):
    x0 = app.leftRightMargin2x2 + col * app.cellSize2x2
    x1 = app.leftRightMargin2x2 + (col+1) * app.cellSize2x2
    y0 = app.topMargin2x2 + row * app.cellSize2x2
    y1 = app.topMargin2x2 + (row+1) * app.cellSize2x2
    return (x0, y0, x1, y1)

def resetCube(app):
    app.rFace = [ [app.rColor for i in range(3)] for i in range(3) ]
    app.uFace = [ [app.uColor for i in range(3)] for i in range(3) ]
    app.fFace = [ [app.fColor for i in range(3)] for i in range(3) ]
    app.lFace = [ [app.lColor for i in range(3)] for i in range(3) ]
    app.dFace = [ [app.dColor for i in range(3)] for i in range(3) ]
    app.bFace = [ [app.bColor for i in range(3)] for i in range(3) ]
    updateCube(app)

def applyScramble(app, scramble):
    for move in scramble.split(' '):
        if move[-1] == '2':
            direction = 2
        elif move[-1] == '\'':
            direction = 3
        else:
            direction = 1
        for i in range(direction):
            if len(move) > 1 and move[1] == 'w':
                eval('makeMove' + move[0] + move[1] + '(app)')
            else:
                eval('makeMove' + move[0] + '(app)')

def isCubeSolved(app):
    for r in range(3):
        for c in range(2):
            if (app.rFace[r][c] != app.rFace[r][c+1] or app.uFace[r][c] != app.uFace[r][c+1] or
                app.fFace[r][c] != app.fFace[r][c+1] or app.lFace[r][c] != app.lFace[r][c+1] or
                app.dFace[r][c] != app.dFace[r][c+1] or app.bFace[r][c] != app.bFace[r][c+1]):
                app.isCubeSolved = False
                return
    for r in range(2):
        for c in range(3):
            if (app.rFace[r][c] != app.rFace[r+1][c] or app.uFace[r][c] != app.uFace[r+1][c] or
                app.fFace[r][c] != app.fFace[r+1][c] or app.lFace[r][c] != app.lFace[r+1][c] or
                app.dFace[r][c] != app.dFace[r+1][c] or app.bFace[r][c] != app.bFace[r+1][c]):
                app.isCubeSolved = False
                return
    app.isCubeSolved = True

def resetTimer(app):
    app.timeList = '\n' + str(app.solveTime)[:5] + app.timeList
    app.moveCountList = '\n' + str(app.moveCount) + app.moveCountList
    app.solveTime = 0
    app.moveCount = 0
    app.scrambleApplied = False
    app.firstMoveApplied = False

def drawCube(app, canvas):
    for r in range(len(app.cubeNet)):
        for c in range(len(app.cubeNet[0])):
            if app.cubeNet[r][c] != '':
                x0, y0, x1, y1 = getCellBounds(app, r, c)
                canvas.create_rectangle(x0, y0, x1, y1, fill=app.cubeNet[r][c])

def drawCube2x2(app, canvas):
    for r in range(len(app.cubeNet2x2)):
        for c in range(len(app.cubeNet2x2[0])):
            if app.cubeNet2x2[r][c] != '':
                x0, y0, x1, y1 = getCellBounds2x2(app, r, c)
                canvas.create_rectangle(x0, y0+30, x1, y1+30, fill=app.cubeNet2x2[r][c])

def drawMoves(app, canvas):
    canvas.create_text(10, 10, anchor=NW, text=('Moves: ' + str(app.moveCount)))

def drawTimeList(app, canvas):
    canvas.create_text(320, 505, anchor=NE, text=('Times' + app.timeList))

def drawMoveCountList(app, canvas):
    canvas.create_text(330, 505, anchor=NW, text=('Move Count' + app.moveCountList))

def drawButtons(app, canvas):
    for i in range(len(app.buttonCoords)):
        button = app.buttonCoords[i]
        x0, y0, x1, y1 = button[0], button[1], button[2], button[3]
        canvas.create_rectangle(x0, y0, x1, y1, fill=app.buttonColors[i], outline='black', width=1.5)
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=app.buttonText[i], font='Arial 16 bold')

def drawReturnToHomeButton(app, canvas):
    canvas.create_rectangle((app.width-125)/2, app.height-50, (app.width+125)/2, app.height, fill='white')
    canvas.create_text(app.width/2, app.height-25, text='Return to Home', font='Arial 12 bold')

def drawInputButton(app, canvas):
    canvas.create_rectangle(0, app.height-50, 125, app.height, fill='white')
    canvas.create_text(125/2, app.height-25, text='Input your own cube', font='Arial 10')

def drawGoToPractice(app, canvas):
    canvas.create_rectangle((app.width-125)/2, app.height-125, (app.width+125)/2, app.height-75, fill='white')
    canvas.create_text(app.width/2, app.height-100, text='Go to practice', font='Arial 12 bold')

def generateScramble():
    moves = [ 'R', 'U', 'F', 'L', 'D', 'B' ]
    dirs = [ '', '\'', '2' ]
    scramble = ''
    for i in range(25):
        move = random.choice(moves)
        if len(scramble.split(' ')) >= 2:
            while move == scramble.split(' ')[-2][0]:
                move = random.choice(moves)
        if len(scramble.split(' ')) >= 3:
            while (move == scramble.split(' ')[-3][0] or
                   move == scramble.split(' ')[-2][0]):
                move = random.choice(moves)
        moveDir = random.choice(dirs)
        scramble = scramble + move + moveDir + ' '
    return scramble[:-1]

def inverseScramble(scr):
    scrAllUpper = ''
    for c in scr:
        if c == 'x' or c == 'y' or c == 'z':
            scrAllUpper += c.upper()
        else:
            scrAllUpper += c
    inv = ''
    for move in list(reversed(scrAllUpper.split(' '))):
        if move[-1] == '2':
            inv += move + ' '
        elif move[-1] == "'":
            inv += move[:-1] + ' '
        else:
            inv += move + "'" + ' '
    return inv[:-1]

# CITATION: From hw5
def matrixMultiply(m1,m2):
    result = [ ([0] * len(m2[0])) for i in range(len(m1)) ]
    for row in m1:
        if len(row) != len(m2):
            return None
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                result[i][j] += m1[i][k] * m2[k][j]
    return result

def drawColorButtons(app, canvas):
    for color in app.manualInputColors:
        x0, y0, x1, y1 = app.manualInputColors[color]
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black', width=2)
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=color)

def drawCube3D(app, canvas):
    colors = []
    for face in [app.uFace, app.fFace, app.rFace]:
        for row in face:
            for color in row:
                colors.append(color)
    for i in range(0, len(app.cubeCoordsIso), 4):
        x0, y0 = app.cubeCoordsIso[i][0][0]+app.width/2, app.cubeCoordsIso[i][1][0]+app.width/2
        x1, y1 = app.cubeCoordsIso[i+1][0][0]+app.width/2, app.cubeCoordsIso[i+1][1][0]+app.width/2
        x2, y2 = app.cubeCoordsIso[i+2][0][0]+app.width/2, app.cubeCoordsIso[i+2][1][0]+app.width/2
        x3, y3 = app.cubeCoordsIso[i+3][0][0]+app.width/2, app.cubeCoordsIso[i+3][1][0]+app.width/2
        canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, outline='black', fill=colors[i//4])

def drawHiddenSides(app, canvas):
    colors = []
    for face in [list(reversed(app.dFace)), [list(reversed(app.bFace[0])), list(reversed(app.bFace[1])), list(reversed(app.bFace[2]))], [list(reversed(app.lFace[0])), list(reversed(app.lFace[1])), list(reversed(app.lFace[2]))]]:
        for row in face:
            for color in row:
                colors.append(color)
    for i in range(0, len(app.hiddenSidesCoords), 4):
        x0, y0 = app.hiddenSidesCoords[i][0][0]+app.width/2, app.hiddenSidesCoords[i][1][0]+app.width/2
        x1, y1 = app.hiddenSidesCoords[i+1][0][0]+app.width/2, app.hiddenSidesCoords[i+1][1][0]+app.width/2
        x2, y2 = app.hiddenSidesCoords[i+2][0][0]+app.width/2, app.hiddenSidesCoords[i+2][1][0]+app.width/2
        x3, y3 = app.hiddenSidesCoords[i+3][0][0]+app.width/2, app.hiddenSidesCoords[i+3][1][0]+app.width/2
        canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, outline='black', fill=colors[i//4])

def drawToggle3D(app, canvas):
    canvas.create_text(app.width/2, 15, text='Press 0 to toggle between 2D and 3D', font='Arial 10')

def drawShowSides(app, canvas):
    canvas.create_text(app.width/2, 30, text='Press 1 to show the hidden sides', font='Arial 10')

def drawInstructions(app, canvas):
    canvas.create_text((app.width-125)/2/2, app.height-15, text='Press Space to\nscramble the cube', font='Arial 10', anchor=S)
    canvas.create_text((400+(app.width+125)/2)/2, app.height-15, text='Press Escape to\nreset the cube', font='Arial 10', anchor=S)

def updateCube(app):
    app.cubeNet = [ ['' for i in range(3)] + app.uFace[0] + ['' for i in range(6)],
                    ['' for i in range(3)] + app.uFace[1] + ['' for i in range(6)],
                    ['' for i in range(3)] + app.uFace[2] + ['' for i in range(6)],
                    app.lFace[0] + app.fFace[0] + app.rFace[0] + app.bFace[0],
                    app.lFace[1] + app.fFace[1] + app.rFace[1] + app.bFace[1],
                    app.lFace[2] + app.fFace[2] + app.rFace[2] + app.bFace[2],
                    ['' for i in range(3)] + app.dFace[0] + ['' for i in range(6)],
                    ['' for i in range(3)] + app.dFace[1] + ['' for i in range(6)],
                    ['' for i in range(3)] + app.dFace[2] + ['' for i in range(6)] ]
    app.cubeNet2x2 = [ ['' for i in range(2)] + [app.uFace[0][0], app.uFace[0][2]] + ['' for i in range(4)],
                       ['' for i in range(2)] + [app.uFace[2][0], app.uFace[2][2]] + ['' for i in range(4)],
                       [app.lFace[0][0], app.lFace[0][2], app.fFace[0][0], app.fFace[0][2], app.rFace[0][0], app.rFace[0][2], app.bFace[0][0], app.bFace[0][2]],
                       [app.lFace[2][0], app.lFace[2][2], app.fFace[2][0], app.fFace[2][2], app.rFace[2][0], app.rFace[2][2], app.bFace[2][0], app.bFace[2][2]],
                       ['' for i in range(2)] + [app.dFace[0][0], app.dFace[0][2]] + ['' for i in range(4)],
                       ['' for i in range(2)] + [app.dFace[2][0], app.dFace[2][2]] + ['' for i in range(4)] ]

def moveKeybinds(app, event):
    if event.key == 'q': makeMove(app, 'Z\'')
    elif event.key == 'w': makeMove(app, 'B')
    elif event.key == 'e': makeMove(app, 'L\'')
    elif event.key == 'r': makeMove(app, 'Lw\'')
    elif event.key == 't' or event.key == 'y': makeMove(app, 'X')
    elif event.key == 'u': makeMove(app, 'Rw')
    elif event.key == 'i': makeMove(app, 'R')
    elif event.key == 'o': makeMove(app, 'B\'')
    elif event.key == 'p': makeMove(app, 'Z')
    elif event.key == 'a': makeMove(app, 'Y\'')
    elif event.key == 's': makeMove(app, 'D')
    elif event.key == 'd': makeMove(app, 'L')
    elif event.key == 'f': makeMove(app, 'U\'')
    elif event.key == 'g': makeMove(app, 'F\'')
    elif event.key == 'h': makeMove(app, 'F')
    elif event.key == 'j': makeMove(app, 'U')
    elif event.key == 'k': makeMove(app, 'R\'')
    elif event.key == 'l': makeMove(app, 'D\'')
    elif event.key == ';': makeMove(app, 'Y')
    elif event.key == 'z': makeMove(app, 'Dw')
    elif event.key == 'x' or event.key == '.': makeMove(app, 'M\'')
    elif event.key == 'c': makeMove(app, 'Uw\'')
    elif event.key == 'v': makeMove(app, 'Lw')
    elif event.key == 'b' or event.key == 'n': makeMove(app, 'X\'')
    elif event.key == 'm': makeMove(app, 'Rw\'')
    elif event.key == ',': makeMove(app, 'Uw')
    elif event.key == '/': makeMove(app, 'Dw\'')
    elif event.key == '5' or event.key == '6': makeMove(app, 'M')
    elif event.key == '0': app.isoGraphics = not app.isoGraphics
    elif event.key == '1' and app.isoGraphics: app.hiddenSidesRevealed = not app.hiddenSidesRevealed

def returnToHome(app, event):
    x, y = event.x, event.y
    if x in range((app.width-125)//2, (app.width+125)//2) and y in range(app.height-50, app.height):
        app.mode = 'homescreen'
        resetCube(app)
        app.hiddenSidesRevealed = False
        app.cubeIsSolvable = True
        app.isoGraphics = False

def cubeIsSolvable(app):
    edges = getEdges(app)
    corners = getCorners(app)
    edgeSwaps, edgeFlips = edgeParity(edges, solved=[ ['white', 'blue'],   ['white', 'red'],  ['white', 'green'],  ['white', 'orange'],
                                                       ['green', 'orange'], ['green', 'red'],  ['blue', 'orange'],  ['blue', 'red'],
                                                       ['yellow', 'blue'],  ['yellow', 'red'], ['yellow', 'green'], ['yellow', 'orange'] ], swaps=0, flips=0)
    cornerSwaps, cornerTwists = cornerParity(corners, solved=[ ['white', 'blue', 'orange'],   ['white', 'red', 'blue'],  ['white', 'green', 'red'],  ['white', 'orange', 'green'],
                                                               ['yellow', 'orange', 'blue'],  ['yellow', 'blue', 'red'], ['yellow', 'red', 'green'], ['yellow', 'green', 'orange'] ], swaps=0, twists=0)
    if edgeFlips % 2 != 0 or cornerTwists%3 != 0 or (edgeSwaps+cornerSwaps)%2 != 0:
        return False
    return True

def getEdges(app):
    r, u, f, l, d, b = app.rFace, app.uFace, app.fFace, app.lFace, app.dFace, app.bFace
    ub = [u[0][1], b[0][1]]
    ur = [u[1][2], r[0][1]]
    uf = [u[2][1], f[0][1]]
    ul = [u[1][0], l[0][1]]
    fl = [f[1][0], l[1][2]]
    fr = [f[1][2], r[1][0]]
    bl = [b[1][2], l[1][0]]
    br = [b[1][0], r[1][2]]
    db = [d[2][1], b[2][1]]
    dr = [d[1][2], r[2][1]]
    df = [d[0][1], f[2][1]]
    dl = [d[1][0], l[2][1]]
    edges = [ub, ur, uf, ul, fl, fr, bl, br, db, dr, df, dl]
    return edges

def edgeParity(edges, solved, swaps, flips):
    sortedEdges = []
    for edge in solved:
        sortedEdges.append(sorted(edge))
    if edges == []:
        return swaps, flips
    else:
        if edges[0] == solved[0]:
            return edgeParity(edges[1:], solved[1:], swaps, flips)
        elif sorted(edges[0]) == sorted(solved[0]):
            return edgeParity(edges[1:], solved[1:], swaps, flips+1)
        else:
            i = sortedEdges.index(sorted(edges[0]))
            edges[0], edges[i] = edges[i], edges[0]
            return edgeParity(edges, solved, swaps+1, flips)

def getCorners(app):
    r, u, f, l, d, b = app.rFace, app.uFace, app.fFace, app.lFace, app.dFace, app.bFace
    ubl = [u[0][0], b[0][2], l[0][0]]
    urb = [u[0][2], r[0][2], b[0][0]]
    ufr = [u[2][2], f[0][2], r[0][0]]
    ulf = [u[2][0], l[0][2], f[0][0]]
    dlb = [d[2][0], l[2][0], b[2][2]]
    dbr = [d[2][2], b[2][0], r[2][2]]
    drf = [d[0][2], r[2][0], f[2][2]]
    dfl = [d[0][0], f[2][0], l[2][2]]
    corners = [ubl, urb, ufr, ulf, dlb, dbr, drf, dfl]
    return corners

def cornerParity(corners, solved, swaps, twists):
    sortedCorners = []
    for corner in solved:
        sortedCorners.append(sorted(corner))
    if corners == []:
        return swaps, twists
    else:
        if corners[0] == solved[0]:
            return cornerParity(corners[1:], solved[1:], swaps, twists)
        elif sorted(corners[0]) == sorted(solved[0]):
            if 'white' in corners[0]:
                return cornerParity(corners[1:], solved[1:], swaps, twists+corners[0].index('white'))
            else:
                return cornerParity(corners[1:], solved[1:], swaps, twists+corners[0].index('yellow'))
        else:
            i = sortedCorners.index(sorted(corners[0]))
            corners[0], corners[i] = corners[i], corners[0]
            return cornerParity(corners, solved, swaps+1, twists)

def stickersAreValid(app):
    stickers = [i for row in app.cubeNet for i in row]
    return stickers.count('white') == stickers.count('green') == stickers.count('red') == stickers.count('blue') == stickers.count('orange') == stickers.count('yellow') == 9


runApp(width=400, height=700)