from random import randint
from .Data import DataBase
from yoomoney import Quickpay, Client


token = ("YOUR TOKEN")
card = 'YOUR CARD'


class Payment:
    def __init__(self):
        self.token = token
        self.card = card
        self.data = DataBase()

    async def generate_label(self):
        while True:
            code = randint(1000000, 9999999)
            flag = await self.data.get_labels(str(code))
            if not flag:
                break
        return code

    def create_invoice(self, amount: int, label: str):
        quick_pay = Quickpay(
            receiver=self.card,
            quickpay_form="shop",
            targets='Flonium', # название
            paymentType="AC", # способ оплаты можно найти на сайте yoomoney
            sum=amount,
            label=label
        )
        return quick_pay.base_url

    def check_invoice(self):
        client = Client(self.token)
        history = client.operation_history()
        return history.operations
