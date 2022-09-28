from math import floor
from tkinter import *
from time import sleep
from random import randint
from threading import Thread, Lock
from collections import deque
import pygame

root = Tk()
root.title("Elevator Boss")
root.geometry("800x1200")
root.configure(bg='#fde7b5')
root.resizable(False, False)

InputLock = Lock()

MoveLock = Lock()

running = True
floorData = []  # queue with all floor requests
ElevatorY = 1120


def InputGeneration():
    global running
    while True:
        randTime = randint(1, 3)
        sleep(randTime)
        if not running:
            continue
        activeRequest = randint(1, 15)
        nextStop = (15-activeRequest)*80

        InputLock.acquire()
        floorData.append(nextStop)
        print(f"New Requets: {activeRequest}")
        InputLock.release()


def createElevatorWidget():
    MainCanvas.pack(side=RIGHT)

    for floor in range(1, 16):
        bgcolor = '#45b6d4' if floor % 2 else '#abdbe3'
        MainCanvas.create_rectangle(
            0, 0 + 80*(floor-1), 550, 80+80*floor, fill=bgcolor)  # Floor container
        MainCanvas.create_text(60, 30 + 80*(floor-1), fill='black', text='Floor ' + str(
            16-floor), font="Times 20 italic bold")  # Floor number text
        MainCanvas.create_text(60, 60 + 80*(floor-1), fill='black',
                               text='waiting: 5', font="Times 12 italic bold")
        MainCanvas.create_line(125, 80*(floor-1), 125, 80*(floor))


def moveElevator():
    global ElevatorY
    global floorData
    global running
    while True:
        if not floorData or not running:
            continue

        InputLock.acquire()
        nextFloorCoords = floorData.pop(0)
        InputLock.release()
        Yoffset = (nextFloorCoords - ElevatorY)/10
        Yshift = -10 if Yoffset < 0 else 10

        for k in range(int(abs(Yoffset))):
            if (ElevatorY in floorData):
                floorData = [
                    floorCords for floorCords in floorData if floorCords != ElevatorY]
                sleep(1)
            sleep(0.025)
            MainCanvas.move(Elevator, 0, Yshift)
            MainCanvas.update()
            ElevatorY += Yshift
            CurrDisplayFloor.set(f'Floor {floor(15- ElevatorY/80)}')
            if not running:
                print('Not running')
                print(f'Elevator Y: {ElevatorY}')
                break
        sleep(1)

# Main starts


TitleFrame = Frame(root, height=450, width=200, bg='#fde7b5')
TitleFrame.pack(side=LEFT)
TitleFrame.pack_propagate(0)

TitleLabel = Label(TitleFrame, text="Isaiah's \nBossman \nElevator", font=(
    'Arial', 24), borderwidth=2, relief='solid', width=8, height=3, bg='#fde7b5')
TitleLabel.pack(side=TOP)

CurrDisplayFloor = StringVar(value='Floor 1')
CurrFloorDisplay = Label(TitleFrame, textvariable=CurrDisplayFloor, font=(
    'Arial', 24), borderwidth=2, relief='solid', width=8, height=3, bg='#fde7b5')
CurrFloorDisplay.pack(side=BOTTOM)

MainCanvas = Canvas(root, bg='purple', width=550, height=1200,
                    bd=0, highlightthickness=0, relief='ridge')

pygame.mixer.init()
pygame.mixer.music.load("theelevatorbossanova.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.01)

createElevatorWidget()

Elevator = MainCanvas.create_rectangle(
    150, 1120, 527, 1200, fill='red', outline="")

randomNumThread = Thread(target=InputGeneration)
randomNumThread.daemon = True
randomNumThread.start()

ElevaterMovement = Thread(target=moveElevator)
ElevaterMovement.daemon = True
ElevaterMovement.start()

root.mainloop()
