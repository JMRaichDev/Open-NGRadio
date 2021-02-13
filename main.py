import discord
import requests
from colorama import Fore
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix="ong!", description="A remake of NGRadio#4551 in Open-Source by JMimosa#2495")

bot.remove_command("help")


# Event

@bot.event
async def on_ready():
    print(Fore.GREEN + "[+] Bot is now started and ready")
    print(Fore.GREEN + '[+] Logged in as:'
                       f'\n [-->] {bot.user.name}#{bot.user.discriminator} -> {bot.user.id}')  # printing into the console some information about the bot


@bot.command(pass_context=True, name='help', aliases=['h'])
async def _help(ctx):
    await ctx.send("```Help : "
                   "\n  --> ong!help -> (ong!h) : Show this message and help you."
                   "\n  --> ong!play -> (ong!p) : Join your voice channel and play NG-radio."
                   "\n  --> ong!leave -> (ong!l) : Leave current voice channel."
                   "\n  --> ong!song -> (ong!sg) : Shows current played song.```")  # sending help to user


@bot.command(pass_context=True, name='song', aliases=['sg'])
async def _song(ctx):
    source = getRadioApiJSON()  # setting source to NGRadio-Api.json

    # creating an embed with all the information about current music
    embed = discord.Embed(
        title=":musical_note:  Quel est le titre en cours ?",
        description=f"Actuellement sur NGRadio : {source['now_playing']['song']['title']} de {source['now_playing']['song']['artist']}",
        color=discord.Colour.blue()
    )

    embed.set_footer(text="NGRadio • NationsGlory.fr")
    embed.set_thumbnail(url=f"{source['now_playing']['song']['art']}")
    await ctx.send(embed=embed)  # sending to user the embed with all information about current music


@bot.command(pass_context=True, name='play', aliases=['p'])
async def _play(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:  # check if channel is None (= user not connected to any voice channel)
        await ctx.send("You are not connected to a voice channel")  # telling to user that he isn't in a voice channel
        return

    voice = get(bot.voice_clients, guild=ctx.guild)  # getting bot voice client in message's guild

    if voice and voice.is_connected():  # check if bot is already connected to any channel and if voice isn't None
        await voice.move_to(channel)  # moving to user's voice channel
    else:
        voice = await channel.connect()  # creating a voice object and connecting to user's channel

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}
    NG_RADIO_URL = getRadioApiJSON()['station'][
        'listen_url']  # or https://radio.nationsglory.fr:8000/ngradio

    voice = get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():  # check if bot is already playing NGRadio
        voice.play(FFmpegPCMAudio(NG_RADIO_URL, **FFMPEG_OPTIONS))  # playing to microphone NGRadio sound

    await ctx.message.delete()  # deleting command message


@bot.command(pass_context=True, name='leave', aliases=['l'])
async def _leave(ctx):
    await ctx.message.delete()  # deleting command message
    await ctx.voice_client.disconnect()  # disconnect bot voice_client


def getRadioApiJSON():
    return requests.get("https://apiv2.nationsglory.fr/radio/api.json").json()  # parsing api.json and returning content as JSON


bot.run("")  # connecting to discord with a token and starting the bot
