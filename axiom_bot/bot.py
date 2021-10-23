import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import datetime
import math
import os
import random
import threading
import time
from os import listdir
import requests
from discord.utils import get
from discord.enums import ChannelType
import psutil
import sys
import richhelp
#from keep_alive import Keep_alive #use flask only to host on replit

bot = commands.Bot(command_prefix='.', help_command=richhelp.MyHelpCommand(),
                   owner_id=,
                   intents=discord.Intents.all()) #owner_id needs to begiven

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle,
                              activity=discord.Activity(
                                  type=discord.ActivityType.listening,
                                  name=".help"))
								  
    print("\nBot is connected, and Online!\nConnected as", f'{bot.user}')

@bot.command(help="Gives a pong message, showing bot's latency")
async def ping(ctx):
    color = discord.Colour.green()
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

@bot.command(description="Permanent server hardware information")
async def serverinfo(ctx):
    embed = discord.Embed(color=discord.Color.blurple())
    embed.title = 'Server Information'
    data = ""
    data += str(psutil.cpu_count()) + " Processing Cores \n"
    data += f"{psutil.cpu_count() // psutil.cpu_count(logical=False) * 16}" + " Thread Count \n"
    data += f"{psutil.virtual_memory().total / 2**30:.2f}" + " GB Total Memory \n"
    data += f"{psutil.virtual_memory().available / 2**30:.2f}" + " GB Available Currently \n"
    data += f"{psutil.virtual_memory().used / 2**30:.2f}" + "GB Being Used \n"
    embed.description = data
    await ctx.channel.send(embed=embed)


@bot.command(hidden=True, name='cpu', description="Cpu Information")
async def cpustats(ctx):
    embed = discord.Embed(color=discord.Color.blurple())
    embed.title = 'CPU Information'
    embed.description = str(psutil.cpu_percent(interval=1)) + "% CPU Usage \n"
    embed.description += str(
        psutil.getloadavg()[1]) + " average load over the last 5 minutes"
    await ctx.channel.send(embed=embed)


@bot.command(name='sm', help="sets a channel cooldown, only for admins")
@has_permissions(manage_messages=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode in this channel to {seconds} seconds!")


@slowmode.error
async def slowmode_error(ctx, error):
    print(error)
    print(type(error))
    print(dir(error))
    print(error.args)

    if isinstance(error, commands.BadArgument):
        await ctx.send('> [BadArgument] ' + str(error))
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('```This command can only run in a guild```')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('> [BadArgument] ' + str(error))
    print(ctx.args)
    print(ctx.message)


@bot.command(name='kick', description="Used by admins to kick members"
             )  #working kick command
@commands.has_permissions(kick_members=True)
async def kick_user(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    emb = discord.Embed(color=discord.Color.red())
    emb.title = 'Kick'
    emb.description = member.display_name + " was kicked."
    await ctx.channel.send(embed=emb)


@bot.command(name='assign',
             description="Usable by Admins to assign roles to server members.",
             aliases=["role"])  #command to assign roles to users
@has_permissions(manage_channels=True)
async def assign_role(ctx, member: discord.Member, *, role_name):
    role = get(ctx.guild.roles, name=role_name)
    #member : Member = get(ctx.guild.members,name = user_name)
    await member.add_roles(role)
    emb = discord.Embed(color=discord.Color.cyan())
    emb.title = 'Role assigned'
    emb.description = str(role) + " was successfully given to " + str(
        member.display_name)
    await ctx.channel.send(embed=emb)


@bot.command(hidden=True)
@has_permissions(ban_members=True)
async def unban(ctx, Member: discord.Member):
    await ctx.unban(Member)


def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)


@bot.command(hidden=True,
             name='restart',
             aliases=['reboot'],
             pass_context=True)
@has_permissions(administrator=True)
async def restart(ctx):
    await ctx.send('<:check:879595032078860308>|Restarting the bot!')
    restart_bot()
    if bot.restart == True:
        await ctx.send('<:check:879595032078860308>|Restart succesful!')
    else:
        await ctx.send('X_X Reboot unsuccessful')


#@restart.error()
#await ctx.send("<:cross:879595358978719824>|You dont have sufficient permissions to perform this action!")


@bot.command(hidden=True, help='Can only be executed by the Bot owner')
async def shutdown(ctx):
    id = str(ctx.author.id)
    if id == '722343830149398539':
        await ctx.send('<:check:879595032078860308>|GoodBye!')
        await ctx.bot.close()
    else:
        await ctx.send(
            "<:cross:879595358978719824>|You dont have sufficient permissions to perform this action!"
        )


@bot.command(aliases=['8ball'], help="Ask all you queries to the mighty 8ball")
async def _8ball(ctx, *question):
    x = ""
    for i in question:
        x += i + " "

    if '@everyone' in x or '@here' in x: return

    responses = [
        'It is certain.', 'It is decidedly so.', 'Without a doubt.',
        'Yes – definitely.', 'You may rely on it.', 'As I see it, yes.',
        'Most likely.', 'Outlook good.', 'Yes.', 'Ask your mum',
        'Signs point to yes.', ' Reply hazy, try again.', 'Ask again later.',
        ' Better not tell you now.', ' Cannot predict now.',
        'Concentrate and ask again.', 'Don\'t count on it.',
        ' My reply is no.', ' My sources say no.', 'Outlook not so good.',
        'Very doubtful.','bruh'
    ]
    if 'mom' in question:
        await ctx.send("Ask your mum!")
        return

    if '.flag' in question:
        await ctx.channel.purge(limit=1)
        return

    if 'where' and 'flag' in question:
        await ctx.send('All flags are secretly stored in a private repl')
        time.sleep(1)
        await ctx.channel.purge(limit=2)
        return

    if 'is' and 'earth' in question:
        await ctx.send(f'Question: {question}\nAnswer: Always has been')
        return

    if 'gay' in question:
        await ctx.send('why are you being gay :P')

    if 'AX10M{' in question:
        await ctx.channel.purge(limit=1)
        await ctx.send('Oh no no! Don\'t post flags here.')
    else:
        question_string = ""
        for i in question:
            question_string += i + " "
        await ctx.send(
            f'Question: {question_string}\nAnswer: {random.choice(responses)}')


@bot.command(help="Gives info about the current server")
async def guildinfo(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(title=name + " Server Information",
                          description=description,
                          color=discord.Color.blue())
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value='', inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)


@guildinfo.error
async def server_error(ctx, error):
    print(error)
    print(type(error))
    print(dir(error))
    print(error.args)

    if isinstance(error, commands.BadArgument):
        await ctx.send('> [BadArgument] ' + str(error))
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('```This command can only run in a guild```')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('> [BadArgument] ' + str(error))
    print(ctx.args)
    print(ctx.message)


@bot.command(help="alias - mb", aliases=["mb"])
async def membercount(ctx):
    memberCount = str(ctx.guild.member_count)
    embed = discord.Embed(description='', color=discord.Colour.orange())
    embed.add_field(name="Member Count", value=memberCount, inline=True)
    await ctx.send(embed=embed)


@bot.command(help='Get an inspirational quote')
async def quote(ctx):
    with open('quotes.txt', encoding="utf8") as f:
        lines = [l.strip() for l in f.readlines()]
    emb = discord.Embed(description=random.choice(lines),
                        color=discord.Colour.green())
    await ctx.send(embed=emb)


@bot.command(name="dm", help="Sends a nice-looking help command in your DM")
async def dm(ctx):
    await ctx.author.send(
        "> <:badge_botdev:862917160879783967> Below is the list of commands <:bot:859664040669741057> \n> <:discordchannel:859664074169122816> _8ball *Ask all your queries to the mighty 8ball*\n> <:discordchannel:859664074169122816> dm      *Sends a nice-looking help command*\n> <:discordchannel:859664074169122816> help    *Shows this message*\n> <:discordchannel:859664074169122816> ping    *Check the bot's latency*\n> <:discordchannel:859664074169122816> rate    *Rates anything you ask for*\n> <:discordchannel:859664074169122816> quote   *get a hand-picked quote*\n> <:discordchannel:859664074169122816> botinfo   *gives info about the bot dev*\n> <:discordchannel:859664074169122816> timer   *sets a timer for you*\n> <a:exclamation:862917802508025946> .help command for more info on a command.\n> <a:verified_blue:863247778222178355> You can also type .help <command> for more info on a command use."
    )


@bot.command(help="url to official Club AXIOM website")
async def web(ctx):
    embed = discord.Embed(title="The official webpage of AXIOM",
                          color=discord.Color.gold())
    embed.add_field(name="https://axiomdps.xyz/", value='', inline=True)
    embed.add_field(name="This site has been abandoned",
                    value=":(",
                    inline=False)
    embed.set_image(url=str(ctx.guild.icon_url))
    await ctx.send(embed=embed)


'''
@bot.command(help="Add a timer...")
async def timer(ctx, timeInput, *args):
    try:
        try:
            time = int(timeInput)
        except:
            convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
            time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
        if time > 86400:
            await ctx.send("I can\'t do timers over a day long")
            return
        if time < 0:
            await ctx.send("Timers don\'t go into negatives :/")
            return   
        if time >= 3600:
            emb = discord.Embed(description= f"data", color=discord.Colour.blurple())
            emb.title = 'Timer'
            data = ""
            embed.description = data            
            data += ("Timer: {time//3600} hours {time%3600//60} minutes {time%60} seconds")
            message = await ctx.send(embed=emb)
        elif time >= 60:
            emb = discord.Embed(description= f"data", color=discord.Colour.blurple())
            emb.title = 'Timer'
            data = ""
            embed.description = data            
            data += ("Timer: {time//3600} hours {time%3600//60} minutes {time%60} seconds")
            message = await ctx.send(embed=emb)
        elif time < 60:
            emb = discord.Embed(description= f"data", color=discord.Colour.blurple())
            emb.title = 'Timer'
            data = ""
            embed.description = data            
            data += ("Timer: {time//3600} hours {time%3600//60} minutes {time%60} seconds")
            message = await ctx.send(embed=emb)
        while True:
            try:
                await asyncio.sleep(3)
                time -= 3
                if time >= 3600:
                    await message.edit(content=f"Timer: {time//3600} hours {time %3600//60} minutes {time%60} seconds")
                elif time >= 60:
                    await message.edit(content=f"Timer: {time//60} minutes {time%60} seconds")
                elif time < 60:
                    await message.edit(content=f"Timer: {time} seconds")
                if time <= 0:
                    await message.edit(content="Ended!")
                    emb = discord.Embed(description=f"{ctx.author.mention} Your countdown Has ended!", color=discord.Colour.gold())    
                    await ctx.send(embed=emb)
                    break
            except:
                break
    except:
        await ctx.send(f"Alright, first you gotta let me know how I\'m gonna time **{timeInput}**....")
'''


@bot.command(hidden=True)
@has_permissions(mute_members=True)
async def tempmute(ctx, member: discord.Member, time: int, d, *, reason=None):
    guild = ctx.guild
    for role in guild.roles:
        if role.name == "muted":
            await member.add_roles(role)
            embed = discord.Embed(
                title="muted!",
                description=f"{member.mention} has been tempmuted ",
                colour=discord.Colour.light_gray())
            embed.add_field(name="reason:", value=reason, inline=False)
            embed.add_field(name="time left for the mute:",
                            value=f"{time}{d}",
                            inline=False)
            await ctx.send(embed=embed)
            if d == "s":
                await asyncio.sleep(time)
            if d == "m":
                await asyncio.sleep(time * 60)
            if d == "h":
                await asyncio.sleep(time * 60 * 60)
            if d == "d":
                await asyncio.sleep(time * 60 * 60 * 24)
            await member.remove_roles(role)
            embed = discord.Embed(title="unmute (temp) ",
                                  description=f"unmuted -{member.mention} ",
                                  colour=discord.Colour.light_gray())
            await ctx.send(embed=embed)
            return


@bot.command()
@has_permissions(administrator=True)
async def admincomms(ctx, ):
    await ctx.author.send(
        '```Secret guild commands at AXIOM server:\n1.) Kick -  .kick <Member>\n2.) Ban -   .ban <Member>\n3.) unban - .unban <Member>\n4.) Tempmute -  .tempmute <member> <time> <reason>```'
    )


@bot.command()
async def bug(ctx, desc=None, rep=None):
    user = ctx.author
    await ctx.author.send('```1.) Please explain the bug```')
    responseDesc = await bot.wait_for(
        'message',
        check=lambda message: message.author == ctx.author,
        timeout=300)
    description = responseDesc.content
    await ctx.author.send(
        '```2.) Please provide pictures/videos of this bug```')
    responseRep = await bot.wait_for(
        'message',
        check=lambda message: message.author == ctx.author,
        timeout=300)
    await ctx.author.send(
        '```Your bug report has been successfully submitted 😄```')
    responseRep = await bot.author.send(
        'message', check=lambda message: message.author == ctx.author)

    replicate = responseRep.content
    embed = discord.Embed(title='Bug Report', color=0x00ff00)
    embed.add_field(name='Description', value=description, inline=False)
    embed.add_field(name='Replicate', value=replicate, inline=True)
    embed.add_field(name='Reported By', value=user, inline=True)
    adminBug = bot.get_channel()
    await adminBug.send(embed=embed)


@bot.command(name='lock', help="Locks a specified channel", aliases=['l'])
@has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('✅ Locked down {}'.format(ctx.channel.mention))


@bot.command(name='unlock', help="Unlocks a specified channel", aliases=['ul'])
@has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('✅ Unlocked {}'.format(ctx.channel.mention))


@bot.command(hidden=True)
@has_permissions(administrator=True)
async def report(ctx):
    await ctx.author.send("Submitted bug reports ⏬")
    await ctx.author.send("{}".format(bug.reports))


@bot.command(help="Clears the entire channel", aliases=['p'])
@has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=1000)
    await ctx.send('messages cleared by {}'.format(ctx.author.mention))
    await ctx.message.delete()


@bot.command(help="add emotes", aliases=['ae'])
@has_permissions(administrator=True)
async def addemoji(ctx):
    await ctx.send("work in progress!")


@bot.command(help="removes emotes", aliases=['re'])
@has_permissions(administrator=True)
async def removeemoji(ctx):
    await ctx.send("work in progress!")


@bot.command(help="Divides given two numbers", aliases=['divide'])
async def div(ctx, num1: float, num2: float):
    answer = num1 / num2
    ans_em = discord.Embed(
        title='Division',
        description=f'Question: {num1} / {num2}\nAnswer: {answer}',
        colour=discord.Colour.from_rgb(252, 252, 0))
    await ctx.send(embed=ans_em)


@div.error
async def div_error(ctx, error):
    print(error)
    print(type(error))
    print(dir(error))
    print(error.args)

    if isinstance(error, commands.BadArgument):
        await ctx.send('[BadArgument] ' + str(error))
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('[CommandInvokeError] ' + str(error))
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('It needs two values')
    print(ctx.args)
    print(ctx.message)


@bot.command(help="Mulitply two rationals", aliases=["multiply"])
async def multi(ctx, num1: float, num2: float):
    answer = num1 * num2
    ans_em = discord.Embed(
        title='Multiplication',
        description=f'Question: {num1} * {num2}\nAnswer: {answer}',
        colour=discord.Colour.from_rgb(252, 252, 0))
    await ctx.send(embed=ans_em)


@multi.error
async def multi_error(ctx, error):
    print(error)
    print(type(error))
    print(dir(error))
    print(error.args)

    if isinstance(error, commands.BadArgument):
        await ctx.send('[BadArgument] ' + str(error))
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('[CommandInvokeError] ' + str(error))
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('It needs two values')
    print(ctx.args)
    print(ctx.message)


@bot.command(help="Adds two rationals", aliases=["add"])
async def addi(ctx, num1: float, num2: float):
    answer = num1 + num2
    ans_em = discord.Embed(
        title='Addition',
        description=f'Question: {num1} + {num2}\nAnswer: {answer}',
        colour=discord.Colour.from_rgb(252, 252, 0))
    await ctx.send(embed=ans_em)


@addi.error
async def add_error(ctx, error):
    print(error)
    print(type(error))
    print(dir(error))
    print(error.args)

    if isinstance(error, commands.BadArgument):
        await ctx.send('[BadArgument] ' + str(error))
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('[CommandInvokeError] ' + str(error))
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('It needs two values')
    print(ctx.args)
    print(ctx.message)


@bot.command(help="Subtracts two rationals", aliases=["sub"])
async def subtract(ctx, num1: float, num2: float):
    answer = num1 - num2
    ans_em = discord.Embed(
        title='Subtraction',
        description=f'Question: {num1} - {num2}\nAnswer: {answer}',
        colour=discord.Colour.from_rgb(252, 252, 0))
    await ctx.send(embed=ans_em)


@subtract.error
async def subtract_error(ctx, error):
    print(error)
    print(type(error))
    print(dir(error))
    print(error.args)

    if isinstance(error, commands.BadArgument):
        await ctx.send('[BadArgument] ' + str(error))
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('[CommandInvokeError] ' + str(error))
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('It needs two values')
    print(ctx.args)
    print(ctx.message)


@bot.command(help="sends you all the bot commands aliases in your DMs")
async def aliases(ctx):
    await ctx.author.send("```Below are all the command aliases```")


@bot.command(hidden=True)
async def on_command_error(ctx, error):
    print('[on_command_error] error:', error)
    print('[on_command_error] ctx:', ctx)


@bot.command(aliases=["rr"])
@commands.has_permissions(administrator=True)
async def reactionroles(ctx):
    await ctx.author.send("> Work in progress 🤖")


@bot.command(aliases=["tkth"])
async def tickethelp(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title='Ticketing System',
                          description='How to use the ticketing system: ',
                          colour=discord.Colour.blue())
    embed.add_field(
        name='Creating a ticket',
        value=
        'To create a ticket just use the command and a new channel will be opened for you',
        inline=True)
    embed.add_field(name='Transcript of ticket',
                    value='This command logs all ticket actions and messgaes',
                    inline=True)
    embed.add_field(
        name='Closing a Ticket',
        value=
        'To close a ticket just type the message closeTicket in the new ticket channel created for you',
        inline=True)
    embed.add_field(name='Shows Error logs',
                    value='Shows up errors if any',
                    inline=True)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_author(name='Made by Hype')
    await ctx.send(embed=embed)

@bot.command(help="Shows the current errors in the bot's code", aliases=["el"])
async def errorlogs(ctx):
    with open("errors.txt") as f:
        try:
            await ctx.author.send(f.readlines())
        except:
            await ctx.send("This is awkward, an error has occured!")


@bot.command(aliases=['tkt', 'tickets'])
async def ticket(ctx):
    guild = ctx.message.guild
    admin_role = get(guild.roles, name="APEX")
    bot_self = bot.user
    author = ctx.author
    overwrites = {
        guild.default_role:
        discord.PermissionOverwrite(read_messages=False),
        admin_role:
        discord.PermissionOverwrite(read_messages=True),
        bot_self:
        discord.PermissionOverwrite(read_messages=True, manage_channels=True),
        author:
        discord.PermissionOverwrite(read_messages=True)
    }
    confirmation = await ctx.send(
        f"> Hey, {ctx.author.mention}\n> Please react to this message with the below emoji within 60 seconds to open a ticket."
    )
    await confirmation.add_reaction(emoji='✅')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '✅'

    try:
        reaction, user = await bot.wait_for('reaction_add',
                                            timeout=60.0,
                                            check=check)
        guild = ctx.message.guild
        TicketChannel = await guild.create_text_channel(f'{ctx.author}',
                                                        overwrites=overwrites,
                                                        category=None)
        await TicketChannel.send(
            f"> Hey, {ctx.author.mention},\n> You have opened a ticket so please wait till the support team arrives, until then please describe your query down.\n> Use the command `.transcript` for a transcript and `.close` to close the ticket."
        )

        def checkClose(m):
            return m.content == 'closeTicket' and m.channel == TicketChannel

        msg = await bot.wait_for('message', check=checkClose)
        await TicketChannel.send("> Ok closing the ticket in 5 seconds")
        time.sleep(5)
        await TicketChannel.delete()
    except asyncio.TimeoutError:
        await ctx.send(
            f"> {ctx.author.mention}, You didn't react on time to open your ticket successfully."
        )


@bot.command(brief='This command can delete bulk messages!')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.message.delete


@bot.command(aliases=['transcript', 'copy'])
@has_permissions(manage_messages=True)
async def history(ctx, limit: int = 100):
    channel = ctx.message.channel
    messages = await ctx.channel.history(limit=limit).flatten()
    with open(f"{channel}_messages.txt", "a+", encoding="utf-8") as f:
        print(f"\nTranscript Saved by - {ctx.author.display_name}.\n\n",
              file=f)
        for message in messages:
            embed = ""
            if len(message.embeds) != 0:
                embed = message.embeds[0].description
                print(f"{message.author.name} - {embed}", file=f)
            print(f"{message.author.name} - {message.content}", file=f)
    await ctx.message.add_reaction("✅")
    await ctx.send(f"{ctx.author.mention}, Transcript saved.")
    history = discord.File(fp=f'{channel}_messages.txt', filename=None)
    await ctx.author.send(file=history)


@bot.command(aliases=['del_chan', 'close'])
@commands.has_permissions(administrator=True)
async def shh(ctx):
    Channel = ctx.message.channel
    await Channel.delete()


@bot.command(hidden=True, help="Inter event's leaderboard", aliases=["le"])
async def leaderboard(ctx):
    icon = str(ctx.guild.set_thumbnail)  #icon_url
    emb = discord.Embed(title="Aiom Inter-school winners",
                        color=discord.Color.dark_theme())
    emb.set_thumbnail(url=icon)
    emb.add_field(name="Algorithmix", value='', inline=True)
    emb.add_field(name="Brain Booster", value='', inline=False)
    emb.add_field(name="Sync the Link", value='', inline=False)
    emb.add_field(name="Problem Solving",
                  value='Have patience, the result is yet to be declared (:',
                  inline=True)
    await ctx.send("embed=emb")

@bot.command(aliases=['massping','msp'], pass_context=True)
async def ms_ping(ctx):
	channel = ctx.message.channel   
	async def Typing():
		await asyncio.sleep(0.5)
		try:
			t1 = time.perf_counter()
			await ctx.channel.send.Typing(channel)
			ta = t1
			t2 = time.perf_counter()
			await ctx.channel.send.Typing(channel)
			tb = t2
			ra = round((tb - ta) * 1000)
		finally:
			pass
		try:
			t1a = time.perf_counter()
			await ctx.channel.send.Typing(channel)
			ta1 = t1a
			t2a = time.perf_counter()
			await ctx.channel.send.Typing(channel)
			tb1 = t2a
			ra1 = round((tb1 - ta1) * 1000)
		finally:
			pass
		try:
			t1b = time.perf_counter()
			await ctx.channel.send.Typing(channel)
			ta2 = t1b
			t2b = time.perf_counter()
			await ctx.channel.send.Typing(channel)
			tb2 = t2b
			ra2 = round((tb2 - ta2) * 1000)
		finally:
			pass
		try:
			t1c = time.perf_counter()
			await ctx.channel.send.Typing(channel)
			ta3 = t1c

			t2c = time.perf_counter()
			await ctx.channel.send.Typing(channel)
			tb3 = t2c

			ra3 = round((tb3 - ta3) * 1000)
		finally:
			pass
		try:
			t1d = time.perf_counter()
			await ctx.channel.send.Typing(channel)
			ta4 = t1d

			t2d = time.perf_counter()
			await ctx.channel.send.Typing(channel)
			tb4 = t2d

			ra4 = round((tb4 - ta4) * 1000)
		finally:
			pass

		e = discord.Embed(title="Connection", colour = 909999)
		e.add_field(name='Ping 1', value=str(ra))
		e.add_field(name='Ping 2', value=str(ra2))
		e.add_field(name='Ping 3', value=str(ra3))
		e.add_field(name='Ping 4', value=str(ra4))
		await bot.say(embed=e)

#Keep_alive() #for flask server
bot.run(TOKEN)
