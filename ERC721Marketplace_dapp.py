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
ABI = [{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"tokenAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenId","type":"uint256"},
    {"indexed":false,"internalType":"address","name":"customer","type":"address"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"}],"name":"BuyItem","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Cancel","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"auctionId","type":"uint256"},
    {"indexed":false,"internalType":"address","name":"tokenAddress","type":"address"},{"indexed":false,"internalType":"address","name":"customer","type":"address"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"},{"indexed":false,"internalType":"bool","name":"result","type":"bool"}],"name":"FinishAuction","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"tokenAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"}],"name":"ListItem","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"tokenAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"minPrice","type":"uint256"}],"name":"ListItemOnAuction","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"auctionId","type":"uint256"},{"indexed":false,"internalType":"address","name":"customer","type":"address"},{"indexed":false,"internalType":"uint256","name":"newBid","type":"uint256"}],"name":"MakeBid","type":"event"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"buyItem","outputs":[],"stateMutability":"payable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"cancel","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"_tokenId","type":"uint256"},
    {"internalType":"bytes","name":"_data","type":"bytes"}],"name":"checkOnERC721Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"bool","name":"_choice","type":"bool"},{"internalType":"uint256","name":"_price","type":"uint256"}],"name":"encryptData","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"finishAuction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"list","outputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},
    {"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"address","name":"tokenOwner","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"listAuction","outputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},
    {"internalType":"uint256","name":"currentPrice","type":"uint256"},{"internalType":"uint256","name":"time","type":"uint256"},{"internalType":"uint256","name":"bidCount","type":"uint256"},{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"address","name":"tokenOwner","type":"address"},{"internalType":"address","name":"lastCustomer","type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"listAuctionId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"listId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"makeBid","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"payable","type":"function"}]

Marketplace = w3.eth.contract(address='0x398469Db4212E43eBDcf985ABEf04df1C0977017', abi=ABI)

#  ====    Функции, отслеживающие события - НАЧАЛО   ====

def log_loop_list_item(event_filter, poll_interval):
    while True:
        while not print_event:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nNew token is for sale!")
            print(f"id item: {event['args']['id']}")
            print(f"token address: {event['args']['tokenAddress']}")
            print(f"token Id: {event['args']['tokenId']}")
            print(f"price: {event['args']['price']}\n")
        time.sleep(poll_interval)


def log_loop_buy_item(event_filter, poll_interval):
    while True:
        while not print_event:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nToken was bought")
            print(f"id item: {event['args']['id']}")
        time.sleep(poll_interval)


def log_loop_cancel(event_filter, poll_interval):
    while True:
        while not print_event:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nItem was cancelled")
            print(f"id item: {event['args']['id']}")
        time.sleep(poll_interval)


def log_loop_list_item_on_auction(event_filter, poll_interval):
    while True:
        while not print_event:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nNew token is on auction!")
            print(f"id item: {event['args']['id']}")
            print(f"token address: {event['args']['tokenAddress']}")
            print(f"token Id: {event['args']['tokenId']}")
            print(f"min price: {event['args']['price']}\n")
        time.sleep(poll_interval)


def log_loop_make_bid(event_filter, poll_interval):
    while True:
        while not print_event:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nNew bid")
            print(f"id item: {event['args']['id']}")
            print(f"price: {event['args']['price']}\n")
        time.sleep(poll_interval)


def log_loop_finish_auction(event_filter, poll_interval):
    while True:
        while not print_event:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nAuction was finished")
            print(f"id item: {event['args']['id']}")
            print(f"price: {event['args']['price']}\n")
        time.sleep(poll_interval)


#  ====    Функции, отслеживающие события - КОНЕЦ   ====


#  ====    Функции, для взаимодействия с контрактом бесплатные - НАЧАЛО    ====

def call_list_id():
    list_id = Marketplace.functions.listId().call()
    print(f"listId: {list_id}")
    menu()


def call_list_auction_id():
    list_auction_id = Marketplace.functions.listAuctionId().call()
    print(f"listAuctionId: {list_auction_id}")
    menu()


def call_list():
    n = int(input("Введите номер лота: "))
    list = Marketplace.functions.list(n).call()
    print(f"listItem: {list}")
    menu()
    
    
def call_list_auction():
    n = int(input("Введите номер лота на аукционе: "))
    list_auction = Marketplace.functions.listAuction(n).call()
    print(f"listAuction: {list_auction}")
    menu()
#  ====    Функции, для взаимодействия с контрактом бесплатные - КОНЕЦ    ====


#  ====    Функции, для взаимодействия с контрактом платные - НАЧАЛО    ====

def call_list_item():
    token_address = input("Укажите адрес токена: ")
    token_id = int(input("Укажите id токена: "))
    price = int(input("Укажите цену токена: "))
    # Создаём объект транзакции
    transaction = Marketplace.functions.listItem(token_address, token_id, price).build_transaction({
        'from': address,
        'chainId': 11155111,
        'gas': 300000,
        'maxFeePerGas': w3.eth.gas_price * 2,
        'nonce': w3.eth.get_transaction_count(address)
    })
    w3.eth.send_transaction(transaction)
    menu()


def call_buy_item():
    token_id = int(input("Укажите id токена для покупки: "))
    price = int(input("Укажите цену, которую хотите заплатить: "))
    transaction = Marketplace.functions.buyItem(token_id).build_transaction({
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
    transaction = Marketplace.functions.cancel(token_id).build_transaction({
        'from': address,
        'chainId': 11155111,
        'gas': 300000,
        'maxFeePerGas': w3.eth.gas_price * 2,
        'nonce': w3.eth.get_transaction_count(address)
    })
    w3.eth.send_transaction(transaction)
    menu()


def call_list_item_on_auction():
    token_address = input("Укажите адрес токена: ")
    token_id = int(input("Укажите id токена для выставления на аукцион: "))
    price = int(input("Укажите начальную ставку: "))
    transaction = Marketplace.functions.listItemOnAuction(token_address, token_id, price).build_transaction({
        'from': address,
        'chainId': 11155111,
        'gas': 300000,
        'maxFeePerGas': w3.eth.gas_price * 2,
        'nonce': w3.eth.get_transaction_count(address)
    })
    w3.eth.send_transaction(transaction)
    menu()


def call_make_bid():
    token_id = int(input("Укажите id токена для совершения ставки: "))
    price = int(input("Укажите сумму ставки: "))
    transaction = Marketplace.functions.makeBid(token_id).build_transaction({
        'from': address,
        'value': price,
        'chainId': 11155111,
        'gas': 300000,
        'maxFeePerGas': w3.eth.gas_price * 2,
        'nonce': w3.eth.get_transaction_count(address)
    })
    w3.eth.send_transaction(transaction)
    menu()


def call_finish_auction():
    token_id = int(input("Укажите id токена для окончания аукциона: "))
    transaction = Marketplace.functions.finishAuction(token_id).build_transaction({
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
        print("1. Узнать listId")
        print("2. Узнать listAuctionId")
        print("3. Получить информацию о лоте из словаря list")
        print("4. Получить информацию о лоте из словаря listAuction")
        print("5. Вызвать функцию listItem")
        print("6. Вызвать функцию buyItem")
        print("7. Вызвать функцию cancel")
        print("8. Вызвать функцию listItemOnAuction")
        print("9. Вызвать функцию makeBid")
        print("10. Вызвать функцию finishAuction")
        print("11. Настроить отслеживание событий")
        print("12. Выйти из программы")
        choice = int(input("\nВведите номер пункта меню, который выбрали: "))
        if choice == 1:
            call_list_id()
        elif choice == 2:
            call_list_auction_id()
        elif choice == 3:
            call_list()
        elif choice == 4:
            call_list_auction()
        elif choice == 5:
            call_list_item()
        elif choice == 6:
            call_buy_item()
        elif choice == 7:
            call_cancel()
        elif choice == 8:
            call_list_item_on_auction()
        elif choice == 9:
            call_make_bid()
        elif choice == 10:
            call_finish_auction()
        elif choice == 11:
            event_tracking_setup()
        elif choice == 12:
            exit()


def main():

    # создание фильтров
    event_filter_list_item = Marketplace.events.ListItem.create_filter(fromBlock="latest")
    event_filter_buy_item = Marketplace.events.BuyItem.create_filter(fromBlock="latest")
    event_filter_cancel = Marketplace.events.Cancel.create_filter(fromBlock="latest")
    event_filter_list_item_on_auction = Marketplace.events.ListItemOnAuction.create_filter(fromBlock="latest")
    event_filter_make_bid = Marketplace.events.MakeBid.create_filter(fromBlock="latest")
    event_filter_finish_auction = Marketplace.events.FinishAuction.create_filter(fromBlock="latest")

    # создание потоков
    event_thread_list_item = Thread(target=log_loop_list_item, args=(event_filter_list_item, 10), daemon=True)
    event_thread_buy_item = Thread(target=log_loop_buy_item, args=(event_filter_buy_item, 10), daemon=True)
    event_thread_cancel = Thread(target=log_loop_cancel, args=(event_filter_cancel, 10), daemon=True)
    event_thread_list_item_on_auction = Thread(target=log_loop_list_item_on_auction, args=(event_filter_list_item_on_auction, 10), daemon=True)
    event_thread_make_bid = Thread(target=log_loop_make_bid, args=(event_filter_make_bid, 10), daemon=True)
    event_thread_finish_auction = Thread(target=log_loop_finish_auction, args=(event_filter_finish_auction, 10), daemon=True)

    # запуск потоков
    event_thread_list_item.start()
    event_thread_buy_item.start()
    event_thread_cancel.start()
    event_thread_list_item_on_auction.start()
    event_thread_make_bid.start()
    event_thread_finish_auction.start()

    # запуск меню
    event_tracking_setup()

#  ====    Прочие функции - КОНЕЦ    ====


if __name__ == '__main__':
    main()
