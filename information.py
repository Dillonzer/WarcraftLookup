from interactions import Extension, slash_command, Embed, BrandColors, SlashContext
from test_consts import Consts

class BotInformation(Extension):
    @slash_command(name="info", description="Get information about the bot")
    async def PrintCommands(self, ctx: SlashContext):
        e = Embed()
        e.color = BrandColors.GREEN
        e.title = "Information!"
        e.description = "Thanks for using Warcraft Lookup! If you'd like to support what I do please follow me on [Patreon](https://www.patreon.com/bePatron?u=34112337)"
        e.set_author(name="Warcraft Lookup")#,icon_url=Consts.LOGO_ADDRESS)
        #e.set_thumbnail(url=Consts.POKEMON_CARD_LOGO_ADDRESS)
        
        commands = "• `/mythic_plus_rating <characterName> <region> <realm>`: Displays current season mythic plus rating!\n"
        commands += "• `/raid_progress <characterName> <region> <realm>`: Displays current expansion raid progression for a character!\n"
        
        e.add_field(name="Commands", value=commands, inline=False)
        e.set_footer(text="Created by Dillonzer")

        await ctx.send(embeds = e, ephemeral=True)