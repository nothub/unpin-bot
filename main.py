#!/usr/bin/env python3
import os
from os.path import exists

from disnake import Message
from disnake.ext import tasks, commands
from dotenv import load_dotenv


class Shit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ass.start()

    @tasks.loop(seconds=10)
    async def ass(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                pins = await channel.pins()
                if len(pins) > int(os.environ['MAX_PINS']):
                    pins.sort(key=lambda m: m.created_at)  # sort by creation date (oldest first)
                    oldest: Message = pins[0]
                    print("unpinning message_id=" + str(oldest.id) +
                          " author_id=" + str(oldest.author.id) +
                          " author_name=" + oldest.author.name +
                          " message_content=\"" + oldest.content + "\"")
                    await oldest.unpin()

    @ass.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()


# pyz entrypoint
def main():
    if not exists("config.env"):
        print("saving default config")
        with open('config.env', 'w') as file:
            file.write("BOT_TOKEN=CHANGEME" + "\n" + "MAX_PINS=100" + "\n")
        exit(0)
    load_dotenv("config.env")
    bot = commands.Bot()
    bot.add_cog(Shit(bot))
    bot.run(os.environ['BOT_TOKEN'])


# this will not be invoked, when called in pyz context
if __name__ == '__main__':
    main()
