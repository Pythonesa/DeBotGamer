from _secrets import IRC_TOKEN
from twitchio.ext import commands
from trivia.trivia_commands import trivia


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=IRC_TOKEN,
            prefix="!",
            initial_channels=["pythonesa"]
        )

        self.add_command(trivia)

    async def event_ready(self):
        for channel in self.connected_channels:
            print(f"Logged in as {self.nick} to channel {channel.name}.")


def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()