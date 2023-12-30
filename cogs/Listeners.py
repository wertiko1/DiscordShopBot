import disnake
from disnake.ext import commands, tasks
from .utils.Data import DataBase
from .configs.Config import SERVER_ID
from .utils.Payment import Payment


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DataBase()
        self.pay = Payment()
        self.color = 0x2B2D31

    @tasks.loop(seconds=10)
    async def user_db(self):
        guild = self.bot.get_guild(SERVER_ID)
        for member in guild.members:
            if member.bot:
                continue
            results = await self.db.get_user(member)
            if not results:
                await self.db.add_user(member)

    @tasks.loop(seconds=10)
    async def transfer_check(self):
        results = await self.db.get_transfers()
        for i in results:
            result = self.pay.check_invoice()
            for res in result:
                if res.status == 'success' and res.label == i[1]:
                    await self.db.add_money(user_id=i[0], amount=i[2])
                    await self.db.rm_transfer(i[1])
                    channel = self.bot.get_channel(1188387508640297042)
                    member = self.bot.get_guild(SERVER_ID).get_member(i[0])
                    embed = disnake.Embed(
                        title=f'Платеж #{i[1]}',
                        description=f'Участник {member.mention}',
                        color=self.color
                    ).set_thumbnail(url=member.display_avatar.url)
                    embed.add_field(name='Сумма', value=f'```{i[2]}```', inline=False)
                    embed.add_field(name='Статус', value='Оплачен', inline=False)
                    await channel.send(embed=embed)
                    embed = disnake.Embed(
                        title=f'Платеж #{i[1]}',
                        description='Ваш баланс успешно пополнен',
                        color=self.color
                    ).set_thumbnail(url=member.display_avatar.url)
                    embed.add_field(name='Сумма', value=f'```{i[2]}```', inline=False)
                    embed.set_footer(text='Если произошла ошибка, обратитесь в поддержку!')
                    await member.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        self.user_db.start()
        self.transfer_check.start()

    @commands.Cog.listener()
    async def on_slash_command_error(self, interaction: disnake.CommandInteraction, error):
        embed = disnake.Embed(
            title=f'{interaction.user.display_name}',
            description=f'Неизвестная ошибка!',
            color=disnake.Color.red()
        )
        if isinstance(error, commands.MissingAnyRole):
            embed = disnake.Embed(
                title=f'{interaction.user.display_name}',
                description='У вас недостаточно прав для выполнения данной команды!',
                color=disnake.Color.red())
        await interaction.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Listeners(bot))
