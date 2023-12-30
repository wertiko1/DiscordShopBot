import disnake
import datetime
from ..utils.Data import DataBase
from ..utils.Payment import Payment


class PayModal(disnake.ui.Modal):
    def __init__(self):
        self.db = DataBase()
        self.pay = Payment()
        self.color = 0x2B2D31
        components = [
            disnake.ui.TextInput(
                label="Сумма",
                placeholder="Напишите сумму пополнения",
                custom_id="money",
                style=disnake.TextInputStyle.paragraph,
                min_length=1,
                max_length=32,
            ),
        ]
        super().__init__(title="Сумма", custom_id="money_modal", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        amount = inter.text_values['money']
        code = await self.pay.generate_label()
        url_pay = self.pay.create_invoice(amount=amount, label=code)
        embed = disnake.Embed(
            title=f'Платеж #{code}',
            description='Оплатите по ссылке ниже',
            color=self.color
        )
        embed.add_field(name='Сумма', value=f'```{amount}```')
        await inter.send(embed=embed, ephemeral=True, delete_after=5, components=[
            disnake.ui.Button(
                label="Ссылка",
                style=disnake.ButtonStyle.url,
                url=url_pay
            )
        ])
        await self.db.add_transfer(label=code, amount=amount, user=inter.author)


class PayButtons(disnake.ui.View):
    def __init__(self):
        self.db = DataBase()
        self.pay = Payment()
        self.color = 0x2B2D31
        super().__init__(timeout=60)

    @disnake.ui.button(label='YooMoney', style=disnake.ButtonStyle.primary, custom_id='yoomoney_button')
    async def payment_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(modal=PayModal())

    @disnake.ui.button(label='Soon...', style=disnake.ButtonStyle.grey, custom_id='soon_button', disabled=True)
    async def soon_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass
