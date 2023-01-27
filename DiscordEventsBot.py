import discord
from discord.ui import *
from datetime import datetime

bot = discord.Bot()

YOURTOKEN="YOURTOKEN"

class MyView(View):
    
    def __init__(self,embed,ctx):
        super(MyView, self).__init__()
        self.embed=embed
        self.ctx=ctx

    @discord.ui.button(label="Button 1", style=discord.ButtonStyle.red, emoji="⚔️")
    async def callbackDPS(self, button, interaction:discord.Interaction):
        await self.callback(button, interaction, "Field 1")

    @discord.ui.button(label="Button 2", style=discord.ButtonStyle.green, emoji="💊")
    async def callbackSUP(self, button, interaction):
        await self.callback(button, interaction, "Field 2")

    @discord.ui.button(label="Button 3", style=discord.ButtonStyle.blurple, emoji="🪖")
    async def callbackTANK(self, button, interaction):
        await self.callback(button, interaction, "Field 3")

    async def callback(self, button, interaction, field_name):
        UserDisplayName=interaction.user.display_name
        FormatedName="\n> "+UserDisplayName
        for i, field in enumerate(self.embed.fields):
            if field.name == field_name:
                if FormatedName in field.value:
                    field.value=field.value.replace(FormatedName,"")
                else:
                    field.value = field.value+FormatedName
            elif field.name != "Time":
                newValue=field.value.replace(FormatedName,"")
                self.embed.set_field_at(i, name=field.name, value=newValue, inline=True)

        await interaction.response.edit_message(embed=self.embed)

@bot.event
async def on_ready(): # Check if bot is online
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name = "create", description = "Create a New Event")
async def create(ctx, title:str, description:str, datainicial:str, horainicial:str, datafinal:str, horafinal:str, role:str): # Command to create a new event "/create".
    print(ctx.author.display_name)
    try:
        DataComeço = datetime.strptime(datainicial+" "+horainicial,'%d/%m/%Y %H:%M')
        DataFim = datetime.strptime(datafinal+" "+horafinal,'%d/%m/%Y %H:%M')
    except ValueError:
        await ctx.respond("Invalid Date or Invalid Time. Please enter in the format 'dd/mm/yyyy', 'H:M'.")
        return
    UnixComeço = int(DataComeço.timestamp())
    UnixFim = int(DataFim.timestamp())
    if datainicial == datafinal:
        TimeValue=f"<t:{UnixComeço}:F> - <t:{UnixFim}:t>"
    else:
        TimeValue = f"<t:{UnixComeço}:F> - <t:{UnixFim}:f>"
    embed = discord.Embed(
    title=title,
    description=description,
    color=discord.Color.yellow(),
    timestamp=datetime.now(),
    )
    embed.add_field(
        name="Time", 
        value=TimeValue,
        inline=False
        )
    embed.add_field(
        name="Field 1", 
        value="", 
        inline=True
        )
    embed.add_field(
        name="Field 2", 
        value="", 
        inline=True
        )
    embed.add_field(
        name="Field 3", 
        value="", 
        inline=True
        )
    embed.set_footer(
        text=f"Created by {ctx.author.display_name}"
    )
    view = MyView(embed,ctx)
    roles = discord.utils.get(ctx.guild.roles, name=role)
    if roles:
        await ctx.respond(view=view, embed=embed, content=f'{roles.mention}')
    else:
        await ctx.respond(view=view, embed=embed, content="Invalid role")


# Start Bot
bot.run(YOURTOKEN)
