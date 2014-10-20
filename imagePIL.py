from PIL import Image
from os import listdir

enemyA_images = listdir("Images/Enemies/EnemyA")
enemyA_images = ["Images/Enemies/EnemyA/{0}".format(i) for i in enemyA_images if not i.startswith('.')]
enemyB_images = listdir("Images/Enemies/EnemyB")
enemyB_images = ["Images/Enemies/EnemyB/{0}".format(i) for i in enemyB_images if not i.startswith('.')]

for image in enemyA_images:	
	img = Image.open(image)
	datas = img.getdata()

	newData = []
	for item in datas:
	    if item[0] == 255 and item[1] == 255 and item[2] == 255:
	        newData.append((255, 255, 255, 0))
	    else:
	        newData.append(item)

	img.putdata(newData)
	img.save(image, "BMP")