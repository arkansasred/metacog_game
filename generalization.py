from psychopy import visual, core, event
from os import listdir, path, mkdir
from itertools import product, permutations, izip_longest
from random import shuffle



SUBJECT = raw_input("Subject Number: ")
def checkData(SUBJECT):
    if path.exists("Subject %s/Generalization"%SUBJECT):
        answer = raw_input("Data already exists for Subject %s, would you like to erase the data and continue? Y/N: "%SUBJECT)
        if answer == "N":
            SUBJECT = raw_input ("Subject Number:")
            return checkData(SUBJECT)
        elif answer == "Y":
            pass
        else:
            checkData(SUBJECT)
checkData(SUBJECT)
"""make directory for subject if it doesn't already exist"""
if not path.exists("Subject %s/Generalization"%SUBJECT):
	mkdir("Subject %s/Generalization"%SUBJECT)

win = visual.Window(monitor="testMonitor", units="deg", allowGUI=False, fullscr = True)
intro = visual.TextStim(win, text="You will be presented with a series of aliens, please use 'Space' and 'Enter' to indicate whether you would 'Shoot' or 'Capture' the Aliens. Press Space to begin.", wrapWidth=20, alignHoriz="center")

question = visual.TextStim(win, text="Capture or Shoot?", color='Black', pos=(0,8), wrapWidth=20)
answer = visual.TextStim(win, text="Space								Enter", color='Black', pos=(0,-2), wrapWidth=20, bold = True)
reminder = visual.TextStim(win,text="Capture 							  	Shoot", color='Black', pos=(0,0),wrapWidth=20, height = 0.9)


confidenceQuestion = visual.TextStim(win, text="How confident are you in your judgment", color = 'Black', pos = (0,4), wrapWidth=20)
confidenceResponse = visual.TextStim(win, text="1			2	 		3			4			5", color='Black', pos=(0,-4), wrapWidth=20)
confidenceReminder = visual.TextStim(win, text="Not at all Confident 					 Very Confident", color = 'Black', pos=(0,0), wrapWidth=40)

fixation = visual.TextStim(win,text="+", pos=(0,0))
fixation.size = 2


eachEnemy = 4  #total number of times they see each enemy
enemyATypes = listdir("Images/Enemies/EnemyA")
enemyA = ["Images/Enemies/EnemyA/{0}".format(i) for i in enemyATypes if not i.startswith('.')]
enemyA = [visual.ImageStim(win, A, pos=(0,0), size=(4,4), units="deg", name=A[-7:-4]) for A in enemyA]
enemyBTypes = listdir("Images/Enemies/EnemyB")
enemyB = ["Images/Enemies/EnemyB/{0}".format(i) for i in enemyBTypes if not i.startswith('.')]
enemyB = [visual.ImageStim(win, B, pos=(0,0), size=(4,4), units="deg", name=B[-7:-4]) for B in enemyB]
enemies = enemyA*eachEnemy+enemyB*eachEnemy
shuffle(enemies)
shuffle(enemies)

confidenceRatings=[]
alienResponses= []
alienTypes = []
RTs = []

familiarityRankings = open("Subject %s/Generalization/responses.txt"%SUBJECT, "w")

newPair = False
aliens = False
start = True
confidence = False

t = core.Clock()

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
		image = enemies.pop()
		alien = image
		alienType = alien.name
		newPair = False
		aliens = True

	elif aliens and not newPair and not confidence:
		t.reset()
		alien.draw()
		question.draw()
		answer.draw()
		reminder.draw()
		win.flip()
		responseKeys = event.waitKeys(keyList=['space','return'])
		if len(responseKeys)>0:
			RT = t.getTime()
			RTs.append(str(RT))
			alienTypes.append(str(alienType))
			alienResponse = responseKeys.pop()
			alienResponses.append(str(alienResponse))
			"""if len(enemyCombinations)==0:
				for response in responses:
					familiarityRankings.write("%s \n"%response)
				break"""
			confidence = True
			aliens = False
			event.clearEvents()

	elif confidence and not newPair and not aliens:
		confidenceReminder.draw()
		confidenceQuestion.draw()
		confidenceResponse.draw()
		win.flip()
		#added this pause in case participant presses another key accidentally immediately following shoot/capture response
		core.wait(.25)
		responseKeys = event.waitKeys(keyList=['1','2','3','4','5'])
		if len(responseKeys)>0:
			confidenceRating = (responseKeys.pop())
			confidenceRatings.append(str(confidenceRating))
			if len(enemies)==0:
				break
			confidence = False
			newPair = True
		event.clearEvents()


#cleanup

for theType, response, rating, RT in izip_longest(alienTypes, alienResponses, confidenceRatings, RTs):
	familiarityRankings.write(theType+','+response+','+rating + ',' + RT + '\n')
familiarityRankings.close()
win.close()
core.quit()