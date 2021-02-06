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

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

# client = discord.Client()

bot = commands.Bot(command_prefix=["!",'?'])

#flag to check if corey has changed hands
changed = False

#this is a dictionary of all the people who I know is part of the schedule
dictionary = {'cathy': '443813095622705152','anthony': '133779065600475137', 'henry': '139598054373195776', 'yeff': '155755250228264960','wendy': '411300301174341653','jihoon': '77268822075125760', 'matt': '173502986448797696','pedro':'177602897381556224', 'jon': '77186511736410112'}
weekDay = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}

def findDay(date):
	today = datetime.datetime.strptime(date, '%d %m %Y').weekday()+1
	return(today)

def week_number_of_month(date_value):
	firstDay = date_value.replace(day=1)
	dom = date_value.day
	adjustedDom = dom + firstDay.weekday()

	return int(ceil((adjustedDom/7.0)-1.0))
    # return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)

person = " "
dayNum = findDay(datetime.date.today().strftime("%d %m %Y"))
weekNum = week_number_of_month(datetime.datetime.today().date())

print("week " + str(weekNum))
print("day " + str(dayNum))

#reads the csv file of the schedule
with open('schedule.csv') as file: 
	csvFile = csv.reader(file, delimiter=',')
	header= next(csvFile)
	if header != None:
		for i, row in enumerate(csvFile):
			# print(row[dayNum])
			if i==weekNum:
				print(row[dayNum])
				person = row[dayNum]

# df = pd.read_csv('schedule.csv')
# person = df.iloc[weekNum,dayNum]

@bot.command()
async def todo(ctx):
	user = str(ctx.message.author.id)
	# print(user)
	await ctx.channel.send("Master would like to do <@" + user + ">'s mother but he also plans to implement the following commands: \n week, day, explain, pedro")

@bot.command()
async def today(ctx):

	global person
	global weekNum
	global dayNum

	print(person)

	beginning = "It is "
	end = "'s day today"

	if person in dictionary.keys():
		await ctx.channel.send(beginning + "<@" + dictionary.get(person) + ">" + end)
	else:
		await ctx.channel.send(beginning + person + end)


@bot.command()
async def week(ctx):
	global weekNum 

	await ctx.channel.send('It is week ' + str(weekNum))
	await ctx.channel.send("Here's this week's schedule: ")
	await ctx.channel.send(df.iloc[weekNum-1])

@bot.command()
async def day(ctx):
	global dayNum

	print()
	await ctx.channel.send("huh?")

@bot.command()
async def schedule(ctx):
	await ctx.channel.send(file=discord.File('Corey_Schedule.png'))

@bot.command()
async def change(ctx, newPerson):

	global changed
	global person

	if not changed:
		changed = True
		await ctx.channel.send("It was <@" + dictionary.get(person) + ">'s day, but it's " + newPerson + "'s day now")
	else:
		await ctx.channel.send("The day has been changed, you cannot change it again")

@bot.command(pass_context=True, aliases=['changeback'])
async def changeBack(ctx):

	global changed
	global person

	if changed:
		await ctx.channel.send("The day has been changed back to <@" + dictionary.get(person) + ">")
	else:
		await ctx.channel.send("You can't change back if the day hasn't been changed")

@bot.command(pass_context=True, aliases=['Yeff'])
async def yeff(ctx):
	await ctx.channel.send("<@155755250228264960>")

@bot.command()
async def master(ctx):
	await ctx.channel.send("<@173502986448797696> is the master, nobody goes against the master")

@bot.command(pass_context=True, aliases=['dad', 'Dad', 'Daddy'])
async def daddy(ctx):
	await ctx.channel.send("<@139598054373195776> is <@443813095622705152>'s daddy")

@bot.command(pass_context=True, aliases=['hubby'])
async def husband(ctx):
	await ctx.channel.send("<@133779065600475137>")

@bot.command(pass_context=True, aliases=['girlfriend'])
async def mother(ctx):
	await ctx.channel.send("<@411300301174341653> is <@225359460812455936>'s girlfriend and <@443813095622705152>'s mother")

@bot.command()
async def gf(ctx):
	if(person=="cathy"):
		await ctx.channel.send("Corey loves <@443813095622705152> the most")
	else:
		await ctx.channel.send("<@443813095622705152> is <@225359460812455936>'s gf")

@bot.command(pass_context=True, aliases=['bae','corbae','coreybae','Corey'])
async def corey(ctx):
	await ctx.channel.send("All hail the great <@225359460812455936> may he forever live a prosperous life")

@bot.command(pass_context=True, alisases=['freecorey'])
async def freeCorey(ctx):
	await ctx.channel.send("The following want to free <@225359460812455936>: <@483463488929529867> and <@184424945768464384>")

@bot.command()
async def live(ctx):
	await ctx.channel.send("@ everyone Corey, the great god, is streaming so hop in and say hi! www.twitch.tv/spareboredom")

@bot.command()
async def request(ctx):
	# file=discord.File('fireCan.jpg')
	await ctx.channel.send("Please send submit your command request and a description of it into the following container")
	await ctx.channel.send(file = discord.File('fireCan.jpg'))

@bot.command(pass_context=True, aliases=['punish'])
async def reprimand(ctx):
	await ctx.channel.send("Go practice more piano! <@" + dictionary.get('cathy')+">")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		# await ctx.channel.send("huh?")
		print("Command not found")

@bot.command()
async def status(ctx):
	print(ctx.author.activities)
	await ctx.channel.send(ctx.author.acitivites)

@bot.command()
async def baby(ctx):
	await ctx.channel.send()

@bot.event
async def chan(msg):
	print()
	# await ctx.channel.send()
	# chan = await msg.guild.create_txt_channel(name='new text')
	# web=await chan.create_webhook(name='new web')
	# print(web.url)

print("Running")
bot.run(TOKEN)