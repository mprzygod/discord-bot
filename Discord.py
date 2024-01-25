import discord
import random
import asyncio

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('$guess'):
            await message.channel.send('Guess a number between 1 and 10.')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long it was {answer}.')

            if int(guess.content) == answer:
                await message.channel.send('You are right!')
            else:
                await message.channel.send(f'Oops. It is actually {answer}.')
        
        
        if message.content.startswith('$pkn'):
            await self.play_rps(message)

    async def play_rps(self, message):
        await message.channel.send("Co wybierasz ?")

        def is_valid_choice(m):
            return m.author == message.author and m.content.lower() in ['$papier', '$kamień', '$nożyce']

        user_choice = await self.wait_for('message', check=is_valid_choice, timeout=15.0)

        choices = ['kamień', 'papier', 'nożyce']
        bot_choice = random.choice(choices)

        await message.channel.send(f'Wybieram {bot_choice}.')

        if user_choice.content.lower() == f'${bot_choice}':
            await message.channel.send("REMIS!")
        elif (
            (user_choice.content.lower() == '$kamień' and bot_choice == 'nożyce') or
            (user_choice.content.lower() == '$papier' and bot_choice == 'kamień') or
            (user_choice.content.lower() == '$nożyce' and bot_choice == 'papier')
        ):
            await message.channel.send('WYGRAŁEŚ!')
        else:
            await message.channel.send('PRZEGRAŁEŚ:(')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run("Token")
