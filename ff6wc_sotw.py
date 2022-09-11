import datetime
import json
import os
import discord

import interactions
from dotenv import load_dotenv

from functions.string_functions import parse_done_time

load_dotenv()

bot = interactions.Client(token=os.getenv('discord_token'), intents=interactions.Intents.GUILD_PRESENCES | interactions.Intents.DEFAULT)

def sortdict(e):
    return e['time']

@bot.command()
@interactions.option(name="name")
@interactions.option(name="submitter")
@interactions.option(name="seed")
async def new_sotw(ctx: interactions.CommandContext, name: str, submitter: str, seed: str):
    """What's the flagstring?"""
    message_header = f'-----------------------------------\n**{name}** by: {submitter}, rolled on' \
                     f' {str(datetime.datetime.now().strftime("%b %d %Y"))}\n' \
                     f'Seed Link: {seed}\n-----------------------------------'
    sotw_channel = discord.utils.get(ctx.guild.channels, id=682266472466481158)
    leaderboard_channel = discord.utils.get(ctx.guild.channels, id=682266947278209113)
    spoiler_channel = discord.utils.get(ctx.guild.channels, id=682267113758523470)
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
    role = discord.utils.get(ctx.guild.roles, id=682268600236638215)
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
    sotw_channel = discord.utils.get(ctx.guild.channels, id=682266472466481158)
    leaderboard_channel = discord.utils.get(ctx.guild.channels, id=682266947278209113)
    with open('sotw_db.json') as x:
        sotw_db = json.load(x)
    rankings = await leaderboard_channel.get_message(sotw_db[str(len(sotw_db))]['rankings_msg_id'])
    participants = await sotw_channel.get_message(sotw_db[str(len(sotw_db))]['participants_msg_id'])
    if str(ctx.user) in sotw_db[str(len(sotw_db))]['runners']:
        message = f"{ctx.user}, you already finished this race!"
    else:
        try:
            dt = parse_done_time(time)
        except:
            await ctx.send("Invalid time format!", ephemeral=True)
            return None
        sotw_db[str(len(sotw_db))]['runners'][str(ctx.user)] = {"id": ctx.user.id, "finish_time": str(dt),
                                                                "timestamp": str(datetime.datetime.now().strftime(
                                                                    "%b %d %Y %H:%M:%S"))}
        message = f"Great job {ctx.user}, you finished in {str(dt)}!"
        updated_rankings_msg = ""
        runner_list = []
        count = 0
        for x, y in sotw_db[str(len(sotw_db))]['runners'].items():
            runner_list.append({'name': x, 'time': y['finish_time']})
            runner_list.sort(key=sortdict)
        for x in runner_list:
            count += 1
            updated_rankings_msg += f"\n{count}) {x['name']} - {x['time']}"
        updated_participants_msg = f"{len(sotw_db[str(len(sotw_db))]['runners'].values())} participants"
        await rankings.edit(content=updated_rankings_msg)
        await participants.edit(content=updated_participants_msg)
        with open('sotw_db.json', 'w') as updatefile:
            updatefile.write(json.dumps(sotw_db))
        role = discord.utils.get(ctx.guild.roles, name="seed-of-the-week")
        await ctx.member.add_role(role=role, guild_id=666661907628949504)
    await ctx.send(message, ephemeral=True)


bot.start()
