import time
import threading
from datetime import datetime
from kucoin.client import Client

# Kucoin keys
API_PUBLIC_KEY = ''
API_SECRET_KEY = ''
PASSPHRASE = ''


# Inputs and sends
print("Activated")
print()
time.sleep(1)

# Receiving user input
coin = str(input("What is the coin you would like to thread : ").upper())
amount_usdt = str(input("How many dollars worth of {} would you like to thread : ".format(coin)))
IEO_time = input("What time is the IEO? (HH:MM:SS) : ")
print()

# The complex timer
# Calculating Time to start the thread
IEO_hour_time = int(IEO_time[:2])
IEO_minute_time = int(IEO_time[3:5])
IEO_second_time = int(IEO_time[6:8])


thread_start_hour = IEO_hour_time - 1
thread_start_minute = 59
thread_start_second = 29

thread_starting_at = "{}:{}:{}".format(thread_start_hour, thread_start_minute, thread_start_second)

# Calculating The current time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_hour_time = int(current_time[:2])
current_minute_time = int(current_time[3:5])
current_second_time = int(current_time[6:8])

# Calculating how long the timer needs to wait for
wait_till_thread_hour = thread_start_hour - current_hour_time
wait_till_thread_minute = thread_start_minute - current_minute_time
if thread_start_second > current_second_time:
    wait_till_thread_second = thread_start_second - current_second_time
elif current_second_time > thread_start_second:
    wait_till_thread_second = current_second_time - thread_start_second
else:
    wait_till_thread_second = 0

# Default sleep times
time_sleep_hour = 0
time_sleep_minute = 0
time_sleep_second = 0

# Calculating amount of SECONDS it needs to sleep
if wait_till_thread_hour != 0:
    time_sleep_hour += ((wait_till_thread_hour * 60)*60)
if wait_till_thread_minute != 0:
    time_sleep_minute += (wait_till_thread_minute * 60)
if wait_till_thread_second != 0:
    time_sleep_second += wait_till_thread_second
seconds_to_sleep = int(time_sleep_hour + time_sleep_minute + time_sleep_second)

# Sending confirmation messages
print("I will start threading to buy ${} of \"{}\" at {}, the IEO is at {}:00:00."
      .format(amount_usdt, coin, thread_starting_at, IEO_hour_time))
print()

# Actually sleeping
time.sleep(seconds_to_sleep)

# Sending threading has begun message
now_deploy_thread = datetime.now()
deploy_thread_time = now_deploy_thread.strftime("%H:%M:%S")
print("The time is {} and im now deploying threading".format(deploy_thread_time))

# Starting threading (sending buy orders)
client = Client(API_PUBLIC_KEY, API_SECRET_KEY, PASSPHRASE)


def the_order():
    max_threads = 200
    for i in range(max_threads):
        try:
            order_coin = coin + "-USDT"
            client.create_market_order(order_coin, Client.SIDE_BUY, funds=amount_usdt)
        except:
            pass


dot_join_threads = []
number_of_threads = 8
for _ in range(number_of_threads):
    t = threading.Thread(target=the_order)
    t.start()
    dot_join_threads.append(t)

for thread in dot_join_threads:
    thread.join()

# Sending threading has finished message
now_after_deploy_thread = datetime.now()
after_deploy_thread_time = now_after_deploy_thread.strftime("%H:%M:%S")
print("\nThe time is {} and i've finished deploying threading".format(after_deploy_thread_time))

# Pulling available amount of coin
time.sleep(1)
all_balance = client.get_accounts()
for balance in all_balance:
    l_balance = list(balance.items())
    if l_balance[1][1] == coin and l_balance[2][1] == "trade":
        buy_amount = l_balance[4][1]
        break
    else:
        buy_amount = 1

# Getting results

# Buy price
buy_price = float(amount_usdt) / float(buy_amount)
rounded_buy_price = "{:0f}".format(buy_price)

# Order filled time
order_filled_time = "-"

# Amount purchased
amount_purchased = buy_amount

# Getting end price of coin before it sends
ticker = client.get_ticker('{}-USDT'.format(coin))
price_of_coin = ticker["price"]

# Formatting and sending results
time.sleep(3)

print("\nMission success, you bought ${} worth of {} with a buy price of ${}. "
      "{} is currently ${} and you brought {} of them."
      .format(amount_usdt, coin, rounded_buy_price, coin, price_of_coin, amount_purchased))

# Closing 
time.sleep(4)
print("\nDeactivated")
