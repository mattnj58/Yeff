# bot.py
import os
import discord
import pandas as pd
import datetime
import calendar
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

# client = discord.Client()

bot = commands.Bot(command_prefix="!")

@bot.command()
async def today(ctx):

	#this is a dictionary of all the people who I know is part of the schedule
	dictionary = {'Cathy': '443813095622705152','Anthony': '133779065600475137', 'Henry': '139598054373195776', 'Yeff': '155755250228264960','Wendy': '411300301174341653','Jihoon': 'idk man, whatever jinhoon username is', 'Matt': '173502986448797696'}

	#reads the csv file of the schedule.... note that there should be no headers
	df = pd.read_csv('schedule.csv', encoding = 'utf8', delimiter=',')
	print(df)
	day = findDay(datetime.date.today().strftime("%d %m %Y"))
	week = week_number_of_month(datetime.datetime.today().date())
	print("day", day)
	print("week",week)

	person = df.iloc[week-1,day]

	beginning = "It is "
	end = "'s day today"

	if person in dictionary.keys():
		await ctx.channel.send(beginning + "<@" + dictionary.get(person) + ">" + end)
	else:
		await ctx.channel.send(beginning + person + end)

@bot.command()
async def schedule(ctx):
	await ctx.channel.send(file=discord.File('Corey_Schedule.png'))

# def users(ctx):
# 	user_list = []
# 	# members = await ctx.guild.fetch_members(limit=150).flatten()
# 	for guild in bot.guilds:
# 		for member in guild.members:
# 			user_list.append("<@"+str(member.id)+">")
# 			# print("@"+str(member.id))
# 	# await ctx.channel.send(user_list[0])
# 	return user_list

def findDay(date):
	today = datetime.datetime.strptime(date, '%d %m %Y').weekday()+1
	return(today)

def week_number_of_month(date_value):
     return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)


print("Running")
bot.run(TOKEN)