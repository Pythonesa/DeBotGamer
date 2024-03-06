import asyncio
from twitchio.ext import commands
from .question import Question
from trivia.trivia_questions import trivia_questions
import random
from players.player import Player, players_list

current_trivia = False
current_question = None
users_correct = []
users_answered = []


@commands.command(name="trivia")
async def trivia(ctx, *, message: str = None):
    global current_trivia
    global current_question
    global users_correct
    global users_answered
    global players_list
    if not message:
        await ctx.send("Debes especificar un mensaje al usar el comando trivia")
        return
    if message == "start":
        if current_trivia:
            await ctx.send("Ya hay una trivia en curso")
        else:
            current_trivia = True
            current_question = random.choice(trivia_questions)
            await ctx.send(current_question.text)
            for option in current_question.options:
                await ctx.send(f"{option}")
            users_answered = []
            users_correct = []
            await ctx.send(f"La trivia durará 5 minutos")
            await asyncio.sleep(300)
            await ctx.send(f"La respuesta correcta era: {current_question.options[current_question.correct_answer - 1]}")
            await ctx.send(f"Los usuarios que acertaron son: {', '.join([user for user in users_correct])}")
            if len(users_correct) > 0:
                if users_correct[0] in [player.name for player in players_list]:
                    for player in players_list:
                        if player.name == users_correct[0]:
                            player.points += 1
                else:
                    players_list.append(Player(users_correct[0], 1))
            for player in players_list:
                print(f"{player.name}: {player.points}")
            current_trivia = False
            current_question = None
    elif current_trivia and ctx.author.name not in users_answered:
        try:
            answer = int(message)
            users_answered.append(ctx.author.name)
            if answer == current_question.correct_answer:
                print(f"{ctx.author.name} acerto la trivia")
                users_correct.append(ctx.author.name)
        except ValueError:
            await ctx.send(f"{ctx.author.name} especifica una opción con el comando")
