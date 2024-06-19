from interactions import Extension, slash_command, Embed, BrandColors, SlashContext, OptionType, slash_option, AutocompleteContext, SlashCommandChoice, Button, ButtonStyle
from consts import Consts
from error import Error
from battlenet import BattleNet
from raiderio_helper import RaiderIO_Helper

guild_ids = [642081591371497472]
_battleNet = BattleNet()

class RaiderIO(Extension):

    @slash_command(name="mythic_plus_rating", description="Get current mythic plus season rating for a character.")
    @slash_option(
        name="name",
        description="Character Name",
        required=True,
        opt_type=OptionType.STRING
    )
    @slash_option(
        name="region",
        description="Character's Region",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
        SlashCommandChoice(name="United States", value=Consts.REGION_US),
        SlashCommandChoice(name="Europe", value=Consts.REGION_EU)
        ]
    )
    @slash_option(
        name="realm",
        description="Character's Realm",
        required=True,
        opt_type=OptionType.STRING,
        autocomplete=True
    )
    async def MythicPlusRating(self, ctx: SlashContext, name, region, realm):      
        await ctx.defer()
        data = RaiderIO_Helper.GetRaiderIOData(name, realm, region)
        if(data is None):
            e = Error.GetErrorEmbed()
            await ctx.send(embeds = e)
        else:    
            profileButton = Button(
                style=ButtonStyle.URL,
                label=f"{data['name']}'s Raider.IO Page",
                url=data['profile_url'],
            )
            e = Embed()
            e.color = BrandColors.YELLOW
            seasonName = RaiderIO_Helper.GetNameForSlug_MythicPlus(data['mythic_plus_scores_by_season'][0]['season'])
            e.title = f"{data['name']}"
            e.set_author(name=f"Mythic+ {seasonName}")
            e.description = f"{data['race']} {data['class']}"
            e.add_field(name="DPS", value=data['mythic_plus_scores_by_season'][0]['scores']['dps'], inline=True)
            e.add_field(name="Healer", value=data['mythic_plus_scores_by_season'][0]['scores']['healer'], inline=True)
            e.add_field(name="Tank", value=data['mythic_plus_scores_by_season'][0]['scores']['tank'], inline=True)
            e.set_thumbnail(url=data['thumbnail_url'])
            e.set_footer(text="Powered by Raider.IO", icon_url="https://cdn.raiderio.net/images/brand/Icon_FullColor_Square.png")
            await ctx.send(embeds = e, components=profileButton)

    @slash_command(name="raid_progress", description="Get current expansions raid progression information for a character")
    @slash_option(
        name="name",
        description="Character Name",
        required=True,
        opt_type=OptionType.STRING
    )
    @slash_option(
        name="region",
        description="Character's Region",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
        SlashCommandChoice(name="United States", value=Consts.REGION_US),
        SlashCommandChoice(name="Europe", value=Consts.REGION_EU)
        ]
    )
    @slash_option(
        name="realm",
        description="Character's Realm",
        required=True,
        opt_type=OptionType.STRING,
        autocomplete=True
    )
    async def RaidProgression(self, ctx: SlashContext, name, region, realm):        
        await ctx.defer()
        data = RaiderIO_Helper.GetRaiderIOData(name, realm, region)
        if(data is None):
            e = Error.GetErrorEmbed()
            await ctx.send(embeds = e)
        else:    
            profileButton = Button(
                style=ButtonStyle.URL,
                label=f"{data['name']}'s Raider.IO Page",
                url=data['profile_url'],
            )
            e = Embed()
            e.color = BrandColors.YELLOW
            e.title = f"{data['name']}"
            e.set_author(name=f"Raid Progression")
            e.description = f"{data['race']} {data['class']}"
            for key, value in data['raid_progression'].items():
                raidName = RaiderIO_Helper.GetNameForSlug_Raid(key)
                e.add_field(name=raidName, value=f"{value['normal_bosses_killed']} N\n{value['heroic_bosses_killed']} H\n{value['mythic_bosses_killed']} M", inline=True)
            e.set_thumbnail(url=data['thumbnail_url'])
            e.set_footer(text="Powered by Raider.IO", icon_url="https://cdn.raiderio.net/images/brand/Icon_FullColor_Square.png")
            await ctx.send(embeds = e, components=profileButton)
       
    @slash_command(name="guild_progress", description="Get current expansions raid progression information for a guild")
    @slash_option(
        name="name",
        description="Guild's Name",
        required=True,
        opt_type=OptionType.STRING
    )
    @slash_option(
        name="region",
        description="Guild's Region",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
        SlashCommandChoice(name="United States", value=Consts.REGION_US),
        SlashCommandChoice(name="Europe", value=Consts.REGION_EU)
        ]
    )
    @slash_option(
        name="realm",
        description="Guild's Realm",
        required=True,
        opt_type=OptionType.STRING,
        autocomplete=True
    )
    async def GuildProgression(self, ctx: SlashContext, name, region, realm):        
        await ctx.defer()
        data = RaiderIO_Helper.GetRaiderIOGuildData(name, realm, region)
        if(data is None):
            e = Error.GetErrorEmbed()
            await ctx.send(embeds = e)
        else:    
            profileButton = Button(
                style=ButtonStyle.URL,
                label=f"{data['name']}'s Raider.IO Page",
                url=data['profile_url'],
            )
            e = Embed()
            e.color = BrandColors.YELLOW
            e.title = f"{data['name']}"
            e.set_author(name=f"Raid Progression")
            e.description = f"{data['realm']}"
            for key, value in data['raid_progression'].items():
                raidName = RaiderIO_Helper.GetNameForSlug_Raid(key)
                e.add_field(name=raidName, value=f"{value['normal_bosses_killed']} N\n{value['heroic_bosses_killed']} H\n{value['mythic_bosses_killed']} M", inline=True)
            e.set_thumbnail(url="https://wow.zamimg.com/images/wow/icons/large/inv_shirt_guildtabard_01.jpg")
            e.set_footer(text="Powered by Raider.IO", icon_url="https://cdn.raiderio.net/images/brand/Icon_FullColor_Square.png")
            await ctx.send(embeds = e, components=profileButton)
       
    @MythicPlusRating.autocomplete("realm")
    @RaidProgression.autocomplete("realm")
    @GuildProgression.autocomplete("realm")
    async def autocompleteRealm(self, ctx: AutocompleteContext):  
        try:
            region = ctx.kwargs.get("region")
            realmList = _battleNet.GetRealms(region) 
            choices = [
                SlashCommandChoice(name = realm['name'], value = realm['slug']) for realm in realmList['realms'] if ctx.input_text.lower() in realm['name'].lower()
            ] 

            if(len(choices) > 25):
                choices = choices[0:25]

            await ctx.send(choices)
        except:
            pass


        