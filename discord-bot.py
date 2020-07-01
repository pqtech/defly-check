import discord
from os import getenv
from discord.ext import commands
from typing import Optional


import bot_utils

bot = commands.Bot(command_prefix="!")

tracklist = bot_utils.load_tracklist()

bot.remove_command("help")


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.command()
async def check_server(
    ctx: commands.Context, region: str, port: Optional[int] = None
) -> None:
    if __debug__:
        bot_utils.logger(ctx, bot_utils.Logger.CHECK_SERVER)

    if region:
        await bot_utils.check_server(ctx, region, port=port)
    else:
        await bot_utils.error(ctx)


@bot.command()
async def check_servers(ctx: commands.Context, port: Optional[str] = None) -> None:
    if __debug__:
        bot_utils.logger(ctx, bot_utils.Logger.CHECK_SERVERS)

    await bot_utils.check_servers(ctx, port=port)


@bot.command()
async def get_link(
    ctx: commands.Context, region: str, port: Optional[str] = None
) -> None:
    if __debug__:
        bot_utils.logger(ctx, bot_utils.Logger.GET_LINK)

    await ctx.send(bot_utils.get_link(region=region, port=port))


@bot.command()
async def search_player(ctx: commands.Context, *args) -> None:
    if __debug__:
        bot_utils.logger(ctx, bot_utils.Logger.SEARCH_PLAYER)

    await bot_utils.search_player(ctx, args)


@bot.command()
async def check_list(ctx: commands.Context) -> None:
    if __debug__:
        bot_utils.logger(ctx, bot_utils.Logger.CHECK_LIST)

    await bot_utils.check_tracklist(ctx, tracklist)


@bot.command()
async def get_list(ctx: commands.Context) -> None:
    if __debug__:
        bot_utils.logger(ctx, bot_utils.Logger.GET_LIST)

    await ctx.send(" ".join([f"`{victim}`" for victim in tracklist]))


@bot.command()
async def add_player(ctx: commands.Context, *args) -> None:
    if __debug__:
        bot_utils.logger(ctx, bot_utils.Logger.ADD_PLAYER)

    username = " ".join(args)
    if username:
        if username in ("Player",):
            await ctx.send("srysly??")
        else:
            if username in tracklist:
                await ctx.send("he is already in the tracklist")
            else:
                tracklist.add(username)
                bot_utils.save_tracklist(tracklist)
                await ctx.send(f"{username} is in tracklist now")
    else:
        await bot_utils.error(ctx)


@bot.command()
async def remove_player(ctx: commands.Context, *args) -> None:
    if __debug__:
        bot_utils.logger(ctx, bot_utils.Logger.ADD_PLAYER)

    username = " ".join(args)
    if username:
        if username in ("Player",):
            await ctx.send("srysly??")
        else:
            if username in tracklist:
                tracklist.remove(username)
                bot_utils.save_tracklist(tracklist)
                await ctx.send(f"{username} is in tracklist now")
            else:
                await ctx.send("he is already in not there")
    else:
        await bot_utils.error(ctx)


@bot.command()
async def help(ctx: commands.Context) -> None:
    if __debug__:
        bot_utils.logger(ctx, bot_utils.Logger.HELP)
    await ctx.send(embed=bot_utils.HELP_MSG)


bot.run(
    getenv(
        "DISCORD_TOKEN"
    )
)
