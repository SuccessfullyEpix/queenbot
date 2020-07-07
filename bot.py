import discord
import random
from discord.ext import commands
import asyncio
import os
import logging
import json

client = commands.Bot(command_prefix = 'YOUR PREFIX') #Put your bots prefix here

@client.event
async def on_ready(pass_context=True):
    print(client.user.name)
    print(client.user.id)
    print('-----------------')

async def game_presence():
    await client.wait_until_ready()

    games = ["", ""] #Here is where you put the bots status

    while not client.is_closed():
        status = random.choice(games)

        await client.change_presence(activity=discord.Game(status))

        await asyncio.sleep(60)

@client.command()
async def verify(ctx, message):
    member = ctx.message.author
    role = discord.utils.get(ctx.guild.roles, name='Verified Member')
    await ctx.author.add_roles(role)
    await ctx.send(f'Thank you for verifying {member.mention}.')
    await ctx.message.author.edit(nick='{}'.format(message))

blue = 0x00BFFF

@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOME MESSAGE CHANNEL ID)
    channel2 = client.get_channel(VERIFY PING CHANNEL ID)
    embed = discord.Embed(
        colour = discord.Colour.green()
    )

    embed.set_author(name='Welcome!')
    embed.add_field(name='Thank you for joining', value=f'Welcome to our amazing server {member.mention}! Make sure to head over to #another-general to get verified. We all hope you have a great time.')
    embed.set_thumbnail(url='{}'.format(member.avatar_url))

    await channel.send(embed=embed)
    await channel2.send(f'{member.mention} come here and please use command **verify (your social here)** otherwise you cant use our server.')

    with open('users.json', 'r') as f:
        users = json.load(f)


    await update_data(users, member)


    with open('users.json', 'w') as f:
        json.dump(users, f)

    await asyncio.sleep(120)
    await member.add_roles(role)


@client.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)


        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)
        await client.process_commands(message)


        with open('users.json', 'w') as f:
            json.dump(users, f)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp

async def level_up(users, user, message):
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1/4))
    if lvl_start < lvl_end:
        await message.channel.send(embed= discord.Embed(description= f'{user.mention} has reached level **{lvl_end}**! :tada:', color= blue))
        users[f'{user.id}']['level'] = lvl_end


client.loop.create_task(game_presence())
client.run("Your Bot TOKEN")
