# bot.py
import os
import discord
import datetime
import calendar
from discord.ext import commands
from dotenv import load_dotenv
from math import ceil
from discord.ext.commands import CommandNotFound
import csv
import pytz
from pytz import timezone
from discord.ext import tasks, commands
import aiohttp
import random

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=["!",'?'])

#flag to check if corey has changed hands
changed = False

#A list of all the channels in the discord
channel = []

#this is a dictionary of all the people who I know is part of the schedule
dictionary = {'cathy': '443813095622705152','anthony': '133779065600475137', 'henry': '139598054373195776', 'yeff': '155755250228264960','wendy': '411300301174341653','jihoon': '77268822075125760', 'matt': '173502986448797696','pedro':'177602897381556224', 'jon': '77186511736410112', 'christine':'434507044905680898'}
weekDay = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}

#URL for the pedro command
url = "https://finnhub.io/api/v1/quote?token="+os.getenv('FINNHUB_TOKEN')
randUrl = "https://finnhub.io/api/v1/stock/symbol?exchange=US&token="+os.getenv('FINNHUB_TOKEN')

#looks for the day and week number 
def findDay(date):
	today = datetime.datetime.strptime(date, '%d %m %Y').weekday()+1
	return(today)

def week_number_of_month(date_value):
	firstDay = date_value.replace(day=1)
	dom = date_value.day
	adjustedDom = dom + firstDay.weekday()
	num = int(ceil((adjustedDom/7.0)))

	if num==5:
		num=1

	return num
    # return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)

def setPerson(time):
	peep = " "
	dayNum = findDay(loc_dt.strftime("%d %m %Y"))
	weekNum = week_number_of_month(loc_dt.date())-1

	#reads the csv file of the schedule
	with open('schedule.csv') as file:
		csvFile = csv.reader(file, delimiter=',')
		header= next(csvFile)
		if header != None:
			for i, row in enumerate(csvFile):
				if i==weekNum:
					peep = row[dayNum]
	return peep

eastern=timezone("US/Eastern")
loc_dt = eastern.localize(datetime.datetime.now())
# print(loc_dt)

person = " "

@bot.command(brief="Adds and removes task from the todo list")
async def todo(ctx, *, msg=""):
	tasks = []
	msg = msg.split(" ")
	if ctx.message.author.id == 173502986448797696:
		if msg[0] == "add" or msg[0] =="a":
			try:
				f = open("todo.txt", mode="a")
				f.write(msg[1] + "\n")
				f.close()
				await ctx.channel.send(msg[1] + " has been added to the todo list")
			except:
				print("Something went wrong with adding, it'll be fixed")
		elif msg[0] == "remove" or msg[0] == "r":
			try:
				f=open("todo.txt", mode="r")
				lines = f.readlines()
				f.close()
				newFile = open("todo.txt", "w")
				for line in lines:
					if line.strip("\n") != msg[1]:
						newFile.write(line)
				newFile.close()
				await ctx.channel.send("Deleted the command")
			except:
				await ctx.channel.send("Unable to find the command")
		elif msg[0]=="":
			f=open("todo.txt", "r")
			for word in f.read().splitlines():
				tasks.append(word)
			await ctx.channel.send("Master would like to do <@" + str(ctx.message.author.id) + ">'s mother but he also plans to implement the following commands: \n" + (", ".join(tasks)))
	else:
		await ctx.send("You do not own this bot!")
	# user = str(ctx.message.author.id)
	# await ctx.channel.send("Master would like to do <@" + user + ">'s mother but he also plans to implement the following commands: \n explain, pedro, todo")

@bot.command(brief="Shows whose day it is with Corey (aka Frodo's Other Sandwich)")
async def today(ctx):

	global person
	global loc_dt

	loc_dt = eastern.localize(datetime.datetime.now())

	person = setPerson(loc_dt)

	beginning = "It is "
	end = "'s day today"

	if person in dictionary.keys():
		await ctx.channel.send(beginning + "<@" + dictionary.get(person) + ">" + end)
	else:
		await ctx.channel.send(beginning + person + end)

@bot.command()
async def week(ctx):
	global weekNum

	weekNum = week_number_of_month(loc_dt.date())-1
	await ctx.channel.send('It is week ' + str(weekNum+1))

@bot.command(brief='Shows what day of the week it is')
async def day(ctx):
    global dayNum
    global loc_dt
    weekDay = loc_dt.strftime("%A")
    await ctx.channel.send("Today is " + weekDay + " my dudes") 

@bot.command(brief="Returns the schedule for who's day it is with Corey (aka Frodo's Other Sandwich")
async def schedule(ctx):
	await ctx.channel.send(file=discord.File('Corey_Schedule.png'))

@bot.command(brief="Changes the who's day it is with Corey")
async def change(ctx, newPerson):

	global changed
	global person

	if changed == False:
		changed = True
		await ctx.channel.send("It was <@" + dictionary.get(person) + ">'s day, but it's " + newPerson + "'s day now")
	else:
		await ctx.channel.send("The day has been changed, you cannot change it again")

@bot.command(pass_context=True, aliases=['changeback'], brief="Changes back the day to the original person on the schedule")
async def changeBack(ctx):

	global changed
	global person

	if changed:
		await ctx.channel.send("The day has been changed back to <@" + dictionary.get(person) + ">")
	else:
		await ctx.channel.send("You can't change back if the day hasn't been changed")

@bot.command(pass_context=True, aliases=['Yeff'], brief="Calling Yeff (aka Jeff)")
async def yeff(ctx):
	await ctx.channel.send("<@155755250228264960>")

@bot.command(brief="Shows who's the master")
async def master(ctx):
	await ctx.channel.send("<@173502986448797696> is the master, nobody goes against the master")

@bot.command(pass_context=True, aliases=['dad', 'Dad', 'Daddy'], brief="Shows who's the daddy in this server?")
async def daddy(ctx):
	await ctx.channel.send("<@139598054373195776> is <@443813095622705152>'s daddy")

@bot.command(pass_context=True, aliases=['hubby'], brief="Shows who's the husband of this server?")
async def husband(ctx):
	await ctx.channel.send("<@133779065600475137>")

@bot.command(pass_context=True, aliases=['girlfriend'], brief="Show's who's the girlfriend and the mother in this server... Different from the gf command")
async def mother(ctx):
	await ctx.channel.send("<@411300301174341653> is <@225359460812455936>'s girlfriend and <@443813095622705152>'s mother")

@bot.command(brief="Show's who's the gf in the server... Different from the mother/girlfriend command")
async def gf(ctx):
	if(person=="cathy"):
		await ctx.channel.send("Corey loves <@443813095622705152> the most")
	else:
		await ctx.channel.send("<@443813095622705152> is <@225359460812455936>'s gf")

@bot.command(pass_context=True, aliases=['bae','corbae','coreybae','Corey'], brief="We should all know who's Corey, but just in case")
async def corey(ctx):
	await ctx.channel.send("All hail the great <@225359460812455936> may he forever live a prosperous life")

@bot.command(pass_context=True, alisases=['freecorey'], brief="Reveals the non-believers in the discord")
async def freeCorey(ctx):
	await ctx.channel.send("The following want to free <@225359460812455936>: <@483463488929529867> and <@184424945768464384>")

@bot.command(brief="Shows the steps needed to be taken to request a new command")
async def request(ctx):
	await ctx.channel.send("Please send submit your command request and a description of it into the following container")
	await ctx.channel.send(file = discord.File('fireCan.jpg'))

@bot.command(pass_context=True, aliases=['punish'], brief="Punishes Cathy")
async def reprimand(ctx):
	await ctx.channel.send("Go practice more piano! <@" + dictionary.get('cathy')+">")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		print("Command not found")

@bot.command(brief="Show's who's the real baby in this server")
async def baby(ctx):
	await ctx.channel.send("<@" + dictionary.get('cathy') + '> thinks she is the baby when <@' + dictionary.get('matt') +'> is the real baby for his name is Babyeater58')


@bot.command(brief="This is mom, different from mother")
async def mom(ctx):
	await ctx.channel.send("<@"+dictionary.get("christine")+">is <@"+dictionary.get('cathy')+">'s mom")

@bot.command(brief="Shuts down the bot")
async def shutdown(ctx):
	if ctx.message.author.id == 173502986448797696:
		print("Shutting Down")
		try:
			await ctx.send("Shutting Down.... Bye bye")
			await ctx.bot.logout()
		except:
			print("Environment Error")
			ctx.bot.clear()
	else:
		await ctx.send("You do not own this bot!")

# price search
@bot.command(brief="Dedicated command for pedro")
async def pedro(ctx, ticker=None):
	global url
	global randUrl

	session = aiohttp.ClientSession()

	if(ticker==None):
		res = await session.get(randUrl)
		json = await res.json()
		company = random.randint(0, len(json))
		res2 = await session.get(url+"&symbol="+json[company]['symbol'].upper())
		res2Price = await res2.json()
		await session.close()
		# print(res2Price['c'])
		value = '$'+str(res2Price['c'])
		await ctx.channel.send("Here's a random company for you to throw money at: ")
		await ctx.channel.send(json[company]['symbol']+": " + json[company]['description'])
		await ctx.channel.send("The current price of it is: " + value)
	else:
		res = await session.get(url+"&symbol="+ticker.upper())
		json = await res.json()
		price = json['c']
		await session.close()
		value = "$"+str(price)
		await ctx.channel.send("The current price of " + ticker.upper() + " is:")
		await ctx.channel.send(value)


@tasks.loop(hours=1.0)
async def counter():
	global channel
	global changed
	global dictionary
	global person

	loc_dt = eastern.localize(datetime.datetime.now())
	now = loc_dt.strftime("%H")
	beginning = "It is "
	end = "'s day today"

	# person = setPerson(loc_dt)
	dayNum = findDay(loc_dt.strftime("%d %m %Y"))
	weekNum = week_number_of_month(loc_dt.date())-1

	#reads the csv file of the schedule
	with open('schedule.csv') as file:
		csvFile = csv.reader(file, delimiter=',')
		header= next(csvFile)
		if header != None:
			for i, row in enumerate(csvFile):
				if i==weekNum:
					person = row[dayNum]

	print(loc_dt)

	for server in bot.guilds:
		for text in server.text_channels:
			if not text.id in channel:
				channel.append(text.id)
			else:
				continue

	if len(channel) !=0:
		chan = bot.get_channel(channel[0])
		if now == "10":
			print("Hour " + now)
			print(loc_dt)
			changed = False
			if person in dictionary.keys():
				await chan.send(beginning + "<@" + dictionary.get(person) + ">" + end)
			else:
				await chan.send(beginning + person + end)
		else:
			print(dictionary.get(person))

# @counter.before_loop
# async def counterBefore():
# 	global 

#counter.start()

print("Running")
bot.run(TOKEN)

