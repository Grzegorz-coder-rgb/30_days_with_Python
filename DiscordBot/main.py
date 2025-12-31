import discord 
from discord.ext import commands
from bot_logic import *
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged as {bot.user}")
    
    # Pobieramy ID kanału z pliku .env
    channel_id = os.getenv("WELCOME_CHANNEL_ID")
    
    if channel_id:
        # Zamieniamy ID ze stringa na liczbę (int)
        channel = bot.get_channel(int(channel_id))
        
        if channel:
            await channel.send("✅ Bot jest online! Użyj `!get_help`, aby zobaczyć listę komend.")
        else:
            print("Błąd: Nie znaleziono kanału o podanym ID. Sprawdź uprawnienia bota.")
    else:
        print("Błąd: Brak WELCOME_CHANNEL_ID w pliku .env")

@bot.command()
async def random_number(ctx):
    number = generate_random_number()
    await ctx.send(f"🎲 The number drawn: {number}")

@bot.command()
async def get_help(ctx):
    await ctx.send(help_command())

@bot.command()
async def give_role(ctx, member: discord.Member, *, role_arg):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")

    if admin_role not in ctx.author.roles:
        await ctx.send("❌ Tylko Admin może nadawać role.")
        return

    # resolve role (mention lub nazwa)
    if role_arg.startswith("<@&") and role_arg.endswith(">"):
        role_id = int(role_arg[3:-1])
        role = ctx.guild.get_role(role_id)
    else:
        role = discord.utils.find(
            lambda r: r.name.lower() == role_arg.lower(),
            ctx.guild.roles
        )

    if role is None:
        await ctx.send("❌ Rola nie istnieje.")
        return

    # 🔒 BEZPIECZNIK HIERARCHII
    if role >= ctx.guild.me.top_role:
        await ctx.send("❌ Bot nie może nadawać tej roli (hierarchia ról).")
        return

    await member.add_roles(role)
    await ctx.send(f"✅ Nadano rolę {role.name} użytkownikowi {member.name}")



# main.py
@bot.command()
async def generate_password(ctx, length: int = 24):

    p_gen = PasswordGenerator()
    password, strength = p_gen.generate(length, True, True, True)
    
    response = (
        f"🔑 **Your Password:** `{password}`\n"
        f"📊 **Strength:** {strength}\n"
        f"📏 **Length:** {length}"
    )
    await ctx.send(response)

@bot.command()
async def tictactoe(ctx):

    # Tworzymy instancję gry, przekazując autora wiadomości jako gracza X
    game_view = TicTacToeView(ctx.author)
    
    await ctx.send(f"Kółko i Krzyżyk! Zaczyna {ctx.author.mention} (X). Kto dołączy jako (O)?", view=game_view)

@bot.command()
async def tictactoeAI(ctx):
    game_view = TicTacToeAIView(ctx.author)
    await ctx.send(f"Tic Tac Toe vs AI! You are X. Good luck, {ctx.author.mention}!", view=game_view)

@bot.command()
@commands.has_permissions(manage_messages=True)  # tylko osoby z uprawnieniem mogą użyć
async def clear(ctx, amount: int = 50):
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"Usunięto {len(deleted)} wiadomości.", delete_after=5)  # wiadomość znika po 5 sek.

    
bot.run(os.environ.get("DISCORD_BOT_TOKEN"))