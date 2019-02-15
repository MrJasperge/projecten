#!/usr/bin/env python3
# This is a game of BlackJack using python 3.5.2 and json
# Made by Jasper Kooij 15/2/19
# student number s2164299

import random
import json
from datetime import datetime

random.seed(datetime.now())

# open json file for statistics
stats = open("stats.json", "r+")
data = json.load(stats)

# deck, which gets changed during the course of the game
deckfull = [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6
			,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10
			,"J","J","J","J","Q","Q","Q","Q"
			,"K","K","K","K","A","A","A","A"]

deck = deckfull

# hands of player and dealer begin empty
playerhand = []
dealerhand = []

# global variable, when set to true, the game is over
gameOver = False
win = 0


# determines the winner of the game, when both
# the player score and the dealer score are < 21
def endGame():
	global win
	global gameOver
	pscore = getPlayerScore()
	dscore = getDealerScore()
	if pscore > dscore:
		win = 1
		print("Congrats, you won!")
	elif pscore == dscore:
		win = 2
		print("Gelijkspel!")
	elif pscore < dscore:
		win = 0
		print("Helaas, je hebt verloren!")
	gameOver = True


# functions regarding the player's turn

# adds a card from the deck to the player's hand
def getPlayerCard():
	r= random.randint(0,len(deck))
	card = deck[r-1]
	playerhand.append(card)
	deck.pop(r-1)

# returns player score
def getPlayerScore():
	score = 0
	for i in playerhand:
		if i == "J" or i == "Q" or i == "K":
			score += 10
		elif i == "A":
			score += 1
		else:
			score += i
	return score

# prints contents and score of hand of player
# also ends game if score >= 21
def printPlayerHand():
	global win
	global gameOver
	score = getPlayerScore()
	print(playerhand, score)
	if (score > 21):
		win = 0
		print("Game Over!")
		gameOver = True
	elif (score == 21):
		win = 3
		print("Blackjack! You won")
		gameOver = True


# functions regarding the dealer's turn

# adds a card to dealer's hand
def getDealerCard():
	r = random.randint(0, len(deck))
	card = deck[r-1]
	dealerhand.append(card)
	deck.pop(r-1)

# returns score of dealer's hand
def getDealerScore():
	dealerscore = 0
	for i in dealerhand:
		if i == "J" or i == "Q" or i == "K":
			dealerscore += 10
		elif i == "A":
			dealerscore += 1
		else:
			dealerscore += i	
	return dealerscore

# prints content and score of hand of dealer
def printDealerHand():
	score = getDealerScore()
	print("Dealer: ", dealerhand, score)

# dealer's turn, if dealerscore < 17, get another card
def dealer():
	global win
	global gameOver
	while getDealerScore() < 17:
		getDealerCard()
	if getDealerScore() > 21:
		printDealerHand()
		print("Congrats, you won!")
		win = 1
		gameOver = True
	else:
		printDealerHand()
		endGame()


# functions regarding statistics of games

# prints statistics of previous games
def printStatistics():
	print("wins:", data['wins'])
	print("losses:", data['losses'])
	print("draws:", data['draws'])
	print("games:", data['games'])

# saves statistics of game
def saveStats():
	global win
	data['games'] +=1
	if win == 1:
		data['wins'] += 1
	if win == 3:
		data['wins'] += 1
		data['blackjacks'] += 1
	if win == 2:
		data['draws'] += 1
	if win == 0:
		data['losses'] += 1
	stats.seek(0)
	json.dump(data, stats, indent=4)
	stats.truncate()

# here follow the menus present in the game

# main menu before game
def mainMenu():
	print("Welcome to BlackJack!")
	print("[P]lay game, check [s]tats, [q]uit")
	snap = False
	while not snap:
		optie = input()
		if optie == "p":
			snap = True
			game()
		elif optie == "s":
			snap = True
			printStatistics()
		elif optie == "q":
			snap = True
			print("Till next time!")
		else:
			print("Come again?")

# menu during game
def menu():
	global gameOver
	print("Opties: [q]uit, Get [c]ard, [p]ass")
	optie = input()
	if optie == "q":
		gameOver = True
		print("Quitting")
	elif optie == "c":
		getPlayerCard()
		printPlayerHand()
	elif optie == "p":
		print("pass")
		dealer()

# menu after game
def endMenu():
	global deckfull, deck, playerhand, dealerhand, gameOver
	print("Do you want to play another game?")
	print("[y]es, [n]o")
	optie = input()
	if optie == "y":
		deckfull = deck
		playerhand = []
		dealerhand = []
		gameOver = False
		game()

# main function of game
def game():
	global gameOver
	for i in range(2):
		getPlayerCard()
		getDealerCard()
	printPlayerHand()
	while not gameOver:
		menu()
	saveStats()
	endMenu()

# executes beginning of game
mainMenu()

