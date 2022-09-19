import datetime
import json
import os

from discord.utils import get

from constants import discord_ids as ids
from functions.string_functions import parse_done_time, sortdict


async def create_new_sotw(ctx, name, submitter, seed):
    message_header = f'-----------------------------------\n**{name}** by: {submitter}, rolled on' \
                     f' {str(datetime.datetime.now().strftime("%b %d %Y"))}\n' \
                     f'Seed Link: {seed}\n-----------------------------------'
    sotw_channel = get(ctx.guild.channels, name='seed-of-the-week')
    leaderboard_channel = get(ctx.guild.channels, name='sotw-leaderboards')
    spoiler_channel = get(ctx.guild.channels, name='sotw-spoilers')
    if not os.path.exists('sotw_db.json'):
        with open('sotw_db.json', 'w') as newfile:
            newfile.write(json.dumps({}))
    with open('sotw_db.json') as x:
        sotw_db = json.load(x)
    try:
        participants = await sotw_channel.fetch_message(sotw_db[str(len(sotw_db))]['participants_msg_id'])
        rankings = await leaderboard_channel.fetch_message(sotw_db[str(len(sotw_db))]['rankings_msg_id'])
        await participants.edit(content=rankings.content)
    except:
        pass
    await leaderboard_channel.purge()
    leader_header = await leaderboard_channel.send(message_header)
    rankings = await leaderboard_channel.send("No participants.")
    sotw_header = await sotw_channel.send(message_header)
    participants = await sotw_channel.send("0 participants")
    spoiler_splitter = await spoiler_channel.send(
        f"-----------------------------------\nHere begins the **{name}** Seed of the Week\n"
        f"-----------------------------------")
    sotw_db[len(sotw_db) + 1] = {"name": name, "submitter": submitter, "seed": seed,
                                 "creator": str(ctx.user.name),
                                 "create_date": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")),
                                 "header_msg_id": str(sotw_header.id), "leaderboard_header_id": str(leader_header.id),
                                 "spoiler_splitter_id": str(spoiler_splitter.id),
                                 "rankings_msg_id": str(rankings.id), "participants_msg_id": str(participants.id),
                                 "runners": {}}
    with open('sotw_db.json', 'w') as updatefile:
        updatefile.write(json.dumps(sotw_db))
    role = get(ctx.guild.roles, name='seed-of-the-week')
    for member in ctx.guild.members:
        if role in member.roles:
            try:
                await member.remove_roles(role)
            except:
                print(f'Failed to remove role from {member}')


async def enter_time(ctx, time):
    if time == "Forfeit":
        ff = True
    else:
        ff = False
    sotw_channel = get(ctx.guild.channels, name='seed-of-the-week')
    leaderboard_channel = get(ctx.guild.channels, name='sotw-leaderboards')
    with open('sotw_db.json') as x:
        sotw_db = json.load(x)
    rankings = await leaderboard_channel.fetch_message(sotw_db[str(len(sotw_db))]['rankings_msg_id'])
    participants = await sotw_channel.fetch_message(sotw_db[str(len(sotw_db))]['participants_msg_id'])
    if ff:
        dt = time
    else:
        try:
            dt = parse_done_time(time)
        except:
            await ctx.response.send_message("Something is wrong with your time... try again", ephemeral=True)
            return None
    if str(ctx.user.name) in sotw_db[str(len(sotw_db))]['runners']:
        message = f"{ctx.user.name}, you already finished this race!"
    else:
        sotw_db[str(len(sotw_db))]['runners'][str(ctx.user.name)] = {"id": str(ctx.user.id), "finish_time": str(dt),
                                                                     "timestamp": str(datetime.datetime.now().strftime(
                                                                         "%b %d %Y %H:%M:%S"))}
        if not ff:
            message = f"Great job {ctx.user.name}, you finished in {str(dt)}!"
        else:
            message = f"Better luck next time!"
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
        role = get(ctx.guild.roles, name="seed-of-the-week")
        await ctx.user.add_roles(role)
    await ctx.response.send_message(message, ephemeral=True)


async def refresh(ctx):
    sotw_channel = get(ctx.guild.channels, name='seed-of-the-week')
    leaderboard_channel = get(ctx.guild.channels, name='sotw-leaderboards')
    spoiler_channel = get(ctx.guild.channels, name='sotw-spoilers')
    with open('sotw_db.json') as x:
        sotw_db = json.load(x)
    rankings = await leaderboard_channel.fetch_message(sotw_db[str(len(sotw_db))]['rankings_msg_id'])
    participants = await sotw_channel.fetch_message(sotw_db[str(len(sotw_db))]['participants_msg_id'])
    sotw_header = await sotw_channel.fetch_message(sotw_db[str(len(sotw_db))]['header_msg_id'])
    leader_header = await leaderboard_channel.fetch_message(sotw_db[str(len(sotw_db))]['leaderboard_header_id'])
    spoiler_splitter = await spoiler_channel.fetch_message(sotw_db[str(len(sotw_db))]['spoiler_splitter_id'])
    updated_rankings_msg = ""
    runner_list = []
    count = 0
    for x, y in sotw_db[str(len(sotw_db))]['runners'].items():
        runner_list.append({'name': x, 'time': y['finish_time']})
        runner_list.sort(key=sortdict)
    if not runner_list:
        updated_rankings_msg = rankings.content
    else:
        for x in runner_list:
            count += 1
            updated_rankings_msg += f"\n{count}) {x['name']} - {x['time']}"
    updated_participants_msg = f"{len(sotw_db[str(len(sotw_db))]['runners'].values())} participants"
    updated_header_msg = f"-----------------------------------\n**{sotw_db[str(len(sotw_db))]['name']}** by: {sotw_db[str(len(sotw_db))]['submitter']}, rolled on" \
                         f" {str(datetime.datetime.now().strftime('%b %d %Y'))}\n" \
                         f"Seed Link: {sotw_db[str(len(sotw_db))]['seed']}\n-----------------------------------"
    updated_spliiter_msg = f"-----------------------------------\nHere begins the **{sotw_db[str(len(sotw_db))]['name']}** Seed of the Week\n" \
        f"-----------------------------------"
    await rankings.edit(content=updated_rankings_msg)
    await participants.edit(content=updated_participants_msg)
    await leader_header.edit(content=updated_header_msg)
    await sotw_header.edit(content=updated_header_msg)
    await spoiler_splitter.edit(content=updated_spliiter_msg)
