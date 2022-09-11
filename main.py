import datetime
import json
import os
import discord

import interactions
from dotenv import load_dotenv

load_dotenv()

bot = interactions.Client(token=os.getenv('discord_token'), intents=interactions.Intents.GUILD_PRESENCES | interactions.Intents.DEFAULT)


@bot.command()
@interactions.option(name="name")
@interactions.option(name="submitter")
@interactions.option(name="seed")
async def new_sotw(ctx: interactions.CommandContext, name: str, submitter: str, seed: str):
    """What's the flagstring?"""
    message_header = f'-----------------------------------\n**{name}** by: {submitter}, rolled on' \
                     f' {str(datetime.datetime.now().strftime("%b %d %Y"))}\n' \
                     f'Seed Link: {seed}\n-----------------------------------'
    sotw_channel = discord.utils.get(ctx.guild.channels, id=1017605185931071548)
    leaderboard_channel = discord.utils.get(ctx.guild.channels, id=1017863469657243750)
    spoiler_channel = discord.utils.get(ctx.guild.channels, id=1017863496429469757)
    if not os.path.exists('sotw_db.json'):
        with open('sotw_db.json', 'w') as newfile:
            newfile.write(json.dumps({}))
    with open('sotw_db.json') as x:
        sotw_db = json.load(x)
    try:
        participants = await sotw_channel.get_message(sotw_db[str(len(sotw_db))]['participants_msg_id'])
        rankings = await leaderboard_channel.get_message(sotw_db[str(len(sotw_db))]['rankings_msg_id'])
        await participants.edit(content=rankings.content)
    except:
        pass
    await leaderboard_channel.purge(amount=2)
    await leaderboard_channel.send(message_header)
    rankings = await leaderboard_channel.send("...")
    await sotw_channel.send(message_header)
    participants = await sotw_channel.send("0 participants")
    sotw_db[len(sotw_db) + 1] = {"name": name, "submitter": submitter, "seed": seed, "creator": str(ctx.user),
                                 "create_date": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")),
                                 "rankings_msg_id": str(rankings.id), "participants_msg_id": str(participants.id),
                                 "runners": {}}
    with open('sotw_db.json', 'w') as updatefile:
        updatefile.write(json.dumps(sotw_db))
    role = discord.utils.get(ctx.guild.roles, id=1017863537588195428)
    print(role.name)
    #TODO: why does this not work?
    # for x in ctx.guild.members:
    #     try:
    #         await x.remove_role(role=role, guild_id=834193269311143977)
    #     except:
    #         print(x)
    await spoiler_channel.send(f"-----------------------------------\nHere begins the **{name}** Seed of the Week\n"
                               f"-----------------------------------")
    await ctx.send("New SotW is live!")


@bot.command()
@interactions.option(description="Enter your time for this race!")
async def done(ctx: interactions.CommandContext, time: str):
    """Enter your time in 01:23:45 format"""
    sotw_channel = discord.utils.get(ctx.guild.channels, id=1017605185931071548)
    leaderboard_channel = discord.utils.get(ctx.guild.channels, id=1017863469657243750)
    with open('sotw_db.json') as x:
        sotw_db = json.load(x)
    rankings = await leaderboard_channel.get_message(sotw_db[str(len(sotw_db))]['rankings_msg_id'])
    participants = await sotw_channel.get_message(sotw_db[str(len(sotw_db))]['participants_msg_id'])
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
        updated_participants_msg = f"{len(sotw_db[str(len(sotw_db))]['runners'].values())} participants"
        await rankings.edit(content=updated_rankings_msg)
        await participants.edit(content=updated_participants_msg)
        with open('sotw_db.json', 'w') as updatefile:
            updatefile.write(json.dumps(sotw_db))
        role = discord.utils.get(ctx.guild.roles, name="seed-of-the-week")
        await ctx.member.add_role(role=role, guild_id=834193269311143977)
    await ctx.send(message)


bot.start()
