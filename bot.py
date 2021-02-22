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

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

# client = discord.Client()

bot = commands.Bot(command_prefix=["!",'?'])

#flag to check if corey has changed hands
changed = False

#this is a dictionary of all the people who I know is part of the schedule
dictionary = {'cathy': '443813095622705152','anthony': '133779065600475137', 'henry': '139598054373195776', 'yeff': '155755250228264960','wendy': '411300301174341653','jihoon': '77268822075125760', 'matt': '173502986448797696','pedro':'177602897381556224', 'jon': '77186511736410112'}
weekDay = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}

#looks for the day and week number 
def findDay(date):
	today = datetime.datetime.strptime(date, '%d %m %Y').weekday()+1
	return(today)

def week_number_of_month(date_value):
	firstDay = date_value.replace(day=1)
	dom = date_value.day
	adjustedDom = dom + firstDay.weekday()

	return int(ceil((adjustedDom/7.0)))
    # return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)

eastern=timezone("US/Eastern")
loc_dt = eastern.localize(datetime.datetime.now())
# print(loc_dt)

person = " "
weekNum = week_number_of_month(loc_dt.date())
dayNum = findDay(loc_dt.strftime("%d %m %Y"))

# print("week " + str(weekNum))
# print("day " + str(dayNum))

#reads the csv file of the schedule
with open('schedule.csv') as file:
	csvFile = csv.reader(file, delimiter=',')
	header= next(csvFile)
	if header != None:
		for i, row in enumerate(csvFile):
			# print(row[dayNum])
			if i==weekNum:
				# print(row[dayNum])
				person = row[dayNum]

@bot.command(brief="This is a list of commands that are currently planned/in production")
async def todo(ctx):
	user = str(ctx.message.author.id)
	await ctx.channel.send("Master would like to do <@" + user + ">'s mother but he also plans to implement the following commands: \n week, day, explain, pedro")

@bot.command(brief="Shows who's day it is with Corey (aka Frodo's Other Sandwich)")
async def today(ctx):

	global person
	global loc_dt

	dayNum = findDay(loc_dt.strftime("%d %m %Y"))
	weekNum = week_number_of_month(loc_dt.date())

	#reads the csv file of the schedule
	with open('schedule.csv') as file:
		csvFile = csv.reader(file, delimiter=',')
		header= next(csvFile)
		if header != None:
			for i, row in enumerate(csvFile):
				if i==weekNum:
					person = row[dayNum]

	beginning = "It is "
	end = "'s day today"

	if person in dictionary.keys():
		await ctx.channel.send(beginning + "<@" + dictionary.get(person) + ">" + end)
	else:
		await ctx.channel.send(beginning + person + end)


@bot.command()
async def week(ctx):
	global weekNum

	# await ctx.channel.send('It is week ' + str(weekNum))
	# await ctx.channel.send("Here's this week's schedule: ")
	# await ctx.channel.send(df.iloc[weekNum-1])
	await ctx.channel.send("Master is a lazy and hasn't fixed this command")

@bot.command(brief='Shows what day of the week it is')
async def day(ctx):
    global dayNum 
    weekDay = datetime.datetime.now().strftime("%A")
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

@bot.command(brief="Announces when Corey is live on Twitch.tv")
async def live(ctx):
	await ctx.channel.send("@ everyone Corey, the great god, is streaming so hop in and say hi! www.twitch.tv/spareboredom")

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

@bot.command()
async def status(ctx):
	print(ctx.author.activities)
	await ctx.channel.send(ctx.author.acitivites)

@bot.command(brief="Show's who's the real baby in this server")
async def baby(ctx):
	await ctx.channel.send("<@" + dictionary.get('cathy') + '> thinks she is the baby when <@' + dictionary.get('matt') +'> is the real baby for his name is Babyeater58')

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




print("Running")
bot.run(TOKEN)
