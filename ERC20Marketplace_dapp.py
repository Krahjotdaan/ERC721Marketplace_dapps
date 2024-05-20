from web3 import Web3, HTTPProvider
from threading import Thread
import time
from keys import *


w3 = Web3(HTTPProvider(PROVIDER))

# информация о пользователе
address = ADDRESS
private_key = PRIVATE_KEY

# включаем/отключаем вывод информации о новых событиях
print_event = True

# создание инстанса контракта
true = True
false = False
ABI = [{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"lotId","type":"uint256"},
    {"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Cancel","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"lotId","type":"uint256"},
    {"indexed":false,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"address","name":"tokenAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ListLot","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"lotId","type":"uint256"},
    {"indexed":false,"internalType":"address","name":"tokenAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"address","name":"customer","type":"address"}],"name":"Purchase","type":"event"},
    {"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"cancel","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"list","outputs":[{"internalType":"address","name":"tokenAddress","type":"address"},
    {"internalType":"address","name":"tokenOwner","type":"address"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_tokenAddress","type":"address"},{"internalType":"uint256","name":"_price","type":"uint256"},
    {"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"listLot","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[],"name":"lotId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"purchase","outputs":[],"stateMutability":"payable","type":"function"}]

Marketplace = w3.eth.contract(address='0x90D646a8b170E1c256874F760985BADf467B37D6', abi=ABI)

#  ====    Функции, отслеживающие события - НАЧАЛО   ====

def log_loop_list_lot(event_filter, poll_interval):
    while True:
        while not print_event:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nNew lot is for sale!")
            print(f"id lot: {event['args']['id']}")
            print(f"token address: {event['args']['tokenAddress']}")
            print(f"token Id: {event['args']['tokenId']}")
            print(f"price: {event['args']['price']}\n")
            print(f"amount: {event['args']['amount']}\n")
        time.sleep(poll_interval)


def log_loop_purchase(event_filter, poll_interval):
    while True:
        while not print_event:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nTokens were bought")
            print(f"id lot: {event['args']['id']}")
            print(f"token address: {event['args']['tokenAddress']}")
            print(f"price: {event['args']['price']}\n")
            print(f"amount: {event['args']['amount']}\n")
            print(f"customer: {event['args']['customer']}\n")
        time.sleep(poll_interval)


def log_loop_cancel(event_filter, poll_interval):
    while True:
        while not print_event:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nItem was cancelled")
            print(f"id item: {event['args']['id']}")
            print(f"amount: {event['args']['amount']}\n")
        time.sleep(poll_interval)

#  ====    Функции, отслеживающие события - КОНЕЦ   ====


#  ====    Функции, для взаимодействия с контрактом бесплатные - НАЧАЛО    ====

def call_lot_id():
    list_id = Marketplace.functions.lotId().call()
    print(f"listId: {list_id}")
    menu()


def call_list():
    n = int(input("Введите номер лота: "))
    list = Marketplace.functions.list(n).call()
    print(f"lotId: {n}")
    print(f"tokenAddress: {list[0]}")
    print(f"tokenOwner: {list[1]}")
    print(f"price: {list[2]}")
    print(f"amount: {list[3]}")
    menu()
    
#  ====    Функции, для взаимодействия с контрактом бесплатные - КОНЕЦ    ====


#  ====    Функции, для взаимодействия с контрактом платные - НАЧАЛО    ====

def call_list_lot():
    token_address = input("Укажите адрес токена: ")
    price = int(input("Укажите цену за 1 токен: "))
    amount = int(input("Укажите количество токенов: "))
    # Создаём объект транзакции
    transaction = Marketplace.functions.listItem(token_address, price, amount).build_transaction({
        'from': address,
        'chainId': 11155111,
        'gas': 300000,
        'maxFeePerGas': w3.eth.gas_price * 2,
        'nonce': w3.eth.get_transaction_count(address)
    })
    w3.eth.send_transaction(transaction)
    menu()


def call_purchase():
    token_id = int(input("Укажите id лота для покупки: "))
    price = int(input("Укажите цену, которую хотите заплатить: "))
    amount = int(input("Укажите количество токенов, которое хотите купить: "))
    transaction = Marketplace.functions.purchase(token_id, amount).build_transaction({
        'from': address,
        'value': price,
        'chainId': 11155111,
        'gas': 300000,
        'maxFeePerGas': w3.eth.gas_price * 2,
        'nonce': w3.eth.get_transaction_count(address)
    })
    w3.eth.send_transaction(transaction)
    menu()


def call_cancel():
    token_id = int(input("Укажите id токена для отмены: "))
    amount = int(input("Укажите количество токенов для отмены: "))
    transaction = Marketplace.functions.cancel(token_id, amount).build_transaction({
        'from': address,
        'chainId': 11155111,
        'gas': 300000,
        'maxFeePerGas': w3.eth.gas_price * 2,
        'nonce': w3.eth.get_transaction_count(address)
    })
    w3.eth.send_transaction(transaction)
    menu()

#  ====    Функции, для взаимодействия с контрактом платные - КОНЕЦ    ====


#  ====    Прочие функции - НАЧАЛО    ====

def event_tracking_setup():
    global print_event
    print("1. Выводить сообщения о новых событиях")
    print("2. НЕ выводить сообщения о новых событиях")
    choice = int(input("\nВведите номер пункта меню, который выбрали: "))
    if choice == 1:
        print_event = True
    elif choice == 2:
        print_event = False
    menu()


def menu():
    while True:
        print("\nЧто будем делать?")
        print("1. Узнать lotId")
        print("2. Получить информацию о лоте из словаря list")
        print("3. Вызвать функцию listLot")
        print("4. Вызвать функцию purchase")
        print("5. Вызвать функцию cancel")
        print("6. Настроить отслеживание событий")
        print("7. Выйти из программы")
        choice = int(input("\nВведите номер пункта меню, который выбрали: "))
        if choice == 1:
            call_lot_id()
        elif choice == 2:
            call_list()
        elif choice == 3:
            call_list_lot()
        elif choice == 4:
            call_purchase()
        elif choice == 5:
            call_cancel()
        elif choice == 6:
            event_tracking_setup()
        elif choice == 7:
            exit()


def main():

    # создание фильтров
    event_filter_list_lot = Marketplace.events.ListLot.create_filter(fromBlock="latest")
    event_filter_purchase = Marketplace.events.Purchase.create_filter(fromBlock="latest")
    event_filter_cancel = Marketplace.events.Cancel.create_filter(fromBlock="latest")

    # создание потоков
    event_thread_list_lot = Thread(target=log_loop_list_lot, args=(event_filter_list_lot, 10), daemon=True)
    event_thread_purchase = Thread(target=log_loop_purchase, args=(event_filter_purchase, 10), daemon=True)
    event_thread_cancel = Thread(target=log_loop_cancel, args=(event_filter_cancel, 10), daemon=True)

    # запуск потоков
    event_thread_list_lot.start()
    event_thread_purchase.start()
    event_thread_cancel.start()

    # запуск меню
    event_tracking_setup()

#  ====    Прочие функции - КОНЕЦ    ====


if __name__ == '__main__':
    main()
