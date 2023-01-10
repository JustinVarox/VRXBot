import discord
from discord.ext import commands
import asyncio
import time

# Erstelle den Bot
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

# Client definieren
client = discord.Client(intents=discord.Intents.all())


# Definiere die Support-Rolle
ROLE_ID = 1062195470249762836

# Wartezeit zwischen den Tickets (in Sekunden)
TICKET_COOLDOWN = 120


# Tickets, die gerade erstellt wurden (Nutzer-ID: Zeit, an der das Ticket erstellt wurde)
active_tickets = {}

# Erstelle einen Channel, wenn /ticket eingegeben wurde
@bot.command()
async def ticket(ctx):
    # Überprüfe, ob das Ticket bereits erstellt wurde
    if ctx.author.id in active_tickets:
        # Wartezeit noch nicht abgelaufen
        if active_tickets[ctx.author.id] + TICKET_COOLDOWN > time.time():
            await ctx.send("Bitte warte, bevor du ein neues Ticket erstellst.")
            return
    
    # Speichere die aktuelle Zeit als Ticket-Erstellungszeit
    active_tickets[ctx.author.id] = time.time()
    
    # Erstelle den Channel
    guild = ctx.guild
    role = discord.utils.get(guild.roles, id=ROLE_ID)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True),
        role: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(f"Ticket {ctx.author.name}", overwrites=overwrites)
    
    # Sende eine Nachricht an den Nutzer
    await channel.send(f"Hallo {ctx.author.mention}! Vielen Dank, dass du unseren Dienst nutzt. Ein Mitarbeiter wird sich in Kürze bei dir melden. Bitte habe Verständnis, dass wir nicht alle Tickets direkt bearbeiten können. Die Bearbeitungszeit kann bis zu **24 Stunden** dauern. Dies ist jedoch nur dann der Fall, wenn wir derzeit ausgelastet sind! - {role.mention}")

# Sende eine Hilfe-Nachricht, wenn /hilfe eingegeben wurde
@bot.command()
async def hilfe(ctx):
    await ctx.send("Um Hilfe zu erhalten, eröffne ein Ticket mit /ticket oder schreibe eine Mail an info@vrx-services.de")


# Sende eine Nachricht mit allen offenen Tickets, wenn /tickets eingegeben wurde
@bot.command()
async def tickets(ctx):
    # Überprüfe, ob der Nutzer die erforderliche Rolle hat
    if not discord.utils.get(ctx.author.roles, id=ROLE_ID):
        await ctx.send("Du hast nicht die erforderliche Rolle, um diesen Befehl auszuführen.")
        return
    
    # Sende die Nachricht "Offene Tickets"
    await ctx.send("Offene Tickets:")
    
    # Erstelle eine Liste der Channel mit "ticket" im Namen
    ticket_channels = []
    for channel in ctx.guild.channels:
        if "ticket" in channel.name.lower() and channel.id != 1062210066796781568:
            ticket_channels.append(channel)
    
    # Sende eine Nachricht mit allen gefundenen ticket-Channel
    if ticket_channels:
        for channel in ticket_channels:
            await ctx.send(channel.mention)
    else:
        await ctx.send("Keine offenen Tickets.")

# Login Command + Rolle geben
@bot.command()
async def login(ctx):
    # Check if the user has the required role
    if not discord.utils.get(ctx.author.roles, id=ROLE_ID):
        await ctx.send("Keine Berechtigung")
        return
    
    # Get the role
    role = discord.utils.get(ctx.guild.roles, id=1062211750440747059)
    
    # Add the role to the user
    await ctx.author.add_roles(role)
    
    # Send a message to the user
    await ctx.send(f"Hey, {ctx.author.name} - Du hast dich ins Adminsystem eingeloggt!")

# Logout Command + Rolle wegnehmen
@bot.command()
async def logout(ctx):
    # Check if the user has the required role
    if not discord.utils.get(ctx.author.roles, id=ROLE_ID):
        await ctx.send("Keine Berechtigung")
        return
    
    # Get the role
    role = discord.utils.get(ctx.guild.roles, id=1062211750440747059)
    
    # Remove the role from the user
    await ctx.author.remove_roles(role)
    
    # Send a message to the user
    await ctx.send(f"Hey, {ctx.author.name} - Du hast dich aus dem Adminsystem ausgeloggt!")

# /stafflist Befehl und Ausgabe der Online Mitarbeiter
@bot.command()
async def stafflist(ctx):
    # Get the role
    role = discord.utils.get(ctx.guild.roles, id=1062211750440747059)
    
    # Get a list of all users with the role
    staff_members = [member for member in ctx.guild.members if role in member.roles]
    
    # Check if there are any staff members
    if not staff_members:
        await ctx.send(":no_entry: **Derzeit ist kein Mitarbeiter eingeloggt!** :no_entry: ")
    else:
        # Create a string with the names of all staff members, each on a separate line
        staff_names = "\n".join([member.mention for member in staff_members])
    
        # Send the message
        await ctx.send(f"**Mitarbeiter eingeloggt**\n{staff_names}")


# Führe den Bot mit deinem Token aus
bot.run("MTA2MjE4MjI2NDk5MTEzMzc3OA.GkRYwP.ti_eEs6F4lA5Z-snMgW79UjdohrckGHLUyhFcM")


