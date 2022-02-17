import nextcord
from nextcord import (
    Interaction
)
from nextcord.ext import commands
from nextcord.ext.commands import (
    BucketType,
    Cooldown,
    CooldownMapping,
)
from nextcord.ui import (
    Button, 
    View, 
    button
)
from nextcord.errors import Forbidden

import os
import datetime
import random
from typing import (
    List,
    Callable,
)

import aiohttp
import humanfriendly
import yarsaw
import asyncio
import gtts
import logging

import motor
import motor.motor_asyncio

from urllib.parse import quote_plus

def edited_cooldown(rate, per, type=BucketType.default):
    cooldown = Cooldown(rate, per)
    cooldown_mapping = CooldownMapping(cooldown, type=type)
    ApplicationCommand = nextcord.application_command.ApplicationCommand
    ApplicationSubcommand = nextcord.application_command.ApplicationSubcommand
    def decorator(func: Callable):
        if isinstance(func, (ApplicationCommand, ApplicationSubcommand)):
            func.callback._buckets = cooldown_mapping 
        else:
            raise ValueError("Decorator must be applied to the command decorator, not the command function.")
        return func
    return decorator

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.WARNING)

bot = yarsaw.Client("ybSHEatbivek", "0fc8104d3bmsh9fcc7b9c2a86b3fp14c1ebjsn3b44d7af5e86") 

guilds = 914050761917362186

intents = nextcord.Intents.all()
intents.members = True
intents.guilds = True

client = commands.Bot(
    command_prefix="?", 
    intents=intents, 
    help_command=None,
    status=nextcord.Status.dnd,
    owner_id=852485677777682432
)
cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://FlameyosFlow:reZPy4ZKz5YqumS@discord.fm5pk.mongodb.net/discord?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE")
db = cluster.discord
collection = db.bank
companyaa = db.company
crates = db.crates
serverlevels = db.leveling
memberlevels = db.level

client.activity = nextcord.Game(name=f"Prefix - Slash Commands / | In {len([guild for guild in client.guilds])} guilds")

class Google(View):
    def __init__(self, query: str):
        super().__init__()
        
        query = quote_plus(query)
        url = f'https://www.google.com/search?q={query}'

        self.add_item(Button(label='Results From Google', url=url))
        
@client.slash_command(description="Search on google directly using this command!")
async def google(
    interaction: nextcord.Interaction, 
    query: str = nextcord.SlashOption(
        name="search",
        description="What would you like to search on google?",
        required = True
    )
):
    async with interaction.channel.typing():
        await interaction.send(f'Google Results for: `{query}`', view=Google(query))

@client.slash_command(description="Greentext your text!")
async def greentext(
    interaction: nextcord.Interaction,
    text: str = nextcord.SlashOption(
        name="text",
        description="What would you like to greentext?",
        required=True
    )
):
    async with interaction.channel.typing():
        await interaction.send(
            "```"
            f"{text}"
            "```"
        )
        return

@client.slash_command(description="Talk with the bot!")
async def talk(interaction):
    async with interaction.channel.typing():
        if (interaction.user.voice):
            vc = interaction.user.voice.channel
            vca = await vc.connect()
            talking = True
            await interaction.send("You are now talking to me, to end this interaction type: goodbye famurai!")

            while talking:

                try:
                    def check(m):
                        return m.author == interaction.user

                    msg_raw = await client.wait_for("message", check=check, timeout=60.0)
                    msg = msg_raw.content
                except asyncio.TimeoutError:
                    talking = False
                    await interaction.send("You timed out, rerun the command.")

                raw_response = await bot.get_ai_response(
                    msg, 
                    bot_name="Famu but people call me Famurai", 
                    bot_master="FlameyosFlow", 
                    bot_location="Qatar", 
                    bot_favorite_color="Black", 
                    bot_birth_place="Egypt", 
                    bot_company="Fire Samurai inc.",
                    bot_build='Public',
                    bot_email='...I have no email.',
                    bot_age='1',
                    bot_birth_date='18th December, 2021',
                    bot_birth_year='2021',
                    bot_favorite_book='Harry Potter',
                    bot_favorite_band='Balenciaga',
                    bot_favorite_artist='Eminem',
                    bot_favorite_actress='Selena Gomez',
                    bot_favorite_actor='Tom Holland',
                )

                response = raw_response.AIResponse
                output = gtts.gTTS(text=response, lang="en", slow=False)
                output.save("output.mp3")

                if msg == "goodbye famurai":
                    talking = False
                    await interaction.send("Okay, I will stop talking to you, nice seeing you {}".format(interaction.user.mention))
                    await interaction.guild.voice_client.disconnect()

                else:
                    vca.play(nextcord.FFmpegPCMAudio("output.mp3"))

                    await interaction.send(response)

        else:
            await interaction.send("You're not in a voice channel, do you want to continue without voice? respond in `yes` or `no`")
            try:
                def check(m):
                    return m.author == interaction.user
                    
                raw_msg = await client.wait_for("message", check=check, timeout=60.0)
                msg = raw_msg.content
            except asyncio.TimeoutError:
                await interaction.send("You timed out, rerun the command.")
                pass

            if msg == "yes":
                talking = True
                await interaction.send("You are now talking to me, to end this interaction: type goodbye famurai!")

                while talking:

                    try:
                        def check(m):
                            return m.author == interaction.user and m.channel == interaction.channel

                        msg_raw = await client.wait_for("message", check=check, timeout=60.0)
                        msg = msg_raw.content
                    except asyncio.TimeoutError:
                        await interaction.send("You timed out, rerun the command.")
                        pass

                    if msg == "goodbye famurai":
                        talking = False
                        await interaction.send("Okay, I will stop talking to you, nice seeing you {}".format(interaction.user.mention))

                    else:
                        raw_response = await bot.get_ai_response(
                            msg, 
                            bot_name="Famu but people call me Famurai", 
                            bot_master="FlameyosFlow", 
                            bot_location="Qatar", 
                            bot_favorite_color="Black", 
                            bot_birth_place="Egypt", 
                            bot_company="Fire Samurai inc.",
                            bot_build='Public',
                            bot_email='...I have no email.',
                            bot_age='1',
                            bot_birth_date='18th December, 2021',
                            bot_birth_year='2021',
                            bot_favorite_book='Harry Potter',
                            bot_favorite_band='Balenciaga',
                            bot_favorite_artist='Eminem',
                            bot_favorite_actress='Selena Gomez',
                            bot_favorite_actor='Tom Holland',
                        )
                        response = raw_response.AIResponse

                        await interaction.send(response)

            elif msg == "no":
                await interaction.response.send_message("Okay, I guess I will take that as a no.")

@client.slash_command(description="Set a reminder!")
async def remindme(
    interaction: nextcord.Interaction, 
    time = nextcord.SlashOption(
        name="time",
        description="How long is the timer? ex: 6h or 7d",
        required=True
    ), 

    message = nextcord.SlashOption(
        name="message",
        description="What is your reminder message?",
        required=True
    ),
):
    async with interaction.channel.typing():
        duration = humanfriendly.parse_timespan(time)
        await interaction.send(
            f"Set reminder for {interaction.user.mention} \n{message} \n||Set for {time}||"
        )

        await asyncio.sleep(duration)

        await interaction.channel.send(
            f"Reminder for {interaction.user.mention} \n{message}"
        )

@client.slash_command(description="Stop chatting with Famurai")
async def leave(interaction):
    async with interaction.channel.typing():
        talking = False
        if (interaction.user.voice):
            await interaction.guild.voice_client.disconnect()
            await interaction.send("I have left your voice channel!")

        else:
            await interaction.send("Okay, Thanks for talking with me :D")

@client.slash_command(description="Create a giveaway with this command!")
async def gstart(
    inter: nextcord.Interaction, 
    duration = nextcord.SlashOption(
        name="time",
        description="How long should it last? ex: 7d or 12h",
        required=True
    ), 
    prize = nextcord.SlashOption(
        name="prize",
        description="What is the prize?",
        required=True
    )
):
    if not (inter.user.guild_permissions.manage_guild):
        await inter.send("You need `manage_guild` permissions")
        pass

    else:
        dur = humanfriendly.parse_timespan(duration)

        end = datetime.datetime.utcnow() + datetime.timedelta(seconds=dur)

        giveaway = nextcord.Embed(
            title="Made by {}".format(inter.user),
            description="Prize: {} \nTime: {}".format(prize, duration),
            color = nextcord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        giveaway.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        giveaway.set_footer(text=f"Ends in {end} UTC")
        await inter.send(embed=giveaway)

        await (await inter.original_message()).add_reaction("🎉")
        await asyncio.sleep(dur)
        old_msg = await inter.original_message()

        new_msg = await inter.channel.fetch_message(old_msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(client.user))

        winner = random.choice(users)
        await inter.send(f"Congratulations {winner.mention}, you just won the prize of {prize}")

@client.slash_command(description="Random birbs from the internet!")
async def birbs(interaction):
    async with interaction.channel.typing():
        async def get_birbs():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/Birbs/new.json") as r:
                    res = await r.json()

            return res['data']['children'][random.randint(0, 25)]['data']['url']

        async def btncallback(interaction):
            birbs = await get_birbs()
            emb = interaction.message.embeds[0].set_image(url=birbs)
            emb.set_footer(text=f"🤩: {random.randint(1, 10000)} 😢: {random.randint(1, 1000)}")
            await interaction.response.edit_message(embed=emb)

        async def delcallback(interaction):
           await interaction.message.delete()

        btn1 = Button(
            label="Next Birb",
            style=nextcord.ButtonStyle.green,
        )

        btn2 = Button(
            style=nextcord.ButtonStyle.gray,
            emoji="🗑️"
        )

        btn1.callback = btncallback
        btn2.callback = delcallback
        view=View()
        view.add_item(btn1)
        view.add_item(btn2)

        embed = nextcord.Embed(title="These can talk, cool right?") 
        embed.set_image(url=await get_birbs())
        embed.set_footer(text=f"🤩: {random.randint(1, 10000)} 😢: {random.randint(1, 1000)}")

        await interaction.send(embed=embed, view=view)    

@client.slash_command(description="Random pandas from the internet!")
async def aww(interaction):
    async with interaction.channel.typing():
        async def get_birbs():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/aww/new.json") as r:
                    res = await r.json()

            return res['data']['children'][random.randint(0, 25)]['data']['url']

        async def btncallback(interaction):
            birbs = await get_birbs()
            emb = interaction.message.embeds[0].set_image(url=birbs)
            emb.set_footer(text=f"🤩: {random.randint(1, 10000)} 😢: {random.randint(1, 1000)}")
            await interaction.response.edit_message(embed=emb)

        async def delcallback(interaction):
           await interaction.message.delete()

        btn1 = Button(
            label="Next Cute Animal",
            style=nextcord.ButtonStyle.green,
        )

        btn2 = Button(
            style=nextcord.ButtonStyle.gray,
            emoji="🗑️"
        )

        btn1.callback = btncallback
        btn2.callback = delcallback
        view=View()
        view.add_item(btn1)
        view.add_item(btn2)

        embed = nextcord.Embed(title="These are SOOO CUTEEE") 
        embed.set_image(url=await get_birbs())
        embed.set_footer(text=f"🤩: {random.randint(1, 10000)} 😢: {random.randint(1, 1000)}")

        await interaction.send(embed=embed, view=view)

@client.slash_command(description="Random pandas from the internet!")
async def pandas(interaction):
    async with interaction.channel.typing():
        async def get_birbs():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/panda/new.json") as r:
                    res = await r.json()

            return res['data']['children'][random.randint(0, 25)]['data']['url']

        async def btncallback(interaction):
            birbs = await get_birbs()
            emb = interaction.message.embeds[0].set_image(url=birbs)
            emb.set_footer(text=f"🤩: {random.randint(1, 10000)} 😢: {random.randint(1, 1000)}")
            await interaction.response.edit_message(embed=emb)

        async def delcallback(interaction):
           await interaction.message.delete()

        btn1 = Button(
            label="Next Panda",
            style=nextcord.ButtonStyle.green,
        )

        btn2 = Button(
            style=nextcord.ButtonStyle.gray,
            emoji="🗑️"
        )

        btn1.callback = btncallback
        btn2.callback = delcallback
        view=View()
        view.add_item(btn1)
        view.add_item(btn2)

        embed = nextcord.Embed(title="Cutest animals in my opinion:") 
        embed.set_image(url=await get_birbs())
        embed.set_footer(text=f"🤩: {random.randint(1, 10000)} 😢: {random.randint(1, 1000)}")

        await interaction.send(embed=embed, view=view)    

@client.slash_command(description="Random kittys from the internet")
async def kittys(interaction):
    async with interaction.channel.typing():
        async def get_kittys():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/catpictures/new.json") as r:
                    res = await r.json()

            return res['data']['children'][random.randint(1, 25)]['data']['url']

        async def btncallback(interaction):
            cat = await get_kittys()
            emb = interaction.message.embeds[0].set_image(url=cat)
            emb.set_footer(text=f"🤩: {random.randint(1, 10000)} 😢: {random.randint(1, 1000)}")
            await interaction.response.edit_message(embed=emb)

        async def delcallback(interaction):
            await interaction.message.delete()

        btn1 = Button(
            label="Next Kittys",
            style=nextcord.ButtonStyle.green,
        )

        btn2 = Button(
            style=nextcord.ButtonStyle.gray,
            emoji="🗑️"
        )

        btn1.callback = btncallback
        btn2.callback = delcallback

        view=View()
        view.add_item(btn1)
        view.add_item(btn2)

        embed = nextcord.Embed(title="I got one of the cutiest one:")
        embed.set_image(url=await get_kittys())
        embed.set_footer(text=f"🤩: {random.randint(1, 10000)} 😢: {random.randint(1, 1000)}")
        
        await interaction.response.send_message(embed=embed, view=view)

@client.slash_command(description="Random puppys from the internet!")
async def puppy(interaction):
    async with interaction.channel.typing():
        async def get_puppys():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/dogpictures/new.json") as r:
                    res = await r.json()

            return res['data']['children'][random.randint(0, 25)]['data']['url']

        async def btncallback(interaction):
            pup = await get_puppys()
            emb = interaction.message.embeds[0].set_image(url=pup)
            emb.set_footer(text=f"🤩: {random.randint(1, 10001)} 😢: {random.randint(0, 1000)}")
            await interaction.response.edit_message(embed=emb)

        async def delcallback(interaction):
            await interaction.message.delete()

        btn1 = Button(
            label="Next Puppy",
            style=nextcord.ButtonStyle.green,
        )

        btn2 = Button(
            style=nextcord.ButtonStyle.gray,
            emoji="🗑️"
        ) 

        btn1.callback = btncallback
        btn2.callback = delcallback

        view=View() 
        view.add_item(btn1)
        view.add_item(btn2)

        embed = nextcord.Embed(
            title="I got a cute one for you!"
        )
        embed.set_image(url=await get_puppys())
        embed.set_footer(text= f"🤩: {random.randint(1, 10000)} 😢: {random.randint(1, 1000)}")

        await interaction.response.send_message(embed=embed, view=view)
        
@client.slash_command(description="Get some memes!")
async def meme(interaction):
    async with interaction.channel.typing():
        async def get_meme():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.reddit.com/r/dankmemes/new.json") as r:
                    res = await r.json()

            return res['data']['children'][random.randint(0, 25)]['data']['url']

        async def button_callback(interaction):
            meme = await get_meme()
            emb = interaction.message.embeds[0].set_image(url=meme)
            emb.set_footer(text=f"🤩: {random.randint(0, 75000)} 😢: {random.randint(0, 35000)}")
            await interaction.response.edit_message(embed=emb)

        async def delete_callback(interaction):
            await interaction.message.delete()

        button1 = Button(
            label="Next Meme",
            style=nextcord.ButtonStyle.green,
        )
        button2 = Button(
            label="🗑️",
            style=nextcord.ButtonStyle.gray,
        ) 

        button1.callback = button_callback
        button2.callback = delete_callback
        
        view=View()  
        view.add_item(button1)
        view.add_item(button2)

        embed = nextcord.Embed(title="Rate this bad boi.")
        embed.set_image(url=await get_meme())
    
        embed.set_footer(text=f"🤩: {random.randint(0, 55000)} 😢: {random.randint(0, 35000)}")
        await interaction.send(embed=embed, view=view)

@client.slash_command(description="Random red pandas from the internet (cute)!")
async def redpandas(interaction):
    async with interaction.channel.typing():
        async def get_meme():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.reddit.com/r/redpandas/new.json") as r:
                    res = await r.json()

            return res['data']['children'][random.randint(0, 25)]['data']['url']

        async def button_callback(interaction):
            meme = await get_meme()
            emb = interaction.message.embeds[0].set_image(url=meme)
            emb.set_footer(text=f"🤩: {random.randint(0, 75000)} 😢: {random.randint(0, 35000)}")
            await interaction.response.edit_message(embed=emb)

        async def delete_callback(interaction):
            await interaction.message.delete()

        button1 = Button(
            label="Next Red Panda",
            style=nextcord.ButtonStyle.green,
        )
        button2 = Button(
            label="🗑️",
            style=nextcord.ButtonStyle.gray,
        ) 

        button1.callback = button_callback
        button2.callback = delete_callback
        
        view=View()  
        view.add_item(button1)
        view.add_item(button2)

        embed = nextcord.Embed(title="How cute!!")
        embed.set_image(url=await get_meme())
    
        embed.set_footer(text=f"🤩: {random.randint(0, 55000)} 😢: {random.randint(0, 35000)}")
        await interaction.send(embed=embed, view=view)

@client.slash_command(description="Random food from the internet (really tasty looking)!")
async def tastyfood(interaction):
    async with interaction.channel.typing():
        async def get_meme():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.reddit.com/r/food/new.json") as r:
                    res = await r.json()

            return res['data']['children'][random.randint(0, 25)]['data']['url']

        async def button_callback(interaction):
            meme = await get_meme()
            emb = interaction.message.embeds[0].set_image(url=meme)
            emb.set_footer(text=f"🤩: {random.randint(0, 75000)} 😢: {random.randint(0, 35000)}")
            await interaction.response.edit_message(embed=emb)

        async def delete_callback(interaction):
            await interaction.message.delete()

        button1 = Button(
            label="Next Dish",
            style=nextcord.ButtonStyle.green,
        )
        button2 = Button(
            label="🗑️",
            style=nextcord.ButtonStyle.gray,
        ) 

        button1.callback = button_callback
        button2.callback = delete_callback
        
        view=View()  
        view.add_item(button1)
        view.add_item(button2)

        embed = nextcord.Embed(title="I am starving just looking at these")
        embed.set_image(url=await get_meme())
    
        embed.set_footer(text=f"🤩: {random.randint(0, 55000)} 😢: {random.randint(0, 35000)}")
        await interaction.send(embed=embed, view=view)

@client.slash_command(name="dice", description="Roll The Dice And Bet From 1 to 6")
async def dice(
    interaction: nextcord.Interaction, 
    bet: int = nextcord.SlashOption(
        name="bet",
        description="What do you wanna bet? 1-6",
        required=True
    ), 

    amount = nextcord.SlashOption(
        name="amount",
        description="What is the amount of money that you want to bet?",
        required=True
    )
):  
    async with interaction.channel.typing():
        member = interaction.user
        findbank = await collection.find_one({"_id": member.id})
        if not findbank:
            await collection.insert_one({"_id": member.id, "wallet": 0, "bank": 0})

        wallet = findbank["wallet"]
            
        f = random.randint(0, 6)
        if amount == "all":
            amount = int(wallet)
        else:
            amount = int(amount)

        if amount <= 0:
            await interaction.send(f"{amount} is 0 or negative.")
            return

        elif amount > 300000:
            await interaction.send(f"{amount} is more than $300,000.")
            return

        elif bet < 1 or bet > 6:
            await interaction.send(f"{bet} is not a valid dice number.")
            return

        if bet == f:
            em = nextcord.Embed(
                title="You Won!",
                description=f"My bet was {f} and your bet was {bet}",
                color=nextcord.Color.green()
            )

            updated_money = wallet + amount
            await collection.update_one({"_id": member.id}, {"$set": {"wallet": updated_money}})
            await interaction.send(embed=em)
            return

        em = nextcord.Embed(
            title="You Lost!",
            description="My bet was {:,} and your bet was {:,}".format(f, bet),
            color=nextcord.Color.red()
        )
                
        updated_money = wallet - amount
        await collection.update_one({"_id": member.id}, {"$set": {"wallet": updated_money}})
        await interaction.send(embed=em)

@client.slash_command(name="adventure", description="Stop it, Go Travel.")
async def adventure(
    interaction: nextcord.Interaction, 
    direction = nextcord.SlashOption(
        name="direction",
        choices={"Left", "Right", "Middle"},
        description="Which direction do you wanna go?",
    )
):
    async with interaction.channel.typing():
        member = interaction.user
        f = random.randint(1, 101)
        findcrates = await crates.find_one({"_id": member.id})
        if not findcrates:
            await crates.insert_one({"_id": member.id, "crates": 0})

        num_crates = findcrates["crates"]

        user = interaction.user

        if direction == "Left":
            if f >= 78:
                await interaction.response.send_message(f"{user.mention} You went left, and you got 3 crates, CONGRATULATIONS! :D")
                crates_updated = num_crates + 3
                await crates.update_one({"_id": user.id}, {"$set": {"crates": crates_updated}})

            elif f >= 60:
                await interaction.response.send_message(f"{user.mention} You went left, and you got 2 crates, CONGRATULATIONS! :D")
                crates_updated = num_crates + 2
                await crates.update_one({"_id": user.id}, {"$set": {"crates": crates_updated}})

            elif f >= 50:
                await interaction.response.send_message(f"{user.mention} You went left, and you got 1 crate, CONGRATULATIONS! :D")
                crates_updated = num_crates + 1
                await crates.update_one({"_id": user.id}, {"$set": {"crates": crates_updated}})

            else:
                await interaction.response.send_message(f"{user.mention} You went left, and found nothing.")
                return

        elif direction == "Right":
            if f >= 78:
                await interaction.response.send_message(f"{user.mention} You went right, and you got THREE 3 crates, CONGRATULATIONS! :D")
                crates_updated = num_crates + 3
                await crates.update_one({"_id": user.id}, {"$set": {"crates": crates_updated}})

            elif f >= 60:
                await interaction.response.send_message(f"{user.mention} You went right, and you got TWO 2 crates, CONGRATULATIONS! :D")
                crates_updated = num_crates + 2
                await crates.update_one({"_id": user.id}, {"$set": {"crates": crates_updated}})

            elif f >= 50:
                await interaction.response.send_message(f"{user.mention} You went right, and you got ONE 1 crate, CONGRATULATIONS! :D")
                crates_updated = num_crates + 1
                await crates.update_one({"_id": user.id}, {"$set": {"crates": crates_updated}})

            else:
                await interaction.response.send_message(f"{user.mention} You went right, and found nothing.")
                return

        elif direction == "Middle":
            if f >= 78:
                await interaction.response.send_message(f"{user.mention} You went middle, and you got 3 crates, CONGRATULATIONS! :D")
                crates_updated = num_crates + 3
                await crates.update_one({"_id": user.id}, {"$set": {"crates": crates_updated}})

            elif f >= 60:
                await interaction.response.send_message(f"{user.mention} You went middle, and you got 2 crates, CONGRATULATIONS! :D")
                crates_updated = num_crates + 2
                await crates.update_one({"_id": user.id}, {"$set": {"crates": crates_updated}})

            elif f >= 50:
                await interaction.response.send_message(f"{user.mention} You went middle, and you got 1 crate, CONGRATULATIONS! :D")
                crates_updated = num_crates + 1
                await crates.update_one({"_id": user.id}, {"$set": {"crates": crates_updated}})

            else:
                await interaction.response.send_message(f"{user.mention} You went middle, and found nothing.")
        return

@client.slash_command(description="See someone's avatar!")
async def avatar(
    interaction: nextcord.Interaction,
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who are we taking avatar's picture?",
        required=False
    )
):
    async with interaction.channel.typing():
        if not member:
            member = interaction.user

        if member == interaction.user:
            await interaction.send(embed=nextcord.Embed(title=f"Here is your avatar!").set_image(url=member.avatar.url))
        else:
            await interaction.send(embed=nextcord.Embed(title=f"Here is {member.name}'s avatar!").set_image(url=member.avatar.url))

@client.slash_command(name="bal", description="Check your balance!")
async def balance(
    interaction: nextcord.Interaction,
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who's balance are we checking?",
        required=False
    )
):
    await interaction.response.defer()
    async with interaction.channel.typing():
        if member == None:
            member = interaction.user
        else:
            member = member
                
        findbank = await collection.find_one({"_id": member.id})
        if not findbank:
            await collection.insert_one({"_id": member.id, "wallet": 0, "bank": 0})

        wallet = findbank["wallet"]
        bank = findbank["bank"]

        em = nextcord.Embed(title=f"{member.name}'s Balance", color=member.color)
        em.add_field(name="Wallet Balance:", value="{:,}".format(wallet))
        em.add_field(name='Bank Balance:', value="{:,}".format(bank))
        await interaction.followup.send(embed=em)

@client.slash_command(name="beg", description="Beg off the streets!")
@commands.cooldown(rate=2, per=30.0, type=BucketType.user)
async def beg(interaction: nextcord.Interaction):
    member = interaction.user
    findbank = await collection.find_one({"_id": member.id})
    if not findbank:
        await collection.insert_one({"_id": member.id, "wallet": 0, "bank": 0})

    wallet = findbank["wallet"]

    earnings = random.randrange(1, 1001)

    begchance = random.randint(1, 101)
            
    if begchance > 55:
        em = nextcord.Embed(title="oh um-", description=f"No one gave you any money.", color=nextcord.Color.red(), timestamp=datetime.datetime.utcnow())
        em.set_footer(text="Maybe next time buddy.")
        await interaction.response.send_message(embed=em)

    elif begchance < 45:
        updated_money = wallet + earnings
        await collection.update_one({"_id": member.id}, {"$set": {"wallet": updated_money}})
        em = nextcord.Embed(title="les goo!", description=f"Someone gave you ${earnings}, May god keep Them.", color=nextcord.Color.green())
        await interaction.response.send_message(embed=em)
    return

class ConfirmDEP(View):
    def __init__(self):
        super().__init__()
        self.value = None

    @button(label='Confirm', style=nextcord.ButtonStyle.green)
    async def confirm(self, button: Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("You have confirmed this deposit!", ephemeral=True)
        self.value = True
        self.stop()

    @button(label='Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button: Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("You have cancelled this deposit!", ephemeral=True)
        self.value = False
        self.stop()

@client.slash_command(
    name="deposit", 
    description="Deposit some money to your bank!"
)
async def deposit(
    interaction: nextcord.Interaction, 
    amount: int = nextcord.SlashOption(
        name="amount",
        description="How much do you want to deposit?",
        required=True
    )
):
    async with interaction.channel.typing():
        member = interaction.user
        findbank = await collection.find_one({"_id": member.id})
        if not findbank:
            await collection.insert_one({"_id": member.id, "wallet": 0, "bank": 0})

        wallet = findbank["wallet"]
        bank = findbank["bank"]

        if amount == 'all':
            if int(wallet) > 0:
                amount = int(wallet)
            else:
                await interaction.response.send_message("You don't have any funds in your Wallet")

        if amount > int(wallet):
            await interaction.response.send_message("You have insufficient funds in your Wallet.")
            return

        if amount < 0:
            await interaction.response.send_message("Your amount must be positive")
            return

        else:

            view=ConfirmDEP()
            await interaction.response.send_message(content="Are you sure you want to do this?", view=view, ephemeral=True)
            await view.wait()
            if view.value is None:
                return

            elif view.value:

                updated_wallet = wallet - amount
                updated_bank = bank + amount
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": updated_wallet}})
                await collection.update_one({"_id": member.id}, {"$set": {"bank": updated_bank}})

                await interaction.response.send_message(f"You deposited ${amount} coins from your Wallet, {interaction.user.mention}!", ephemeral=True)

            else:
                await interaction.response.send_message("You have cancelled this deposit!", ephemeral=True)

@client.slash_command(name="daily", description="Get daily money!")
async def daily(interaction: nextcord.Interaction):
    async with interaction.channel.typing():
        member = interaction.user
        findbank = await collection.find_one({"_id": member.id})
        if not findbank:
            await collection.insert_one({"_id": member.id, "wallet": 0, "bank": 0})

        wallet = findbank["wallet"]
        uw = wallet + 10000

        await collection.update_one({"_id": member.id}, {"$set": {"wallet": uw}})
        await interaction.send(f"You have recieved 10000 from /daily, see you next day!")

@client.event
async def on_command_error(interaction: nextcord.Interaction, error):
    if isinstance(error, commands.CommandNotFound):
        em = nextcord.Embed(
            title = "That command was not found!",
            color=nextcord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )

        await interaction.reply(embed=em)

    raise error

@client.event
async def on_application_command_error(interaction, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed=nextcord.Embed(
            title="Hold up bud.",
            description=f"Try again in {error.retry_after:,}"
        )
        await interaction.send(embed=embed)

@client.event
async def on_ready():
    print('We are logged in as {0.user} by FlameyosFlow#8894!'.format(client))

@client.slash_command(name="ping", description="Famurai latency!")
async def ping(interaction: nextcord.Interaction):
    async with interaction.channel.typing():
        if round(client.latency * 1000) <= 50:
            embed = nextcord.Embed(
                title="PONG!",
                description=f"The ping is **{round(client.latency *1000)}** milliseconds!",
                color=nextcord.Color.green()
            )

        elif round(client.latency * 1000) <= 100:
            embed = nextcord.Embed(
                title="PONG!",
                description=f"The ping is **{round(client.latency *1000)}** milliseconds!",
                color=nextcord.Color.green()
            )

        elif round(client.latency * 1000) <= 200:
            embed = nextcord.Embed(
                title="PONG!",
                description=f"The ping is **{round(client.latency *1000)}** milliseconds!",
                color=nextcord.Color.yellow()
            )

        else:
            embed = nextcord.Embed(
                title="PONG!",
                description=f"The ping is **{round(client.latency *1000)}** milliseconds!",
                color=nextcord.Color.red()
            )

        await interaction.response.send_message(embed=embed)

@client.slash_command(name="8ball", description="You have called the 8ball to predict the future for you.")
async def _8ball(
    interaction: nextcord.Interaction, *, 
    question: str = nextcord.SlashOption(
        name="question",
        description="What question do you wanna ask the bot?",
        required=True 
    )
):
    async with interaction.channel.typing():
        possibilities = [
            "Yes.",
            "Ofcourse!",
            "Maybe.",
            "Infact, you're right!",
            "Facts!",
            "I don't know, I'm just an 8ball",
            "Use another 8ball I'm not worth it :(",
            "Probably not.",
            "Ofcourse not!",
            "No."
            "Never",
            "Suck it up #$&@%, Never Ever Ever Never Ever!"
        ]

        responses = random.choice(possibilities)
        if question.startswith("should") or question.startswith("did") or question.startswith("were") or question.startswith("may") or question.startswith("could") or question.startswith("would") or question.startswith("can") or question.startswith("is") or question.startswith("are") or question.startswith("will") or question.startswith("what") or question.startswith("do") or question.startswith("does") or question.startswith("am") or question.startswith("Should") or question.startswith("May") or question.startswith("Could") or question.startswith("Would") or question.startswith("Can") or question.startswith("Is") or question.startswith("Are") or question.startswith("Will") or question.startswith("What") or question.startswith("Do") or question.startswith("Does") or question.startswith("Am") or question.startswith("Did") or question.startswith("Were"):
            if question.endswith("?"):

                e = nextcord.Embed(title="The 8ball has spoken", color = nextcord.Color.random(), timestamp=datetime.datetime.utcnow())
                e.add_field(name="Question:", value=f"{question}")
                e.add_field(name="🎱 Answer:", value=f"🎱 {responses}", inline=False)

            else:

                e = nextcord.Embed(title="The 8ball has spoken", color = nextcord.Color.random(), timestamp=datetime.datetime.utcnow())
                e.add_field(name="Question:", value=f"{question}?")
                e.add_field(name="Answer:", value=f"{responses}", inline=False)

            await interaction.response.send_message(embed=e)
            return
        
        else:

            await interaction.response.send_message("That could not have been a question, start with: \n`do`, `is`, `are`, `did`, `were`, `could`, `will`, `can`, `would`, `what`, `may`, `should`, `does` or `am`")

@client.slash_command(name="search", description="Search for coins all around the world!")
@commands.cooldown(1, 120, BucketType.user)
async def search(
    interaction: nextcord.Interaction, *, 
    where: str = nextcord.SlashOption(
        name="area",
        description="Where do you wanna search for money?",
        required=True
    )
):
    async with interaction.channel.typing():
        member = interaction.user
        findbank = await collection.find_one({"_id": member.id})
        if not findbank:
            await collection.insert_one({"_id": member.id, "wallet": 0, "bank": 0})

        wallet = findbank["wallet"]
        f = random.randint(1, 101)
        earnings = random.randint(1, 1001)
        jackpot = random.randint(21000, 30001)
        jackpot_e = wallet + jackpot
        earnings_e = wallet + earnings

        if where == "park":
            if f > 50:
                e = nextcord.Embed(
                    title="Hooray!",
                    description="You searched the park and found a wallet with ${:,}!".format(earnings),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": earnings_e}})

            elif f == 50:
                e = nextcord.Embed(
                    title="HOLY-",
                    description="You searched the park and found a wallet with ${:,}!".format(jackpot),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": jackpot_e}})

            else:

                e = nextcord.Embed(
                    title="ooh-",
                    description=f"You searched the park and found nothing.",
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

            await interaction.response.send_message(embed=e)
            return

        elif where == "closet":
            if f > 50:
                e = nextcord.Embed(
                    title="Hooray!",
                    description="You searched your closet and found ${:,}!".format(earnings),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": earnings_e}})

            elif f == 50:
                e = nextcord.Embed(
                    title="HOLY-",
                    description="You searched your closet and found ${:,}!".format(jackpot),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": jackpot_e}})

            else:

                e = nextcord.Embed(
                    title="ooh-",
                    description=f"You searched your closet and found nothing but clothes.",
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return

        elif where == "bed":
            if f > 50:
                e = nextcord.Embed(
                    title="Hooray!",
                    description="You searched under your bed and found ${:,}!".format(earnings),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": earnings_e}})

            elif f == 50:
                e = nextcord.Embed(
                    title="HOLY-",
                    description="You searched under your bed and found ${:,}!".format(jackpot),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": jackpot_e}})

            else:

                e = nextcord.Embed(
                    title="ooh-",
                    description=f"You searched under your bed and found a monster :joy:, just kidding but you found nothing.",
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return

        elif where == "company":
            if f > 50:
                e = nextcord.Embed(
                    title="Hooray!",
                    description="You searched your company and found a wallet with ${:,}!".format(earnings),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": earnings_e}})

            elif f == 50:
                e = nextcord.Embed(
                    title="HOLY-",
                    description="You searched your company and found a wallet with ${:,}!".format(jackpot),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": jackpot_e}})

            else:
                e = nextcord.Embed(
                    title="oop-",
                    description=f"You searched your company and found nothing!",
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return

        elif where == "paypal":
            if f > 50:
                e = nextcord.Embed(
                    title="Hooray!",
                    description="You searched your paypal and found ${:,}!".format(earnings),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": earnings_e}})

            elif f == 50:
                e = nextcord.Embed(
                    title="HOLY-",
                    description="You searched your paypal that you literally never even use and found {:,}!".format(jackpot),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": jackpot_e}})

            else:

                e = nextcord.Embed(
                    title="ooh-",
                    description=f"You searched your paypal that you never use and found nothing.",
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return

        elif where == "car":
            if f > 50:
                e = nextcord.Embed(
                    title="Hooray!",
                    description="You searched your car and found a wallet with ${:,}!".format(earnings),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": earnings_e}})

            elif f == 50:
                e = nextcord.Embed(
                    title="HOLY-",
                    description="You searched your car and found a wallet with ${:,}!".format(jackpot),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": jackpot_e}})

            elif f < 50:

                e = nextcord.Embed(
                    title="ooh-",
                    description=f"You searched in the middle of the street and found nothing",
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return

        elif where == "dumpster":
            if f > 50:
                e = nextcord.Embed(
                    title="Hooray!",
                    description="You searched a dumpster and found a wallet with ${:,}!".format(earnings),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": earnings_e}})

            elif f == 50:
                e = nextcord.Embed(
                    title="HOLY-",
                    description="You searched a dumpster and found a wallet with ${:,}!".format(jackpot),
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": jackpot_e}})

            else:

                e = nextcord.Embed(
                    title="ooh-",
                    description=f"You searched a dumpster and found nothing, you kinda stink tho, lol.",
                    color=nextcord.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )

                await interaction.response.send_message(embed=e)
                return

        else:
            await interaction.response.send_message("Try /search `park`, `street`, `car`, `dumpster`, `company`, `paypal`")

@client.slash_command(name="afk", description="Make everyone know your away from keyboard!")
async def afk(
    interaction: nextcord.Interaction, 
    reason = nextcord.SlashOption(
        name="reason",
        description="What is the reason?",
        required=False
    )
):
    async with interaction.channel.typing():
        try:
            await interaction.user.edit(nick=f"[AFK] {interaction.user.name}", reason=reason)
        except Forbidden:
            await interaction.send("I didn't have permissions to nick you, tell the server owner to give me more permissions!")
            return

        em = nextcord.Embed(title=f"{interaction.user} has went AFK!", description="Just type anything or /unafk", timestamp=datetime.datetime.utcnow(), color = nextcord.Color.random())
        em.add_field(name="Reason:", value=f"{reason}")
        await interaction.response.send_message(embed=em)

        def check(m):
            return m.author == interaction.user

        raw_msg = await client.wait_for("message", check=check, timeout=None)
        msg = raw_msg.content

        if msg:
            em1 = nextcord.Embed(title=f"{interaction.user.name}#{interaction.user.discriminator} has UNAFKED!", description=f"Welcome back {interaction.user.mention}", timestamp=datetime.datetime.utcnow(), color = nextcord.Color.random())
            await interaction.send(embed=em1)

@client.slash_command(name="unafk", description="Make everyone know your not away from keyboard anymore!")
async def unafk(interaction: nextcord.Interaction):
    async with interaction.channel.typing():
        try:
            if "[AFK]" in interaction.user.display_name:
                await interaction.user.edit(nick=interaction.user.name)
            else:
                await interaction.send("You're not even afk.")
                return

        except Forbidden:
            await interaction.send("I don't have permissions to nickname you.")
        return

        em = nextcord.Embed(title=f"{interaction.user} has UNAFKED!", description=f"Welcome back {interaction.user.mention}", timestamp=datetime.datetime.utcnow(), color = nextcord.Color.random())
        await interaction.send(embed=em)

mainshop = [
    {
        "name": "Watch",
        "price": 100,
        "description": "Time"
    }, 
    {
        "name": "Laptop",
        "price": 1000,
        "description": "Work"
    }, 
    {
        "name": "PC",
        "price": 10000,
        "description": "Gaming"
    }, 
    {
        "name": 
        "Ferrari", 
        "price": 99999,
        "description": "Sports Car"
    }, 
    {
        "name": "Lucky Charm",
        "price": 10000000,
        "description": "This lucky charm gives you LUCK FOREVER!"
    }
]

petshop = [
    {
        "name": "Gorilla",
        "price": 70000,
        "description": "This angry gorilla will steal some money for you, It could sometimes fail, but don't let that haunt you from getting this masterpiece!",
    },
    {
        "name": "Elephant",
        "price": 950000,
        "description": "This special elephant will protect you from robbers and killers, have fun with it!",
    },
]

@client.slash_command(name="gay", description="Test people's gayness!")
async def gay(
    interaction: nextcord.Interaction, *, 
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who do you want to test gayness on?",
        required=False
    )
):
    async with interaction.channel.typing():
        if member == None:
            member = interaction.user
        

        k = random.randint(1, 101)

        if k > 50:
            em = nextcord.Embed(title=f"{member}'s Gay Result", description=f"{member.mention}'s Gay Result is {k}! \nYou are in 🏳️‍🌈!", color = nextcord.Color.random())
        else:
        
            em = nextcord.Embed(title=f"{member}'s Gay Result",description=f"{member.mention}'s Gay Result is {k}! \nCONGRATULATIONS on not being Gay! :tada: :tada:" ,color=nextcord.Color.random())
            await interaction.response.send_message(embed=em)

@client.slash_command(name="company", description="Company!")
async def company(interaction: nextcord.Interaction):
    pass

@company.subcommand(name="upgrade", description="Upgrade your company!")
async def company_upgrade(interaction):
    async with interaction.channel.typing():
        member = interaction.user
        findcompany = await companyaa.find_one({"_id": member.id})
        if not findcompany:
            await interaction.send("You currently don't have a company! You can create one by `/company create`.")

        findbank = await collection.find_one({"_id": member.id})
        if not findbank:
            await collection.insert_one({"_id": member.id, "wallet": 0, "bank": 0})

        wallet = findbank["wallet"]

        level = findcompany["level"]

        while level < 3:
            async def btncallback(interaction):
                if level == 1:
                    if wallet >= 35000:
                        await collection.update_one({
                                "_id": member.id
                            },

                            {
                                "$set": {
                                    "wallet": wallet - 35000
                                }
                            })

                        await companyaa.update_one({
                                "_id": member.id
                            },

                            {
                                "$set": {
                                    "level": level + 1
                                }
                            })

                        await interaction.send("Your company level has been upgraded to level 2!", ephemeral=True)
                        pass

                    else:
                        await interaction.send("You don't even have enough money.", ephemeral=True)
                        pass
                
                if level == 2:
                    if wallet >= 100000:
                        await collection.update_one({
                                "_id": member.id
                            },

                            {
                                "$set": {
                                    "wallet": wallet - 100000
                                }
                            })

                        await companyaa.update_one({
                                "_id": member.id
                            },

                            {
                                "$set": {
                                    "level": level + 1
                                }
                            })


                        await interaction.send("Your company level has been upgraded to level 2!", ephemeral=True)
                        pass

                    else:
                        await interaction.send("You don't even have enough money.", ephemeral=True)
                        pass

            async def btn2callback(interaction):
                await interaction.send("You have declined this.", ephemeral=True)
                pass

            button = Button(
                label="Yes",
                style=nextcord.ButtonStyle.green
            )

            button2 = Button(
                label="No",
                style=nextcord.ButtonStyle.red
            )

            button.callback = btncallback
            button2.callback = btn2callback
            view=View()
            view.add_item(button)
            view.add_item(button2) 
                
            embed = nextcord.Embed(
                title=f"Would you like to upgrade your company to level {level + 1:,}?",
                description="It'll cost $35,000.",
                color=nextcord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            ).set_thumbnail(url=interaction.user.avatar.url)
            await interaction.send(embed=embed, view=view)
            return

        else:
            await interaction.send("You hit the max level for your company, maybe stay tuned for more")

@company.subcommand(name="info", description="Information about your company!")
async def company_info(interaction):
    async with interaction.channel.typing():
        member = interaction.user
        findcompany = await companyaa.find_one({"_id": member.id})
        if not findcompany:
            await interaction.send("You don't have a company, create one with /company create.")

        worth = findcompany["worth"]
        level = findcompany["level"]
        name = findcompany["name"]
        embed = nextcord.Embed(
            title="{} information:".format(name),
            description="A list of information about your company",
            color=nextcord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )

        embed.add_field(
            name="Company Worth:",
            value=f"{round(worth)}",
        )

        embed.add_field(
            name="Company Level:",
            value=f"{int(level)}",
        )

        await interaction.send(embed=embed)

@company.subcommand(name="create", description="Create a company!")
async def company_create(interaction):
    async with interaction.channel.typing():
        member = interaction.user
        findcompany = await companyaa.find_one({"_id": member.id})
        if not findcompany:
            await interaction.send("What would you like to name your company? 1 minute to respond.")
            def check(m):
                return m.author == interaction.user

            try:
                raw_name = await client.wait_for("message", check=check, timeout=60.0)
                name = raw_name.content
            except asyncio.TimeoutError:
                await interaction.send("You ran out of time, rerun the command.")
                pass
            
            embed = nextcord.Embed(
                title=f"Company successfully created named {name}!", 
                description="Try using `/work` or company aliases.", 
                color=nextcord.Color.green(), 
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.send(embed=embed)

            await companyaa.insert_one({"_id": member.id, "name": str(name), "worth": 0, "level": 1})

        else:
            await interaction.send("You already have a company, no need for a new one!")

@client.slash_command(name="work", description="Work and get Money!")
async def work(interaction: nextcord.Interaction):
    await interaction.response.defer()
    async with interaction.channel.typing():
        user = interaction.user
        findbank = await collection.find_one({"_id": user.id})
        if not findbank:
            await collection.insert_one({"_id": user.id, "wallet": 0, "bank": 0})
            return

        findcompany = await companyaa.find_one({"_id": user.id})
        if not findcompany:
            await interaction.followup.send("You currently don't have a company! You can create one by `/company`.")

        wallet = findbank["wallet"]
        level = findcompany["level"]
        worthaa = findcompany["worth"]

        if level == 1:
            worth = random.randrange(float(100))
            earnings = random.randrange(1000, 10001)
        if level == 2:
            worth = random.randrange(float(250))
            earnings = random.randrange(1000, 15001)

        loss = random.randint(1000, 5000)
        a = random.randint(1, 101)

        if a > 75:
            embed = nextcord.Embed(
                title="oh shi-",
                description=f"You got absolutely nothing from working, actually you owe us ${loss:,}.",
                color=nextcord.Color.random(),
                timestamp=datetime.datetime.utcnow()
            )

            await interaction.followup.send(embed=embed)
            updated_coins = wallet - loss
            await collection.update_one({"_id": user.id}, {"$set": {"wallet": updated_coins}})

        else:
            embed2 = nextcord.Embed(
                title="Successful work", 
                description=f"You have made a total of `${earnings}` after a long day of work!", color=nextcord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.followup.send(embed=embed2)
            updated_coins = wallet + earnings
            updated_worth = worthaa + round(worth)
            await collection.update_one({"_id": user.id}, {"$set": {"wallet": updated_coins}})
            await companyaa.update_one({"_id": user.id}, {"$set": {"worth": updated_worth}})
            
@client.slash_command(name="credits", description="List of people who helped.")
async def credits(interaction: nextcord.Interaction):
    async with interaction.channel.typing():

        em = nextcord.Embed(title="Credits", description="These are a list of people who helped with the bot", color=nextcord.Color.random())
        em.add_field(name="Special thanks to:", value="vAdrian#2839 \n AarushOS#6676", inline=False)
        em.add_field(name="Thanks to:", value="All the people on my nextcord server and all my players on my bot. :D")

        await interaction.response.send_message(embed=em)

@client.slash_command(name="discordserv", description="Get the link to the discord server")
async def nextcordserv(interaction: nextcord.Interaction):
    await interaction.response.send_message("Look in my bio. :D")

class Confirm(View):
    def __init__(self):
        super().__init__()
        self.value = None

    @button(label='Confirm', style=nextcord.ButtonStyle.green)
    async def confirm(self, button: Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("You have confirmed this withdraw!", ephemeral=True)
        self.value = True
        self.stop()

    @button(label='Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button: Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("You have cancelled this withdraw!", ephemeral=True)
        self.value = False
        self.stop()

@client.slash_command(
    name="withdraw", 
    description="Withdraw some money to your wallet!"
)
async def withdraw(
    interaction: nextcord.Interaction, 
    amount: int = nextcord.SlashOption(
        name="amount",
        description="How much do you want to withdraw?",
        required=True
    )
):
    async with interaction.channel.typing():
        member = interaction.user
        findbank = await collection.find_one({"_id": member.id})
        if not findbank:
            await collection.insert_one({"_id": member.id, "wallet": 0, "bank": 0})

        wallet = findbank["wallet"]
        bank = findbank["bank"]
        if amount == 'all':
            if int(bank) > 0:
                amount = int(bank)
            else:
                await interaction.response.send_message("You don't have any funds in your Credit Card.")

        if amount > int(bank):
            await interaction.response.send_message("You have insufficient funds in your Credit Card.")
            return

        if amount < 0:
            await interaction.response.send_message("Your amount must be positive.")
            return

        else:

            view=Confirm()
            await interaction.response.send_message("Are you sure you want to do this?", view=view)
            await view.wait()
            if view.value is None:
                return
            elif view.value:

                updated_wallet = wallet + amount
                updated_bank = bank - amount
                await collection.update_one({"_id": member.id}, {"$set": {"wallet": updated_wallet}})
                await collection.update_one({"_id": member.id}, {"$set": {"bank": updated_bank}})

                await interaction.response.send_message("You withdrew ${:,} coins from your Credit Card, {}!".format(amount, interaction.user.mention), ephemeral=True)

            else:
                await interaction.response.send_message("You have cancelled this withdraw!", ephemeral=True)

class TicTacToeButton(Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=nextcord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = nextcord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = nextcord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)

class TicTacToe(View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

@client.slash_command(
    name="tic",
    description="Tic Tac Toe!"
)
async def tic(interaction: nextcord.Interaction):
    async with interaction.channel.typing():
        await interaction.response.send_message('Tic Tac Toe: X goes first', view=TicTacToe())

@client.slash_command(
    name="rob", 
    description="Rob some innocent people!"
)
@commands.cooldown(1, 180, BucketType.user) 
async def rob(interaction: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(name="member", description="Who is the unlucky person?", required=True)):
    async with interaction.channel.typing():
        fmb = await collection.find_one({"_id": member.id})
        fb = await collection.find_one({"_id": interaction.user.id})
        if not fmb:
            await collection.insert_one({"_id": interaction.user.id, "wallet": 0, "bank": 0})

        mwallet = fmb["wallet"]
        wallet = fb["wallet"]

        if member == interaction.user:
            em = nextcord.Embed(
                title="Error:",
                description="You can't rob yourself!",
                color=nextcord.Color.red(),
                timestamp=datetime.datetime.utcnow() 
            )
            await interaction.send(embed=em)
            pass

        elif int(fmb["wallet"]) < 1500:
            em = nextcord.Embed(
                title="Error:",
                description="Not worth the risk man.",
                color=nextcord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )

            await interaction.send(embed=em)
            pass

        elif int(fb["wallet"]) < 1500:
            em = nextcord.Embed(
                title="Error:",
                description="You don't have enough money (you need $1,500).",
                color=nextcord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )

            await interaction.send(embed=em)
            pass

        else:
            chance = [False, True, True, False, False, True, False, False, True, False, True, True]

            chances = random.choice(chance)
            earnings = random.randrange(int(0.65*int(mwallet)))
            loss = random.randrange(int(0.35*int(wallet)))

            if chances == True:
                earningsa = wallet + earnings
                lossa = mwallet - earnings
                await collection.update_one({"_id": interaction.user.id}, {"$set": {"wallet": earningsa}})
                await collection.update_one({"_id": member.id}, {"$set": {"bank": lossa}})
                em = nextcord.Embed(
                    title="Successful Robbery!",
                    description="You robbed {} and got ${:,}!".format(member.mention, earnings),
                    color = nextcord.Color.green(),
                    timestamp=datetime.datetime.utcnow()
                )
                em.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
                em.set_footer(text="He's so unlucky.", icon_url=member.avatar.url)

                await interaction.send(embed=em)

                em = nextcord.Embed(
                    title="You got robbed!",
                    description="You got robbed by {} and he got ${:,}!".format(member.mention, earnings),
                    color = nextcord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )

                em.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
                em.set_footer(text="You're so unlucky.", icon_url=member.avatar.url)

                await member.send(embed=em)

            else:
                earningsa = mwallet + loss
                lossa = wallet - loss
                await collection.update_one({"_id": interaction.user.id}, {"$set": {"wallet": lossa}})
                await collection.update_one({"_id": member.id}, {"$set": {"bank": earningsa}})
                em = nextcord.Embed(
                    title="Unuccessful Robbery!",
                    description="You **tried to** rob {} and lost ${:,}!".format(member.mention, loss),
                    color = nextcord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                em.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
                em.set_footer(text="He's so lucky.", icon_url=member.avatar.url)

                await interaction.send(embed=em)

                em = nextcord.Embed(
                    title="You got robbed!",
                    description="You got robbed by {} but thats okay, \nHe failed and he had to pay ${:,} for his consequences!".format(interaction.user.mention, loss),
                    color = nextcord.Color.green(),
                    timestamp=datetime.datetime.utcnow()
                )

                em.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
                em.set_footer(text="You're so lucky.", icon_url=member.avatar.url)

                await member.send(embed=em)
        
@client.slash_command(
    name="emojify", 
    description="Turn numbers and letters into emojis",
)
async def emojify(
    interaction: nextcord.Interaction, *, 
    message = nextcord.SlashOption(
        name="message",
        description="What is your message?",
        required=True
    )
):
    async with interaction.channel.typing():
        emojis = []
        message = message.lower()
        for s in message:
            if s.isdecimal():
                num2emo = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
                emojis.append(f':{num2emo.get(s)}:')
            elif s.isalpha():
                emojis.append(f':regional_indicator_{s}:')
            else:
                emojis.append(s)

        await interaction.send(' '.join(emojis))

bullylink = [
    "https://media2.giphy.com/media/4zR888BBbyfiE/giphy.gif?cid=ecf05e47jpv8hofgict82ecd33u657m70h60l2hp4ooi5b3e&rid=giphy.gif&ct=g",
    "https://media0.giphy.com/media/xT5LMtZ06eAXSmftYs/200.gif?cid=ecf05e4713p77gk37gch6881lmfevdtrakkkf812qnooavcq&rid=200.gif&ct=g",
    "https://media2.giphy.com/media/j5QmKNxMNEy24wrr5R/200w.gif?cid=ecf05e4713p77gk37gch6881lmfevdtrakkkf812qnooavcq&rid=200w.gif&ct=g",
    "https://media2.giphy.com/media/vW6r05KjlTxRrvRjGo/100.gif?cid=ecf05e4713p77gk37gch6881lmfevdtrakkkf812qnooavcq&rid=100.gif&ct=g",
    "https://media2.giphy.com/media/j5QmKNxMNEy24wrr5R/200w.gif?cid=ecf05e4713p77gk37gch6881lmfevdtrakkkf812qnooavcq&rid=200w.gif&ct=g",
]

yeetlink = [
    "https://media1.giphy.com/media/j3p5J3EJvAJyJWXyZG/200w.gif?cid=ecf05e47wswqw7c55bqmi3v2wg9n2bmoonryzttm27qa4hts&rid=200w.gif&ct=v",
    "https://media0.giphy.com/media/xCyjMEYF9H2ZcLqf7t/200w.gif?cid=ecf05e47o1o380lro3vi7evf8cahipozzmsayfzaucow7ntz&rid=200w.gif&ct=g",
    "https://media4.giphy.com/media/4EEIsDmNJCiNcvAERe/200w.gif?cid=ecf05e47o1o380lro3vi7evf8cahipozzmsayfzaucow7ntz&rid=200w.gif&ct=g",
    "https://media4.giphy.com/media/NThOsGBwbZi8qaEear/200w.gif?cid=ecf05e472rq89p2gks5vbcy0ne0vok4ug8zp38cylq4pnsd5&rid=200w.gif&ct=g",
    "https://media4.giphy.com/media/5PhDdJQd2yG1MvHzJ6/giphy.gif?cid=ecf05e47b6g62pr0saw4hpkbsc4rz4mbibhc0cneora13jto&rid=giphy.gif&ct=g",
]

kisslink = [
    "https://media1.giphy.com/media/4a6hs4izxxEpCR4nvA/200w.gif?cid=ecf05e477wjoasz9z41xq1kjd8m09ck0g1i5959no0obkqvl&rid=200w.gif&ct=v",
    "https://media0.giphy.com/media/3o72F3zlbWvP4kJp4c/200.gif?cid=ecf05e47ixnjozuwj65chepdus8yujt2tp6ddlu8ndfclb61&rid=200.gif&ct=g",
    "https://media4.giphy.com/media/26tjZKoo8gwbugbsc/200.gif?cid=ecf05e47s6h3682l25uemrbezlzee47zqztki9w9rsq583tm&rid=200.gif&ct=g",
    "https://media4.giphy.com/media/3o7TKqhF898sKm6opy/200w.gif?cid=ecf05e47s6h3682l25uemrbezlzee47zqztki9w9rsq583tm&rid=200w.gif&ct=g",
    "https://media2.giphy.com/media/l2Jhok92mZ2PZHjDG/giphy.gif?cid=ecf05e47z92betjirr7mtzp3d0s8pkr8x5hx7nntly9jst3g&rid=giphy.gif&ct=g",
]

shootlink = [
    "https://media4.giphy.com/media/9umH7yTO8gLYY/200.gif?cid=ecf05e47oukjlbyuwatzf0ex7te6gklxa5hk898q03ne1v6u&rid=200.gif&ct=g",
    "https://media3.giphy.com/media/cS9lGF8gIBdQs/200.gif?cid=ecf05e47oukjlbyuwatzf0ex7te6gklxa5hk898q03ne1v6u&rid=200.gif&ct=g",
    "https://media2.giphy.com/media/Bm6jGUsWDBrHy/200.gif?cid=ecf05e47oukjlbyuwatzf0ex7te6gklxa5hk898q03ne1v6u&rid=200.gif&ct=g",
    "https://media0.giphy.com/media/l4nlWhecm3qN6cYtO9/200w.gif?cid=ecf05e47k1cams6bspui695cpimnr5hjaay66yibx00xmp55&rid=200w.gif&ct=g",
    "https://media2.giphy.com/media/wTZLkZNqI6QYz5cjjG/200w.gif?cid=ecf05e47elj4bczmdlq0ay049ine3vw3kpticwnso5mp81w3&rid=200w.gif&ct=g",
]

stablink = [
    "https://media4.giphy.com/media/3o6gE2MlZupcFIEMP6/200w.gif?cid=ecf05e479afjj0bar8pfcdga9kkvbt0bqk1w4lq7qe3y3j9l&rid=200w.gif&ct=g",
    "https://media3.giphy.com/media/RGecJFMSrMTZz4satb/200.gif?cid=ecf05e479v2f59xzdsy0e8jzymfpnbf2njkr389dg3zbt4vb&rid=200.gif&ct=g",
    "https://media4.giphy.com/media/3orif0HPtMKPs8su6Q/200.gif?cid=ecf05e474z9z804ymcmcivg9nxyt6ocrnaibjvotmgfpolel&rid=200.gif&ct=g",
    "https://media2.giphy.com/media/3o6ozCytqK9iZYgoVO/200w.gif?cid=ecf05e474z9z804ymcmcivg9nxyt6ocrnaibjvotmgfpolel&rid=200w.gif&ct=g",
    "https://media2.giphy.com/media/26grAXwZFhA8kyT60/200w.gif?cid=ecf05e4789n95kh60bvyf6dc0fovfocgu4bzufugv2uqmfnd&rid=200w.gif&ct=g",
]

slaplink = [
    "https://media2.giphy.com/media/Ql5voX2wAVUYw/giphy.gif?cid=ecf05e47hrghq60mnybqyjd8apk4d94nadpr0drm9aqw3thv&rid=giphy.gif&ct=g",
    "https://media1.giphy.com/media/Qvwc79OfQOa4g/200.gif?cid=ecf05e47hrghq60mnybqyjd8apk4d94nadpr0drm9aqw3thv&rid=200.gif&ct=g",
    "https://media2.giphy.com/media/s5zXKfeXaa6ZO/giphy.gif?cid=ecf05e47hrghq60mnybqyjd8apk4d94nadpr0drm9aqw3thv&rid=giphy.gif&ct=g",
    "https://media4.giphy.com/media/3XlEk2RxPS1m8/200.gif?cid=ecf05e47hrghq60mnybqyjd8apk4d94nadpr0drm9aqw3thv&rid=200.gif&ct=g",
    "https://media4.giphy.com/media/uG3lKkAuh53wc/giphy.gif?cid=ecf05e47bra41jymi3e9k5c57msc20dt2p6le7cg51ac9va1&rid=giphy.gif&ct=g",
]

huglink = [
    "https://media3.giphy.com/media/26wkBtoUrZwYnFLWg/200w.gif?cid=ecf05e47m1ivohv3jn16s7oqttpd6f336uc07lyxo3txzkk7&rid=200w.gif&ct=g",
    "https://media1.giphy.com/media/kggfTFCnrAFJSf8JL8/100.gif?cid=ecf05e47m1ivohv3jn16s7oqttpd6f336uc07lyxo3txzkk7&rid=100.gif&ct=g",
    "https://media2.giphy.com/media/bvFS4rALdNDag/giphy.gif?cid=ecf05e47m1ivohv3jn16s7oqttpd6f336uc07lyxo3txzkk7&rid=giphy.gif&ct=g",
    "https://media3.giphy.com/media/EvYHHSntaIl5m/giphy.gif?cid=ecf05e4717ahvmvv2sk76ayh7g6ge9wgearxeikx8crrrc4t&rid=giphy.gif&ct=g",
    "https://media1.giphy.com/media/llmZp6fCVb4ju/giphy.gif?cid=ecf05e47yllvta0wslwqux53gmkrsfgn8ieg5om7fpwllgyx&rid=giphy.gif&ct=g",
]

@client.slash_command(
    name="bully", 
    description="Bully some kids, hehe ;D",
)
async def bully(
    interaction: nextcord.Interaction, 
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who is the unlucky person?",
        required=True
    )
):
    async with interaction.channel.typing():
        embed = nextcord.Embed(title=f"You are bullying {member}!", description=f"You have bullied {member.mention} {interaction.user.mention}.", color = nextcord.Color.random())
        embed.set_image(url=random.choice(bullylink))
        await interaction.response.send_message(embed=embed)

@client.slash_command(name="yeet", description="Yeet some kids, hehe ;D")
async def yeet(
    interaction: nextcord.Interaction, 
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who is the unlucky person?",
        required=True
    )
):
    async with interaction.channel.typing():
        embed = nextcord.Embed(title=f"You are yeeting {member}!", description=f"You have yeeted {member.mention} {interaction.user.mention}.", color = nextcord.Color.random())
        embed.set_image(url=random.choice(yeetlink))
        await interaction.response.send_message(embed=embed)

@client.slash_command(name="kiss", description="Kiss someone.")
async def kiss(
    interaction: nextcord.Interaction, 
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who is the lucky person?",
        required=True
    )
):
    async with interaction.channel.typing():
        embed = nextcord.Embed(title=f"You are kissinging {member}!", description=f"You have kissed {member.mention} {interaction.user.mention}.", color = nextcord.Color.random())
        embed.set_image(url=random.choice(kisslink))
        await interaction.response.send_message(embed=embed)

@client.slash_command(name="shoot", description="Shoot some kids, hehe ;D")
async def shoot(
    interaction: nextcord.Interaction, 
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who is the unlucky person?",
        required=True
    )
):
    async with interaction.channel.typing():
        embed = nextcord.Embed(title=f"You are shooting {member}!", description=f"You have shot {member.mention} {interaction.user.mention}.", color = nextcord.Color.random())
        embed.set_image(url=random.choice(shootlink))
        await interaction.response.send_message(embed=embed)

@client.slash_command(name="stab", description="Stab some kids, hehe ;D")
async def stab(
    interaction: nextcord.Interaction, 
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who is the unlucky person?",
        required=True
    )
):
    async with interaction.channel.typing():
        embed = nextcord.Embed(title=f"You are stabing {member}!", description=f"You have stabbed {member.mention} {interaction.user.mention}.", color = nextcord.Color.random())
        embed.set_image(url=random.choice(stablink))
        await interaction.response.send_message(embed=embed)

@client.slash_command(name="slap", description="Slap some kids, hehe ;D")
async def slap(
    interaction: nextcord.Interaction, 
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who is the unlucky person?",
        required=True
    )
):
    async with interaction.channel.typing():
        embed = nextcord.Embed(title=f"You are slapping {member}!", description=f"You have slapped {member.mention} {interaction.user.mention}.", color = nextcord.Color.random())
        embed.set_image(url=random.choice(slaplink))
        await interaction.response.send_message(embed=embed)

@client.slash_command(name="hug", description="Hug some people.")
async def hug(
    interaction: nextcord.Interaction, 
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who is the unlucky person?",
        required=True
    )
):
    async with interaction.channel.typing():
        embed = nextcord.Embed(title=f"You are hugging {member}!", description=f"You have hugged {member.mention} {interaction.user.mention} :D.", color = nextcord.Color.random())
        embed.set_image(url=random.choice(huglink))
        await interaction.response.send_message(embed=embed)

@client.slash_command(name="say", description="Make the bot say anything!")
async def say(interaction: nextcord.Interaction, message = nextcord.SlashOption(description="What is the message?")):
    async with interaction.channel.typing():
        await interaction.send(f"{message}")

@client.slash_command(name="rps", description="Rock Paper Scissors")
async def rps(interaction: nextcord.Interaction, mode = nextcord.SlashOption(description="What mode? rock, paper, scissors?", required=True)):
    s = ["scissors","Scissors"]
    p = ["paper","Paper"]
    r = ["rock","Rock"]

    z = ["scissors","Scissors","paper","Paper","rock","Rock"]

    b = ["scissors","paper","rock"]
    b2 = random.choice(b)

    if mode not in z:
        await interaction.send("You can only do *scissors*, *paper* or *rock*!")
        return

    if b2 == "scissors":
        if mode in s:
            await interaction.send(f"My choice was scissors aswell, So It was a tie!")
        if mode in p:
            await interaction.send(f"My choice was scissors, so you lost! :rofl:")
        if mode in r:
            await interaction.send(f"My choice was scissors, so you won! :sob:")

    if b2 == "paper":
        if mode in s:
            await interaction.send(f"My choice was paper, so you won! :sob:")
        if mode in p:
            await interaction.send(f"My choice was paper aswell, So It was a tie!")
        if mode in r:
            await interaction.send(f"My choice was paper, so you lost! :rofl:")

    if b2 == "rock":
        if mode in s:
            await interaction.send(f"My choice was rock, so you lost! :rofl:")
        if mode in p:
            await interaction.send(f"My choice was rock! You won! :sob:")
        if mode in r:
            await interaction.send(f"My choice was rock aswell, So It was a tie!")

@client.slash_command(name="casino", description="Casino some money!")
async def casino(
    interaction: nextcord.Interaction, 
    amount = nextcord.SlashOption(
        name="amount",
        description="How much do you want to bet?",
        required=True
    )
):
    async with interaction.channel.typing():
        user = interaction.user
        findbank = await collection.find_one({"_id": user.id})
        if not findbank:
            await collection.insert_one({"_id": user.id, "wallet": 0, "bank": 0})

        wallet = findbank["wallet"]

        amount = int(amount)

        if amount > int(wallet):
            await interaction.send('You do not have sufficient balance')
            return

        if amount < 0:
            await interaction.send('Amount must be positive!')
            return

        final = []
        for i in range(0, 3):
            a = random.choice(['X','O','Q'])

            final.append(a)

        if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
            uw = wallet + amount
            await collection.update_one({"_id": interaction.user.id}, {"$set": {"wallet": uw}})
            await interaction.send(f'You won {amount} {user.mention}!')
        else:
            uw = wallet - amount
            await collection.update_one({"_id": interaction.user.id}, {"$set": {"wallet": uw}})
            await interaction.send(f'You lose {amount} {user.mention}!')

@client.slash_command(name="shop", description="Look at the Shop!")
async def shop(interaction: nextcord.Interaction):
    async with interaction.channel.typing():
        em = nextcord.Embed(title="Shop", color=nextcord.Color.blue())

        for item in mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name=f"{name}", value="${:,} | {}".format(price, desc), inline=False)

        await interaction.send(embed=em)

@client.slash_command(name="buy", description="Buy something from the shop!")
async def buy(interaction: nextcord.Interaction, item = nextcord.SlashOption(description="What is the item?"), amount: int = nextcord.SlashOption(description="How much of that item?")):
    async with interaction.channel.typing():
        await open_account(interaction.user)

        res = await buy_this(interaction.user,item,amount)

        if not res[0]:
            if res[1]==1:
                await interaction.send("That Object isn't there!")
                return
            elif res[1]==2:
                await interaction.send(f"You don't have enough money in your wallet to buy {amount} {item}")
                return

            else:
                await interaction.send(f"You just bought {item} for ${amount}!")

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,-1*cost,"wallet")

    return [True,"Worked"]


@client.slash_command(name="bag", description="What do we have here?")
async def bag(interaction: nextcord.Interaction):
    async with interaction.channel.typing():
        await open_account(interaction.user)
        user = interaction.user
        users = await get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []


        em = nextcord.Embed(title = "Bag")
        for item in bag:
            name = item["item"]
            amount = item["amount"]

            em.add_field(name = name, value = amount)    

        await interaction.send(embed=em)

@client.slash_command(name="sell", description="Sell something to the shop!")
async def sell(interaction: nextcord.Interaction, item = nextcord.SlashOption(description="What is the item?"), amount = nextcord.SlashOption(description="How much of that?")):
    async with interaction.channel.typing():
        await open_account(interaction.user)

        res = await sell_this(interaction.user,item,amount)

        if not res[0]:
            if res[1]==1:
                await interaction.send("That Object isn't there!")
                return
            if res[1]==2:
                await interaction.send(f"You don't have {amount} {item} in your bag.")
                return
            if res[1]==3:
                await interaction.send(f"You don't have {item} in your bag.")
                return

        await interaction.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.7* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

@client.slash_command(name="lb", description="Leaderboard of people, ranked by money!")
async def lb(interaction: nextcord.Interaction):
    x: int = 10
    async with interaction.channel.typing():
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total, reverse=True)

        em = nextcord.Embed(title=f"Top {x} Richest People", description="This is decided on the basis of raw money in the wallet and bank.", color=nextcord.Color.blurple())
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = await interaction.guild.fetch_member(id_)
            name = member.name
            em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
            if index == x:
                break
            else:
                index += 1
        await interaction.send(embed=em)

@client.slash_command(name="info", description="Info about someone!")
async def info(
    interaction: nextcord.Interaction, 
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who do you want to check information on?",
        required=False
    )
):
    async with interaction.channel.typing():
        if member == None:
            user = interaction.user
        else:
            user = member

        roles = [role for role in user.roles]

        isBot = user.bot
        if isBot == True:
            isBot = "BOT"
        else:
            isBot = "Member"

        embed = nextcord.Embed(title=f"Information on {user}.", color=user.color)
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        embed.set_footer(text=f"Requested by: {interaction.user}", icon_url=interaction.user.avatar.url)
        embed.add_field(name="ID:", value=user.id, inline=True)
        embed.add_field(name="Member Nickname:", value=user.nick, inline=True)
        embed.add_field(name="Current Status:",
                        value=str(user.status).title(),
                        inline=True)
        embed.add_field(
            name="Current Activity:",
            value=
            f"{str(user.activity.type).title().split('.')[1]}: {user.activity.name}"
            if user.activity is not None else "None",
            inline=True)
        embed.add_field(
            name="Account created at:",
            value=user.created_at.strftime("%A %B %-d, %Y, %-I:%M %p %Z"),
            inline=True)
        embed.add_field(
            name="Server joined at:",
            value=user.joined_at.strftime("%A %B %-d, %Y, %-I:%M %p %Z"),
            inline=True)
        embed.add_field(name=f"Roles [{len(roles)}]",
                        value=" **|** ".join([role.mention for role in roles]),
                        inline=True)
        embed.add_field(name="Major Role:", value=user.top_role, inline=True)
        embed.add_field(name="Type:", value=isBot, inline=True)
        await interaction.response.send_message(embed=embed)
        return

@client.slash_command(name="cc", description="Create a category!")
async def cc(interaction: nextcord.Interaction, name = nextcord.SlashOption(description="What is the name?")):
    if not (interaction.user.guild_permissions.manage_channels):
        await interaction.response.send_message("You can't use this.", ephemeral=True)
        pass

    else:
        async with interaction.channel.typing():

            await interaction.guild.create_category(name)
            await interaction.send(f"created category {name}")

@client.slash_command(name="ctc", description="Create a text channel!")
async def ctc(interaction: nextcord.Interaction, name = nextcord.SlashOption(description="What is the name?")):
    if not (interaction.user.guild_permissions.manage_channels):
        await interaction.response.send_message("You can't use this.", ephemeral=True)
        pass

    else:
        async with interaction.channel.typing():

            await interaction.guild.create_text_channel(name)
            await interaction.send(f"created text channel {name}")

@client.slash_command(name="cvc", description="Create a voice channel!")
async def cvc(interaction: nextcord.Interaction, *, name = nextcord.SlashOption(description="What is the name?")):
    if not (interaction.user.guild_permissions.manage_channels):
        await interaction.response.send_message("You can't use this.", ephemeral=True)
        pass

    else:
        async with interaction.channel.typing():
        
            await interaction.guild.create_voice_channel(name)
            await interaction.send(f"created voice channel {name}")

@client.slash_command(name="ar", description="Add a role to Someone!")
async def ar(interaction: nextcord.Interaction, *, user: nextcord.Member = nextcord.SlashOption(description="Who is the person?"), role: nextcord.Role = nextcord.SlashOption(description="What is the role?")):
    if not (interaction.user.guild_permissions.manage_roles):
        await interaction.response.send_message("You can't use this.", ephemeral=True)
        pass

    else:
        async with interaction.channel.typing():
        
            if role in user.roles:
                await interaction.send(f"{user} already has this role called {role}.")
                return
            else:
                await user.add_role(role)
                await interaction.send(f"Added {role} to {user.mention}.")

@client.slash_command(name="rr", description="Remove a role from Someone!")
async def rr(interaction: nextcord.Interaction, *, user: nextcord.Member = nextcord.SlashOption(description="Who is the person?"), role: nextcord.Role = nextcord.SlashOption(description="What is the role?")):
    if not (interaction.user.guild_permissions.manage_roles):
        await interaction.response.send_message("You can't use this.", ephemeral=True)
        pass

    else:
        async with interaction.channel.typing():

            if role not in user.roles:
                await interaction.send(f"{user} already doesn't have this role called {role}.")
                return
            else:
                await user.remove_role(role)
                await interaction.send(f"Removed {role} to {user.mention}.")

Facts = [
    "Over 550 million heartbeats happen every 1 minute and it keeps increasing.",
    "McDonald’s once made bubblegum-flavored broccoli",
    "Some fungi create zombies, then control their minds",
    "The first oranges weren’t orange",
    "There’s only one letter that doesn’t appear in any U.S. state name",
    "A cow-bison hybrid is called a **beefalo**"
]

Dadjokes = [
    "Why did the orange lose the race? It ran out of juice.",
    "How you fix a broken pumpkin? With a pumpkin patch.",
    "Why are fish so smart? They live in schools!",
    "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
    "Why did the man fall down the well? Because he couldn’t see that well!",
    "Why do peppers make such good archers? Because they habanero.",
    "What did the sink tell the toilet? You look flushed!",
    "Where do boats go when they're sick? To the dock.",
    "What has ears but cannot hear? A cornfield!",
    "Stop looking for the perfect match; use a lighter.",
    "Can February March? No, but April May!",
    "Why was 6 afraid of 7? Because 7 ate nine!",
    "I'm so good at sleeping that I do it with my eyes closed.",
    "Try the seafood diet—you see food, then you eat it.",
    "What do you call a pencil with two erasers? Pointless.",
    "Did you hear the one about the roof? Never mind, it's over your head.",
    "What's brown and sticky? A stick.",
    "I hated facial hair but then it grew on me.",
    "It really takes guts to be an organ donor.",
    "Did you hear the rumor about butter? Well, I'm not going to go spreading it!",
    "What did the plumber say to the singer? Nice pipes.",
    "I was going to tell a time-traveling joke, but you didn't like it.",
    "How do you deal with a fear of speed bumps? You slowly get over it.",
    "I ordered a chicken and an egg online. I'll let you know.",
    "I'm reading an anti-gravity book. I can't put it down!",
    "I'd avoid the sushi if I were you. It's a little fishy!",
    "What state is known for its small drinks? Minnesota.",
    "What's Forrest Gump's password? 1forrest1",
    "What do houses wear? An address.",
    "What did the two pieces of bread say on their wedding day? It was loaf at first sight.",
    "What kind of shoes does a lazy person wear? Loafers.",
    "What did the ocean say to the beach? Nothing, it just waved.",
    "What happens when a snowman throws a tantrum? He has a meltdown."
]

@client.slash_command(name="clear", description="Clear messages!")
async def clear(
    interaction: nextcord.Interaction, 
    amount: int = nextcord.SlashOption(
        name="amount",
        description="How many messages do you want to delete?",
        required=True
    ),
):
    async with interaction.channel.typing():
        if not (interaction.user.guild_permissions.manage_channels):
            await interaction.response.send_message("You can't use this as you don't have `manage channels` perission.", ephemeral=True)
            return

        else:

            amount = amount + 1
            if amount > 101:
                await interaction.response.send_message("{} needs to be under 101 at least.".format(amount - 1), ephemeral=True)
                return

            if amount <= 0:
                await interaction.response.send_message("{} needs to be above 0 at least.".format(amount - 1), ephemeral=True)
                return

            await interaction.channel.purge(limit=amount)
            em = nextcord.Embed(title=f"{amount} message(s) has been deleted", description="Use /clear <amount> to use this command again!", color=nextcord.Color.green())
            await interaction.send(embed=em)
            await asyncio.sleep(5)
            await (await interaction.original_message()).delete()
            return

@client.slash_command(name="poll", description="Make a Poll!")
async def poll(
    interaction: nextcord.Interaction, 
    topic = nextcord.SlashOption(
        name="topic",
        description="What is the topic of this poll?",
        required=True,
    ), 
    choice1 = nextcord.SlashOption(
        name="choice1",
        description="First Choice.",
        required=True 
    ), 
    choice2 = nextcord.SlashOption(
        name="choice2",
        description="Second Choice.",
        required=True,
    ),
    c3 = nextcord.SlashOption(
        name="choice3",
        description="Third Choice.",
        required=False,
    ),
    c4 = nextcord.SlashOption(
        name="choice4",
        description="Fourth Choice.",
        required=False,
    ),
    c5 = nextcord.SlashOption(
        name="choice5",
        description="Fifth Choice.",
        required=False,
    ),
    c6 = nextcord.SlashOption(
        name="choice6",
        description="Sixth Choice.",
        required=False,
    ),
    c7 = nextcord.SlashOption(
        name="choice7",
        description="Seventh Choice.",
        required=False,
    ),
    c8 = nextcord.SlashOption(
        name="choice8",
        description="Eighth Choice.",
        required=False,
    ),
    c9 = nextcord.SlashOption(
        name="choice9",
        description="Ninth Choice.",
        required=False,
    ),
    c10 = nextcord.SlashOption(
        name="choice10",
        description="Tenth Choice.",
        required=False,
    ),
):
    async with interaction.channel.typing():
        choices = [choice1, choice2, c3, c4, c5, c6, c7, c8, c9, c10]
        choice_reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        embed = nextcord.Embed(
            title=topic,
            description="",
            color=nextcord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name="Requested by " + interaction.user.name, icon_url=interaction.user.avatar.url)
        options = [c for c in choices if c is not None]
        optionreaction = [cr for cr in choice_reactions if options is not None]

        for i in range(0, len(options)):
            embed.description += f'{optionreaction[i]} {options[i]}\n'

        await interaction.send(embed=embed)

        embed_msg = (await interaction.original_message())

        for i in range(0, len(options)):
            await embed_msg.add_reaction(optionreaction[i])

    return

@client.slash_command(name="kick", description="Kick someone!")
async def kick(
    interaction: nextcord.Interaction, 
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who do you want to kick?",
        required=True
    ),

    reason = nextcord.SlashOption(
        name="reason",
        description="What is the reason of kicking this member?",
        required=False
    ),
):
    async with interaction.channel.typing():
        if not (interaction.user.guild_permissions.kick_members):
            await interaction.response.send_message("You can't use this.", ephemeral=True)
            pass
            
        else:
            if member == interaction.user:

                await interaction.send("You can't kick yourself!")
                return
            else:
                await member.kick(reason=reason)
                embed2 = nextcord.Embed(
                    title=f"Kicked {member.name}!", 
                    description="Information about the kicked user.", 
                    color=nextcord. Color.red()
                )
                embed2.add_field(
                    name="**Kicked by:**", 
                    value=f"{interaction.user.mention}", 
                    inline=False
                )
                embed2.add_field(
                    name="**Kicked from**", 
                    value=f"{interaction.guild}", 
                    inline=False
                )
                embed2.add_field(
                    name="**Kicked for:**", 
                    value=f"{reason}", 
                    inline=False
                )
                await interaction.send(embed=embed2)
                em = nextcord.Embed(
                    title="You were kicked!", 
                    description="Information about you.", 
                    color=nextcord.Color.red()
                )
                em.add_field(
                    name="**Kicked by:**", 
                    value=f"{interaction.user.mention}", 
                    inline=False
                )
                em.add_field(
                    name="**Kicked from:**", 
                    value=f"{interaction.guild}", 
                    inline=False
                )
                em.add_field(
                    name="**Kicked for:**", 
                    value=f"{reason}", 
                    inline=False    
                )
                await member.send(embed=em)

@client.slash_command(name="ban", description="Ban someone!")
async def ban(interaction: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(description="Who is the person?"), *, reason=nextcord.SlashOption(description="What is the person?")):
    async with interaction.channel.typing():
        if not (interaction.user.guild_permissions.ban_members):
            await interaction.response.send_message("You can't use this.", ephemeral=True)
            pass

        else:

            if member == interaction.user:

                await interaction.send("You can't ban yourself!")
                return
            else:
                await member.ban(reason=reason)
                embed2 = nextcord.Embed(
                    title=f"Banned {member.name}!", 
                    description="Information about the banned user.", color=nextcord.Color.red()
                )
                embed2.add_field(
                    name="**Banned by:**", 
                    value=f"{interaction.user.mention}", 
                    inline=False
                )
                embed2.add_field(
                    name="**Banned from**", 
                    value=f"{interaction.guild}", 
                    inline=False
                )
                embed2.add_field(
                    name="**Banned for:**", 
                    value=f"{reason}", 
                    inline=False
                )
                await interaction.send(embed=embed2)
                em = nextcord.Embed(
                    title="You were Banned!", 
                    description="Information about you.", 
                    color=nextcord.Color.red()
                )
                em.add_field(
                    name="**Banned by:**", 
                    value=f"{interaction.user.mention}", 
                    inline=False
                )
                em.add_field(
                    name="**Banned from:**", 
                    value=f"{interaction.guild}", 
                    inline=False
                )
                em.add_field(
                    name="**Banned for:**", 
                    value=f"{reason}", 
                    inline=False
                )
                await member.send(embed=em)
            
@client.slash_command(name="mute", description="Mute someone!")
async def mute(
    interaction: nextcord.Interaction, 
    time = nextcord.SlashOption(
        name="time",
        description="How long do you want them muted?",
        required=True
    ), 

    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who is the member?",
        required=True
    ), 

    reason: str = nextcord.SlashOption(
        name="reason",
        description="What is the reason?",
        required=False
    )
):
    async with interaction.channel.typing():
        if not (interaction.user.guild_permissions.moderate_members):
            await interaction.response.send_message("You can't use this as you don't have `timeout members`.", ephemeral=True)
            pass

        else:

            if member == interaction.user:
                await interaction.send("You can\'t mute yourself!")
                return

            duration = humanfriendly.parse_timespan(time)
            await member.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=duration), reason=reason)
            embed = nextcord.Embed(
                title=f"Muted {member.name}!",
                description=f"Information about the muted user. ID: {member.id}",
                color=0xe40707
            )
            embed.add_field(
                name="**Muted by:**", 
                value=f"Username: {interaction.user.mention} ID: {interaction.user.id}",inline=False
            )
            embed.add_field(
                name="**Muted from**", 
                value=f"{interaction.guild}", 
                inline=False
            )
            embed.add_field(
                name="**Muted for:**", 
                value=f"{reason}", 
                inline=False
            )
            embed.add_field(
                name="**Time:**", 
                value=f"{time}", 
                inline=False
            )

            await interaction.send(embed=embed)
            embed = nextcord.Embed(
                title=f"You were muted!",
                description=f"Information about you. ID: {member.id}",
                color=0xe40707
            )
            embed.add_field(
                name="**Muted by:**", 
                value=f"Username: {interaction.user.mention} ID: {interaction.user.id}",inline=False
            )
            embed.add_field(
                name="**Muted from**", 
                value=f"{interaction.guild}", 
                inline=False
            )
            embed.add_field(
                name="**Muted for:**", 
                value=f"{reason}", 
                inline=False
            )
            embed.add_field(
                name="**Time:**", 
                value=f"{time}", 
                inline=False
            )
            await member.send(embed=embed)

@client.slash_command(name="unmute", description="Unmute members!")
async def unmute(
    interaction: nextcord.Interaction, 
    member: nextcord.Member = nextcord.SlashOption(
        name="member",
        description="Who do you want to unmute?",
        required=True
    ),

    reason = nextcord.SlashOption(
        name="reason",
        description="What is the reason?",
        required=False
    )
):
    async with interaction.channel.typing():
        if not (interaction.user.guild_permissions.moderate_members):
            await interaction.response.send_message("You can't use this as you don't have `timeout members`.", ephemeral=True)
            pass

        else:

            await member.edit(timeout=None, reason=reason)
            embed = nextcord.Embed(
                title=f"Unmuted {member.name}!", 
                color=0xe40707
            )
            await interaction.send(embed=embed)
            embed2 = nextcord.Embed(
                title=f"You were Unmuted!", 
                color=0xe40707
            )
            await member.send(embed=embed2)

@client.slash_command(name="warn", description="Warn someone!")
async def warn(interaction: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(description="Who is the person?"), *, reason=nextcord.SlashOption(description="What is the reason?")):
    async with interaction.channel.typing():
        if not (interaction.user.guild_permissions.moderate_members):
            await interaction.send("You don't have permissions for `timeout members`")
            pass

        else:
            embed2 = nextcord.Embed(
                title=f"Warned {member.name}",
                description="Information about the Warned user.",
                color=0xe40707
            )
            embed2.add_field(
                name="**Warned by:**",
                value=f"{interaction.user.mention}",
                inline=False
            )
            embed2.add_field(
                name="**Warned from**",
                value=f"{interaction.guild}",
                inline=False
            )

            embed2.add_field(
                name="**Warned for:**",
                value=f"{reason}",
                inline=False
            )
            await interaction.send(embed=embed2)

            embed3 = nextcord.Embed(
                title=f"Warned {member.name}!",       
                color=0xe40707
            )
            embed3.add_field(
                name="**Warned by:**",
                value=f"{interaction.user.mention}",
                inline=False
            )
            embed3.add_field(
                name="**Warned from**",
                value=f"{interaction.guild}",
                inline=False
            )
            embed3.add_field(
                name="**Warned for:**",
                value=f"{reason}",
                inline=False
            )
            await member.send(embed=embed3)

if __name__ == "__main__":
    client.run("OTAxMDk3NTIzNzAyMjg4Mzg1.YXK6dw.6mf58Yyh4jc5oOHA9ibjIvNwKm0")
