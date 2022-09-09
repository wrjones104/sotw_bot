import datetime
import json
import os
import discord

import interactions
from dotenv import load_dotenv

load_dotenv()

bot = interactions.Client(os.getenv('discord_token'))


@bot.command()
@interactions.option(name="name")
@interactions.option(name="submitter")
@interactions.option(name="seed")
async def new_sotw(ctx: interactions.CommandContext, name: str, submitter: str, seed: str):
    """What's the flagstring?"""
    channel = discord.utils.get(ctx.guild.channels, id=1017605185931071548)
    if not os.path.exists('sotw_db.json'):
        with open('sotw_db.json', 'w') as newfile:
            newfile.write(json.dumps({}))
    with open('sotw_db.json') as x:
        sotw_db = json.load(x)
    await channel.send(f'-----------------------------------\n**{name}** by: {submitter}, rolled on'
                       f' {str(datetime.datetime.now().strftime("%b %d %Y"))}\n'
                       f'Seed Link: {seed}\n-----------------------------------')
    rankings = await channel.send("Nobody's finished yet... will you be the first?")
    sotw_db[len(sotw_db) + 1] = {"name": name, "submitter": submitter, "seed": seed, "creator": str(ctx.user),
                                 "create_date": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")),
                                 "rankings_msg_id": str(rankings.id), "runners": {}}
    with open('sotw_db.json', 'w') as updatefile:
        updatefile.write(json.dumps(sotw_db))
    await ctx.send("New SotW is live!")


@bot.command()
@interactions.option(description="Enter your time for this race!")
async def done(ctx: interactions.CommandContext, time: str):
    """Enter your time in 01:23:45 format"""
    channel = discord.utils.get(ctx.guild.channels, id=1017605185931071548)
    if not os.path.exists('sotw_db.json'):
        with open('sotw_db.json', 'w') as newfile:
            newfile.write(json.dumps({}))
    with open('sotw_db.json') as x:
        sotw_db = json.load(x)
    rankings = await channel.get_message(sotw_db[str(len(sotw_db))]['rankings_msg_id'])
    if str(ctx.user) in sotw_db[str(len(sotw_db))]['runners']:
        message = f"WTF {ctx.user}, you already finished this race!"
    else:
        sotw_db[str(len(sotw_db))]['runners'][str(ctx.user)] = {"finish_time": time,
                                                                "timestamp": str(datetime.datetime.now().strftime(
                                                                    "%b %d %Y %H:%M:%S"))}
        message = f"Wow, great job {ctx.user}, you finished in {time}!"
        updated_rankings_msg = ""
        for x, y in sotw_db[str(len(sotw_db))]['runners'].items():
            updated_rankings_msg += f"\n{x}: {y['finish_time']}"
        await rankings.edit(content=updated_rankings_msg)
        with open('sotw_db.json', 'w') as updatefile:
            updatefile.write(json.dumps(sotw_db))
    await ctx.send(message)


bot.start()
