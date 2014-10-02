from psychopy import visual, core, event
from os import listdir, path, mkdir
from itertools import product, permutations
from random import shuffle

SUBJECT = raw_input("Subject Number: ")
def checkData(SUBJECT):
    if path.exists("Subject %s"%SUBJECT):
        answer = raw_input("Data already exists for Subject %s, would you like to erase the data and continue? Y/N: "%SUBJECT)
        if answer == "N":
            SUBJECT = raw_input ("Subject Number:")
            checkData(SUBJECT)
        elif answer == "Y":
            pass
        else:
            checkData(SUBJECT)
checkData(SUBJECT)
"""make directory for subject if it doesn't already exist"""
if not path.exists("Subject %s"%SUBJECT):
    mkdir("Subject %s"%SUBJECT)

win = visual.Window(monitor="testMonitor", units="deg", fullscr=True, allowGUI=False)

intro = visual.TextStim(win, text="Thanks for participating! You will be presented with a series of pairs of blue aliens. After seeing each pair, please use keys 1-5 to rate the similarity of the aliens to eachother, with '1' being 'not at all similar' and '5' being 'very similar'.  Press any key to begin", wrapWidth=20)

question = visual.TextStim(win, text="How similar do these Aliens appear to you?", color='Black', pos=(0,-5), wrapWidth=20)
answer = visual.TextStim(win, text="1 	     2 	     3 	     4 	     5", color='Black', pos=(0,-9), wrapWidth=20)

fixation = visual.TextStim(win,text="+", pos=(0,0))
fixation.size = 2

enemyATypes = listdir("Images/Enemies/EnemyA")
enemyA = ["Images/Enemies/EnemyA/{0}".format(i) for i in enemyATypes if not i.startswith('.')]
enemyA1 = [visual.SimpleImageStim(win, A, pos=(-10,2), name=A[-7:-4]) for A in enemyA]
enemyA2 = [visual.SimpleImageStim(win, A, pos=(10,2), name=A[-7:-4]) for A in enemyA]
enemyBTypes = listdir("Images/Enemies/EnemyB")
enemyB = ["Images/Enemies/EnemyB/{0}".format(i) for i in enemyBTypes if not i.startswith('.')]
enemyB1 = [visual.SimpleImageStim(win, B, pos=(10,2), name=B[-7:-4]) for B in enemyB]
enemyB2 = [visual.SimpleImageStim(win, B, pos=(-10,2), name=B[-7:-4]) for B in enemyB]

enemyCombinations = list(product(enemyA1,enemyB1)) + list(product(enemyA1,enemyA2)) + list(product(enemyB1,enemyB2))
enemyCombinations = filter(lambda x: x[0].name!=x[1].name, enemyCombinations)
shuffle(enemyCombinations)
shuffle(enemyCombinations)
responses = []

familiarityRankings = open("Subject %s/rankings2.txt"%SUBJECT, "w")

newPair = False
aliens = False
response = False
start = True

while True:

	if start:
		intro.draw()
		win.flip()
		if len(event.waitKeys())>0:
			start = False
			newPair = True

	if newPair:
		fixation.draw()
		win.flip()
		core.wait(1.5)
		images = enemyCombinations.pop()
		alien1 = images[0]
		alien1Type = alien1.name
		alien2 = images[1]
		alien2Type = alien2.name
		newPair = False
		aliens = True

	elif aliens and not newPair:
		alien1.draw()
		alien2.draw()
		question.draw()
		answer.draw()
		win.flip()
		responseKeys = event.waitKeys(keyList=['1','2','3','4','5'])
		if len(responseKeys)>0:
			response = (alien1Type, alien2Type, responseKeys.pop())
			responses.append(str(response))
			if len(enemyCombinations)==0:
				for response in responses:
					familiarityRankings.write("%s \n"%response)
				break
			newPair = True
		event.clearEvents()

#cleanup
familiarityRankings.close()
win.close()
core.quit()
