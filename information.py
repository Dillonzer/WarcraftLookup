from interactions import Extension, slash_command, Embed, BrandColors, SlashContext
from consts import Consts

class BotInformation(Extension):
    @slash_command(name="info", description="Get information about the bot")
    async def PrintCommands(self, ctx: SlashContext):
        e = Embed()
        e.color = BrandColors.GREEN
        e.title = "Information!"
        e.description = "Thanks for using Warcraft Lookup! This bot is currently only setup for US / EU but if needs I can look into expanding. If you'd like to support what I do please follow me on [Patreon](https://www.patreon.com/bePatron?u=34112337). I'd also love to hear feedback on this bot. Please reachout to me via my [Discord](https://discord.gg/SqpJZn2) if you have any issues or ideas!"
        e.set_author(name="Warcraft Lookup",icon_url="https://wow.zamimg.com/images/wow/icons/large/quest_khadgar.jpg")
        e.set_thumbnail(url=Consts.LOGO)
        
        commands = "• `/mythic_plus_rating <characterName> <region> <realm>`: Displays current season mythic plus rating!\n"
        commands += "• `/raid_progress <characterName> <region> <realm>`: Displays current expansion raid progression for a character!\n"
        commands += "• `/guild_progress <characterName> <region> <realm>`: Displays current expansion raid progression for a guild!\n"
        commands += "• `/warcraft_logs <characterName> <region> <realm> <encounter> <metric>`: Get a character's specific logs for a raid or season!\n"
        
        e.add_field(name="Commands", value=commands, inline=False)
        e.set_footer(text="Created by Dillonzer")

        await ctx.send(embeds = e, ephemeral=True)