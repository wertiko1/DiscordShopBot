import disnake
from disnake.ext import commands
from .views.PayButton import PayButtons
from .utils.Data import DataBase


class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DataBase()
        self.color = 0x2B2D31

    @commands.has_any_role(1184845622830973008)
    @commands.command(name='payment')
    async def create_payment(self, ctx: commands.Context):
        embed = disnake.Embed(
            title='Спонсирование сервера',
            description='**Привет!** Мы хотели бы обратиться к нашим замечательным игрокам '
                        'с просьбой о финансовой поддержке нашего сервера. \nМы полность'
                        'ю осознаем, что не каждый человек может себе позволить проход'
                        'ку, поэтому у нас есть специальная спонсорская подписка для т'
                        'ех, кто желает помочь. \n\nВсего за **99** рублей в месяц, вы можете получить'
                        ' подписку\n\n'
                        'Для этого на нашем сервере реализована система платежей, котора'
                        'я позволяет вам пополнить баланс по кнопке ниже и купить ту или иную привилегию.\n'
                        '\nТакже вы можете купить гифт своему другу или же получить реферал'
                        'ьный промокод, который даст скидку вашему другу и вернет вам часть потраченных денег!\n'
                        '\nПодробнее ознакомиться с подпиской можно по '
                        'команде',
            color=self.color
        )
        await ctx.send(embed=embed, components=[
            disnake.ui.Button(label="Пополнить",
                              style=disnake.ButtonStyle.success,
                              custom_id="payment_button"),
        ])
        await ctx.message.delete()

    @commands.Cog.listener('on_button_click')
    async def pay_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["payment_button"]:
            return
        embed = disnake.Embed(title='Способ оплаты',
                              description='Выберите способ оплаты',
                              color=self.color
                              )
        embed.add_field(name='YooMoney', value='Поддерживает банковские карты\n'
                                               '- **Visa**\n'
                                               '- **Mastercard**\n'
                                               '- **Мир**',
                        inline=False)
        embed.add_field(name='Внимание',
                        value='Прошу обратить внимание, что нельзя оплачивать **по '
                              'одной ссылке два раза и более**, иначе ваш платеж **не '
                              'будет зачислен**!\nТакже желательно, чтобы вы сохрани'
                              'ли чек об оплате!\nЕсли у вас возникнут проблемы напишите в <#1184150472240672799>!',
                        inline=False)
        embed.set_thumbnail(url=inter.guild.icon.url)
        embed.set_footer(text='В дальнейшем будут другие способы оплаты')
        await inter.send(embed=embed, view=PayButtons(), ephemeral=True)

    @commands.slash_command(name='профиль', description='Посмотреть ваш профиль')
    async def profile(self, inter):
        user = await self.db.get_user(inter.author)
        embed = disnake.Embed(
            title=f'Профиль {inter.author.display_name}',
            color=self.color
        ).set_thumbnail(url=inter.author.display_avatar.url)
        embed.add_field(name='Баланс', value=f'```{user[2]}```', inline=False)
        roles = inter.author.roles
        role = inter.guild.get_role(1184898031510900736)
        if role in roles:
            embed.add_field(name='Подписка', value=f'Продлена до', inline=False)
        else:
            embed.add_field(name='Подписка', value='Отсутствует')
        await inter.send(embed=embed)

    @commands.has_any_role(1184845622830973008)
    @commands.slash_command(name='выдать-валюту', description='Выдать или забрать валюту')
    async def edit_money(self, inter,
                         member: disnake.Member = commands.Param(name='пользователь',
                                                                 description='Целевой пользователь'),
                         amount: int = commands.Param(name='cумма', description='Колличество валюты')):
        await self.db.add_money(amount=amount, user_id=member.id)
        embed = disnake.Embed(
            title=f'Изменен баланс {member.display_name}',
            color=self.color
        ).set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name='Сумма', value=f'```{amount}```', inline=False)
        await inter.send(embed=embed, ephemeral=True)
        embed.set_footer(text=f'Изменил {inter.author.display_name}', icon_url=inter.author.display_avatar.url)
        channel = inter.guild.get_channel(1188387508640297042)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(UserCommands(bot))
