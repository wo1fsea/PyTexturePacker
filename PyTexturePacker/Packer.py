import random
import math


def cutRect(mainRect, subRect):
	mainL, mainT, mainR, mainB = mainRect
	subL, subT, subR, subB = subRect

	if mainB < subT or mainL > subR or mainR < subL or mainT > subB:
		return (mainRect,)

	subL = mainL if subL < mainL else subL
	subT = mainT if subT < mainT else subT
	subR = mainR if subR > mainR else subR
	subB = mainB if subB > mainB else subB

	L = (mainT, mainL, mainB, subL) if mainL < subL else None
	T = (mainT, mainL, subT, mainR) if mainT < subT else None
	R = (mainT, subR, mainB, mainR) if mainR > subR else None
	B = (subB, mainL, mainB, mainR) if mainB > subB else None

	return filter(lambda x: x, (L, T, R, B))


def isInRect(mainRect, subRect):
	mainL, mainT, mainR, mainB = mainRect
	subL, subT, subR, subB = subRect

	return mainL <= subL and mainT <= subT and mainR >= subR and mainB >= subB

def rank():
	pass

def expand(maxRects, cur):
	pass

def selectBest(maxRectsList, img):
	imgW, imgH = img
	for i, maxRect in enumerate(maxRectsList):
		w, h = maxRect[2] - maxRect[0], maxRect[3] - maxRect[1]
		if w >= imgW and h >= imgH:
			return i
	return -1

def maxRectsBinPack(maxRect, imgs):
	maxRectsList = [maxRect]
	_imgs = []

	for img in imgs:
		index = selectBest(maxRectsList, img)

		if index == -1:
			print("Can't not fit.")
			return

		x, y = maxRectsList[index][:2]
		w, h = img
		imgRect = (x, y, x+w, y+h)
		_imgs.append(imgRect)

		_maxRectsList = []
		for maxRect in maxRectsList:
			_maxRectsList.extend(cutRect(maxRect, imgRect))

		maxRectsList = _maxRectsList

	return maxRectsList, _imgs



def genRectData():
	return (random.randint(0,100), random.randint(0, 100))


def main():
	a = (0,0, 100,100)
	b = ((50, 50), (50, 100), (40,40))
	print( maxRectsBinPack(a, b)[1])

if __name__ == '__main__':
	main()