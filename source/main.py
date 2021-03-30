import logging

from discord.ext import commands

import general_messages as gm
from music_player.player import MusicPlayer
from music_stats.music_manager import MusicManager
from secretConfig import discord_settings
from message_handler import MessageHandler
from chess import chess_manager

bot = commands.Bot(command_prefix=discord_settings['prefix'])
bot.remove_command('help')

music_manager = MusicManager()
music_player = MusicPlayer(music_manager)
handler = MessageHandler(bot, music_manager)


async def on_message(message):
    await handler.process_message(message)

bot.add_listener(on_message, 'on_message')


def _log_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return
    logging.error("{err} in message: {msg}".format(err=error, msg=ctx.message.content))


@bot.check
async def globally_block_on_debug(ctx):
    return discord_settings['debug'] == (str(ctx.message.channel) == 'debug')


@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')


@hello.error
async def hello_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')
    _log_error(ctx, error)


@bot.command()
async def help(ctx):
    await ctx.send(gm.HELP)


@help.error
async def guide_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def sheet(ctx):
    await ctx.send(gm.SHEET_LINK)


@sheet.error
async def sheet_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def github(ctx):
    await ctx.send(gm.GITHUB_LINK)


@github.error
async def github_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def random(ctx, songs_number: int = 1):
    await ctx.send(music_manager.random_songs_to_play(songs_number))


@random.error
async def random_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Аргументом должно быть число DansGame')
        return
    _log_error(ctx, error)


@bot.command()
async def search(ctx, to_find: str):
    await ctx.send(music_manager.find_songs(to_find))


@search.error
async def search_error(ctx, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Аргументом должна быть строка DansGame')
        return
    _log_error(ctx, error)


@bot.command()
async def youtube(ctx):
    await ctx.send(gm.YOUTUBE)


@youtube.error
async def youtube_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def chess(ctx, variant: str = None):
    await ctx.send(chess_manager.create_game(variant))


@chess.error
async def chess_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Неправильное название режима DansGame. Используй lowerCamelCase')
        return
    _log_error(ctx, error)


@bot.command()
async def play(ctx, *song_str):
    await music_player.process_song_request(ctx, ' '.join(song_str))


@play.error
async def play_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def shuffle(ctx):
    await music_player.shuffle()


@shuffle.error
async def shuffle_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def skip(ctx):
    music_player.skip()


@skip.error
async def skip_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def fs(ctx):
    music_player.skip()


@fs.error
async def fs_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def loop(ctx):
    music_player.loop()


@loop.error
async def loop_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def radio(ctx):
    await music_player.enable_radio(ctx)


@radio.error
async def radio_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def stop(ctx):
    music_player.stop()


@stop.error
async def stop_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def pause(ctx):
    music_player.pause()


@pause.error
async def pause_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def resume(ctx):
    music_player.resume()


@resume.error
async def resume_error(ctx, error):
    _log_error(ctx, error)


@bot.command()
async def disconnect(ctx):
    await music_player.disconnect()


@disconnect.error
async def disconnect_error(ctx, error):
    _log_error(ctx, error)


def main():
    bot.run(discord_settings['token'])


if __name__ == '__main__':
    main()
