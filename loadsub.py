import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os, json
import asyncio


intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

try:
    os.system('clear')
except:
    os.system('cls')
with open("config.json", 'r') as config:
    configs = json.load(config)

@bot.event
async def on_ready():
    print("HYPERLEAKS - BOT")
    print(f"Connecté à : {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name="HYPER leaks v{0}".format(configs["version"])))

@bot.event
async def on_invite_create(invite):
    print("ON INVITE event")
    member = invite.inviter

    if invite.uses > 10:
        guild = invite.guild
        role = discord.utils.get(guild.roles, name='Abonné')
        await member.add_roles(role)
    else:
        invites_left = 10 - invite.uses
        await member.send(f"Il vous reste {invites_left} invitations avant d'atteindre les 10 invitations nécessaires pour obtenir le grade !⚡")


@bot.command()
@has_permissions(administrator=True)
async def display_embed(ctx, embed_name):
    with open(f"embeds/{embed_name}.json", "r") as offer:
        offers = json.load(offer)
    for e in offers["embeds"]:
        embed = discord.Embed.from_dict(e)
        await ctx.send(embed=embed)

@bot.command()
@has_permissions(administrator=True)
async def sub(ctx, vintedurl):
    x = await ctx.channel.create_webhook(name="HOOK - {0}".format(ctx.channel.name))
    with open("config.json", 'w+') as configedit:
        configs["suburl"][str(x.url)] = {}
        configs["suburl"][str(x.url)]["url"] = str(vintedurl)
        configs["suburl"][str(x.url)]["salon"] = str(ctx.channel.name)

        json.dump(configs,configedit,indent=4)
    await ctx.send(f"{ctx.author.mention} - **✔️ Webhook ajouté avec le lien !**")

@bot.command()
@has_permissions(administrator=True)
async def change_url(ctx, new_url):
    for weburl in configs["suburl"]:
        if configs["suburl"][weburl]["salon"] == ctx.channel.name:
            with open("config.json", 'w+') as configedit:
                configs["suburl"][str(weburl)]["url"] = str(new_url)
                json.dump(configs,configedit,indent=4)
            await ctx.send(f"{ctx.author.mention} - **✔️ Le lien du scrapping lié au salon {ctx.channel.name} a été modifié avec succès !**")
            return

@bot.command()
@has_permissions(administrator=True)
async def remove_sub(ctx):
    webhook = None
    for weburl in configs["suburl"]:
        if configs["suburl"][weburl]["salon"] == ctx.channel.name:
            webhook = weburl
            with open("config.json", 'w+') as configedit:
                del configs["suburl"][webhook]
                json.dump(configs,configedit,indent=4)
            await ctx.send(f"{ctx.author.mention} - **✔️ Le lien du scrapping lié au salon {ctx.channel.name} a été supprimé avec succès !**")
            return

@bot.command()
@has_permissions(administrator=True)
async def change_color_text(ctx, color):
    if color not in ["fix","YAML"]:
        await ctx.send(f"{ctx.author.mention} - **❌ La couleur n'est pas disponible ! Essayez autre choses.**")
        return

    for weburl in configs["suburl"]:
        if configs["suburl"][weburl]["salon"] == ctx.channel.name:
            with open("config.json", 'w+') as configedit:
                configs["embed-color-text"] = color
                json.dump(configs,configedit,indent=4)
            await ctx.send(f"{ctx.author.mention} - **✔️ La couleur du text de l'embed a été modifié avec succès !**")
            return

@bot.command()
@has_permissions(administrator=True)
async def change_color_embed(ctx, color):
    for weburl in configs["suburl"]:
        if configs["suburl"][weburl]["salon"] == ctx.channel.name:
            with open("config.json", 'w+') as configedit:
                configs["embed-color"] = color
                json.dump(configs,configedit,indent=4)
            await ctx.send(f"{ctx.author.mention} - **✔️ La couleur de l'embed a été modifié avec succès !**")
            return

@bot.command()
@has_permissions(administrator=True)
async def say(ctx, message):
    await ctx.send(message)
    await ctx.message.delete()

@bot.command()
@has_permissions(administrator=True)
async def clear(ctx, amount=5):
    channel = ctx.channel

    deleted = await channel.purge(limit=amount)
    confirmation_msg = await ctx.send(f"Effacement de {len(deleted)} messages !")
    await asyncio.sleep(3)
    await confirmation_msg.delete()


@bot.command()
async def invites(ctx, username):
    try:
        guild = ctx.guild
        for invite in await guild.invites():
            if invite.inviter.name == username:
                num_invites = invite.uses
                await ctx.send(f"{username} a invité {num_invites} personnes sur le serveur.")
                return
        await ctx.send(f"{username} n'a pas créé d'invitation sur ce serveur.")
    except:
        await ctx.send(configs["error_msg"])


@bot.command()
@has_permissions(administrator=True)
async def help(ctx):
    embed = discord.Embed(title="Help Vinted Bot",color=0xFFFFFF)
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.add_field(name="**sub**",value=f"**Usage :** ``{configs['prefix']}sub url_vinted``",inline=False)
    embed.add_field(name="**remove_sub**",value=f"**Usage :** ``{configs['prefix']}remove_sub``",inline=False)
    embed.add_field(name="**change_url**",value=f"**Usage :** ``{configs['prefix']}change_url nouvel_url_vinted``",inline=False)
    embed.add_field(name="**change_color_text**",value=f"**Usage :** ``{configs['prefix']}change_color_text (YAML/fix)``",inline=False)
    embed.add_field(name="**change_color_embed**",value=f"**Usage :** ``{configs['prefix']}change_color_embed couleur``",inline=False)
    await ctx.send(embed=embed)


bot.run(configs["token"])
