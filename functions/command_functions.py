import datetime
import json
import os
import random
import subprocess

import pygsheets
import requests
from discord import Interaction, TextStyle
from discord.ui import Modal, TextInput
from discord.utils import get

import db.constants as constants
import views as views
from flag_builder import chaos
from functions.string_functions import parse_done_time, sortdict


class NewSubModal(Modal):
    sotwname = TextInput(
        label="Enter the name for the Seed of the Week",
        style=TextStyle.short,
    )

    sotwdesc = TextInput(
        label="Enter a description for the seed",
        style=TextStyle.paragraph,
    )

    sotwflags = TextInput(
        label="Enter the flags",
        style=TextStyle.paragraph,
    )

    sotwapi = TextInput(
        label="API Environment (main or dev)",
        placeholder="main",
        default="main",
        min_length=3,
        max_length=4,
        style=TextStyle.short,
    )

    def __init__(self, title: str) -> None:
        super().__init__(title=title, timeout=None)

    async def on_submit(self, interaction: Interaction, /) -> None:
        await interaction.response.defer()


def _get_env_from_submission(submission_data, default='main'):
    try:
        # Also check for empty string
        env = submission_data[7]
        return env if env else default
    except (IndexError, TypeError):
        return default


async def generate_seed(flags, seed_desc, env=None):
    if env not in constants.FF6WC_APIS:
        env = constants.DEFAULT_API

    api_config = constants.FF6WC_APIS[env]
    url = api_config["url"]
    payload = json.dumps({
        "key": api_config["key"],
        "flags": flags,
        "description": seed_desc
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    print(data)
    return data


async def create_new_sotw(ctx, name, submitter, flags, description, env=None):
    if env not in constants.FF6WC_APIS:
        env = constants.DEFAULT_API
    try:
        seed = await generate_seed(flags, description, env)
        seed_link = seed['url']
    except TypeError:
        raise
    message_header = f'-----------------------------------\n**{name}** by: {submitter}, rolled on' \
                     f' {str(datetime.datetime.now().strftime("%b %d %Y"))}\n' \
                     f'Seed Link: <{seed_link}>\n' \
                     f'```{description}```' \
                     f'-----------------------------------'
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
    except Exception:
        pass
    await leaderboard_channel.purge()
    leader_header = await leaderboard_channel.send(message_header)
    rankings = await leaderboard_channel.send("No participants.")
    sotw_header = await sotw_channel.send(message_header)
    participants = await sotw_channel.send("0 participants")
    spoiler_splitter = await spoiler_channel.send(
        f"-----------------------------------\nHere begins the **{name}** Seed of the Week\n"
        f"-----------------------------------")
    sotw_db[len(sotw_db) + 1] = {"name": name, "submitter": submitter, "seed": seed_link,
                                 "creator": str(ctx.user.name), "description": description, "seed_id": seed['seed_id'],
                                 "env": env,
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
            except Exception:
                print(f'Failed to remove role from {member}')

    # Here, we force push the sotw_db.json file out to the Google Cloud bucket.
    # This allows the website to pull updated SotW data immediately.
    try:
        subprocess.check_call("gsutil cp sotw_db.json gs://seedbot", shell=True)
    except subprocess.CalledProcessError:
        pass

    # This next bit of code updates the SotW SeedBot preset.

    api_url = 'https://seedbot.net/api/update_sotw_preset/' if constants.env_type == "production" else 'http://127.0.0.1:8000/api/update_sotw_preset/'
    secret_key = constants.webapp_api_key

    payload = {
        'flags': flags,
        'description': f"Practice for this week's SotW: **{name}** by {submitter}\n```{description}```"
    }

    headers = {
        'Authorization': f'Bearer {secret_key}',
        'Content-Type': 'application/json'
    }

    response = requests.post(api_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print("Successfully updated SotW preset.")
    else:
        print(f"Failed to update preset. Status: {response.status_code}, Response: {response.text}")


async def auto_create_new_sotw(ctx):
    print(f'{datetime.datetime.now()}: Starting auto-roll workflow.')
    sotw_guild = ctx.get_guild(constants.guild)
    sotw_channel = get(ctx.get_all_channels(), guild__id=constants.guild, name="seed-of-the-week")
    leaderboard_channel = get(ctx.get_all_channels(), guild__id=constants.guild, name="sotw-leaderboards")
    spoiler_channel = get(ctx.get_all_channels(), guild__id=constants.guild, name="sotw-spoilers")
    general_channel = get(ctx.get_all_channels(), guild__id=constants.guild, name='ff6wc-general-chat')
    if not os.path.exists('settings.json'):
        with open('settings.json', 'w') as newfile:
            newfile.write(json.dumps({}))
    with open('settings.json') as x:
        settings = json.load(x)
    if not settings:
        return print(f'{datetime.datetime.now()}: No settings options found - shutting down auto-roll workflow')
    elif settings['auto-mode'] == "False":
        return print(f'{datetime.datetime.now()}: Auto-mode set to FALSE - shutting down auto-roll workflow')
    error_check = True
    badflags = ['']
    attempts = 0
    is_flashback = False
    while error_check:
        attempts += 1
        filecheck = False
        this_week = await get_possible_seeds(badflags)

        if not this_week:
            if attempts <= 5:
                print(f"{datetime.datetime.now()}: No submissions found. Attempting Flashback (Attempt {attempts}/5)...")
                this_week = await get_rolled_seed(badflags)
                if this_week:
                    is_flashback = True
            
            if not this_week:
                print(f"{datetime.datetime.now()}: Proceeding with Chaos fallback...")
                flags = chaos()
                description = "There weren't any submissions for me to roll, so now you must face the CHAOS!"
                name = f"Chaos {random.choice(['Ensues', 'Reigns', 'Rains Down', 'Upon Ye Mortals', 'is Lyfe', 'Eternal', 'Infinite'])}"
                env = "main"
                submitter = "SotW Bot"
                del_row = False
                error_check = False # Chaos always works
            else:
                # We found a flashback seed
                flags = this_week[0][4]
                description = this_week[0][3]
                name = this_week[0][2]
                submitter = this_week[0][1]
                env = _get_env_from_submission(this_week[0])
                del_row = False
        elif "ff6worldscollide.com" not in this_week[0][5]:
            flags = this_week[0][4]
            description = this_week[0][3]
            name = this_week[0][2]
            submitter = this_week[0][1]
            del_row = True
            seed_link = this_week[0][5]
            filecheck = True
            env = "main"
        else:
            flags = this_week[0][4]
            description = this_week[0][3]
            name = this_week[0][2]
            submitter = this_week[0][1]
            del_row = True
            env = _get_env_from_submission(this_week[0])

        try:
            if not error_check == False: # Skip if we already rolled chaos
                if not filecheck:
                    getseed = await generate_seed(flags, description, env)
                    seed = getseed['seed_id']
                    seed_link = getseed['url']
                    error_check = False
                else:
                    seed = False
                    error_check = False
        except KeyError:
            print(f'{datetime.datetime.now()}: There was a flag error with this submission: {name} from {submitter}')
            badflags.append(flags)

    sotw_name = f"Flashback: {name}" if is_flashback else name
    message_header = f'-----------------------------------\n**{sotw_name}** by: {submitter}, rolled on' \
                     f' {str(datetime.datetime.now().strftime("%b %d %Y"))}\n' \
                     f'Seed Link: <{seed_link}>\n' \
                     f'```{description}```' \
                     f'-----------------------------------'
    if not os.path.exists('sotw_db.json'):
        with open('sotw_db.json', 'w') as newfile:
            newfile.write(json.dumps({}))
    with open('sotw_db.json') as x:
        sotw_db = json.load(x)
    try:
        participants = await sotw_channel.fetch_message(sotw_db[str(len(sotw_db))]['participants_msg_id'])
        rankings = await leaderboard_channel.fetch_message(sotw_db[str(len(sotw_db))]['rankings_msg_id'])
        await participants.edit(content=rankings.content)
    except Exception:
        pass
    await leaderboard_channel.purge()
    leader_header = await leaderboard_channel.send(message_header)
    rankings = await leaderboard_channel.send("No participants.")
    sotw_header = await sotw_channel.send(message_header)
    participants = await sotw_channel.send("0 participants")
    spoiler_splitter = await spoiler_channel.send(
        f"-----------------------------------\nHere begins the **{name}** Seed of the Week\n"
        f"-----------------------------------")
    create_date = str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))
    sotw_db[len(sotw_db) + 1] = {"name": sotw_name, "submitter": submitter, "seed": seed_link, "flags": flags,
                                 "creator": 'Auto-Rolled', "description": description, "seed_id": seed,
                                 "env": env,
                                 "create_date": create_date,
                                 "header_msg_id": str(sotw_header.id), "leaderboard_header_id": str(leader_header.id),
                                 "spoiler_splitter_id": str(spoiler_splitter.id),
                                 "rankings_msg_id": str(rankings.id), "participants_msg_id": str(participants.id),
                                 "runners": {}}
    await move_tabs(this_week, create_date, submitter, name, description, flags, seed_link, del_row)
    with open('sotw_db.json', 'w') as updatefile:
        updatefile.write(json.dumps(sotw_db))
    role = get(sotw_guild.roles, name='seed-of-the-week')
    for member in sotw_guild.members:
        if role in member.roles:
            try:
                await member.remove_roles(role)
            except Exception:
                print(f'{datetime.datetime.now()}: Failed to remove role from {member}')
    role = get(sotw_guild.roles, name='SotW Ping')
    sotwview = views.SotwPingView()
    await general_channel.send(
        f"<@&{role.id}>: A new SotW is live! **{sotw_name}**, crafted by **{submitter}**!\n```{description}```"
        f"Check it out @ <#{sotw_channel.id}>! And don't "
        f"forget to submit your own ideas for the Seed of the Week!",
        view=sotwview,
        )

    # Here, we force push the sotw_db.json file out to the Google Cloud bucket.
    # This allows the website to pull updated SotW data immediately.
    try:
        subprocess.check_call("gsutil cp sotw_db.json gs://seedbot", shell=True)
    except subprocess.CalledProcessError:
        pass

    # This next bit of code updates the SotW SeedBot preset.
    api_url = 'https://seedbot.net/api/update_sotw_preset/' if constants.env_type == "production" else 'http://127.0.0.1:8000/api/update_sotw_preset/'
    secret_key = constants.webapp_api_key

    payload = {
        'flags': flags,
        'description': f"Practice for this week's SotW: **{name}** by {submitter}\n```{description}```"
    }

    headers = {
        'Authorization': f'Bearer {secret_key}',
        'Content-Type': 'application/json'
    }

    response = requests.post(api_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print("Successfully updated SotW preset.")
    else:
        print(f"Failed to update preset. Status: {response.status_code}, Response: {response.text}")


async def enter_time(ctx, time):
    if time.casefold() in ("forfeit", "ff"):
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
        except Exception:
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
            message = "Better luck next time!"
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
                         f" {' '.join(sotw_db[str(len(sotw_db))]['create_date'].split()[:3])}\n" \
                         f"Seed Link: <{sotw_db[str(len(sotw_db))]['seed']}>\n" \
                         f"```{sotw_db[str(len(sotw_db))]['description']}```" \
                         f"-----------------------------------\n"
    updated_spliiter_msg = f"-----------------------------------\nHere begins the **{sotw_db[str(len(sotw_db))]['name']}** Seed of the Week\n" \
                           f"-----------------------------------"
    await rankings.edit(content=updated_rankings_msg)
    await participants.edit(content=updated_participants_msg)
    await leader_header.edit(content=updated_header_msg)
    await sotw_header.edit(content=updated_header_msg)
    await spoiler_splitter.edit(content=updated_spliiter_msg)


async def new_submission(ctx):
    modal = NewSubModal("Submit your idea for SotW!")
    await ctx.response.send_modal(modal)
    await modal.wait()
    try:
        env = str(modal.sotwapi).lower().strip()
        if env not in constants.FF6WC_APIS:
            env = constants.DEFAULT_API
        link = await generate_seed(str(modal.sotwflags), str(modal.sotwdesc), env)
        await write_new_submission(ctx, modal.sotwname, modal.sotwflags, modal.sotwdesc, link['url'], env)
        return await ctx.user.send(
            'Your submission has been received! Check out the full submission list here:'
            ' <http://seedbot.net/sotw-submissions>')
    except KeyError:
        return await ctx.user.send(
            'There seems to be something wrong with your flags - '
            f'double-check them and try again!\n```{str(modal.sotwflags)}```')


async def write_new_submission(ctx, name, flags, desc, link, env):
    gc = pygsheets.authorize(service_file='functions/sotw-bot-eda350e55a58.json')
    sh = gc.open(constants.sheetname)
    wks = sh[0]

    cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    lastrow = len(cells)

    wks.insert_rows(lastrow, number=1,
                    values=[str(datetime.datetime.now()), str(ctx.user.name), str(name), str(desc), str(flags),
                            str(link), "", str(env)])




async def get_possible_seeds(badflags):
    gc = pygsheets.authorize(service_file='functions/sotw-bot-eda350e55a58.json')
    sh = gc.open(constants.sheetname)
    wks = sh[0]

    cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=True, returnas='matrix')
    random_select = []
    try:
        print(f'{datetime.datetime.now()}: Getting possible flagsets')
        for n, x in enumerate(cells[1:]):
            if x[6] and x[4] not in badflags:
                random_select.append([x, n + 2])
        print(f'{datetime.datetime.now()}: {len(random_select)} possible flagsets found!')
        if random_select:
            return random.choice(random_select)
        else:
            return None
    except IndexError:
        return None


async def get_rolled_seed(badflags):
    gc = pygsheets.authorize(service_file='functions/sotw-bot-eda350e55a58.json')
    sh = gc.open(constants.sheetname)
    wks = sh[1]

    cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=True, returnas='matrix')
    random_select = []
    try:
        print(f'{datetime.datetime.now()}: Getting archive flagsets')
        # Exclude header (1) and the 10 most recent rolls (bottom 10)
        eligible_rows = cells[1:-10] if len(cells) > 11 else []
        for x in eligible_rows:
            if x[4] not in badflags:
                # Reformat to match sh[0] structure: [date, submitter, name, desc, flags, link, vetted, env]
                # sh[1] structure: [date, submitter, name, desc, flags, link, env]
                random_select.append([x[0], x[1], x[2], x[3], x[4], x[5], "", x[6]])
        print(f'{datetime.datetime.now()}: {len(random_select)} archive flagsets found!')
        if random_select:
            return [random.choice(random_select), -1]
        else:
            return None
    except IndexError:
        return None


async def move_tabs(ctx, create_date, submitter, name, description, flags, seed_link, del_row):
    gc = pygsheets.authorize(service_file='functions/sotw-bot-eda350e55a58.json')
    sh = gc.open(constants.sheetname)
    wks = sh[0]
    wks2 = sh[1]

    cells2 = wks2.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    lastrow = len(cells2)

    if del_row:
        wks.delete_rows(ctx[1])

    env = _get_env_from_submission(ctx[0])

    wks2.insert_rows(lastrow, number=1, values=[create_date, submitter, name, description, flags, seed_link, env])


async def auto_mode(ctx, choice):
    with open('settings.json') as settings_file:
        update = json.load(settings_file)
    if not update:
        newdata = {'auto-mode': choice}
    else:
        update['auto-mode'] = choice
        newdata = update
    with open('settings.json', 'w') as updatefile:
        updatefile.write(json.dumps(newdata))
