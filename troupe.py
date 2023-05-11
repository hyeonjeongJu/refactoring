import locale
import math
import json

class Troupe():
    def format(self, amount):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        return locale.currency(amount, symbol=True, grouping=True)
    
    def statement(self, invoice, plays):
        total_amount = 0
        volume_credits = 0
        result = f'청구 내역 (고객명: {invoice["customer"]})\n'

        for perf in invoice['performances']:
            play = plays[perf['playID']]
            this_amount = 0

            # 비극
            if play['type'] == 'tragedy':
                this_amount = 40000
                if perf['audience'] > 30:
                    this_amount += 1000 * (perf['audience'] - 30)
            # 희극
            elif play['type'] == 'comedy':
                this_amount = 30000
                if perf['audience'] > 20:
                    this_amount += 10000 + 500 * (perf['audience'] - 20)
                this_amount += 300 * perf['audience']
            else:
                raise Exception(f'알 수 없는 장르: {play["type"]}')
            
            # 포인트를 적립한다.
            volume_credits += max(perf['audience'] - 30, 0)
            # 희극 관객 5명마다 추가 포인트를 제공한다.
            if 'comedy' == play['type']:
                volume_credits += math.floor(perf['audience'] / 5)

            # 청구 내역을 출력한다.
            result += f'{play["name"]}: {self.format(this_amount/100)} {perf["audience"]}석\n'
            total_amount += this_amount

        result += f'총액: {self.format(total_amount/100)}\n'
        result += f'적립 포인트: {volume_credits}점\n'
        return result


if __name__ == '__main__':
    invoice = ''
    plays = ''

    with open('invoices.json') as f:
        invoice = json.load(f)

    with open('plays.json') as f:
        plays = json.load(f)
    
    #print(type(invoices))
    #print(type(plays))
    print(Troupe().statement(invoice=invoice[0], plays=plays))