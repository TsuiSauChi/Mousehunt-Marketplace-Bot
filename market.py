import requests
import time
import random
import telegram
import asyncio

sb_id = "114"

class Tele:

    def __init__(self):
        self.token = "6241793271:AAEf4myHKt3GWi38O3LqmPSOZKR8_IW20KE"
        self.userid = "335838693"
        self.bot = telegram.Bot(token=self.token)

    # Send the message
    async def send_message(self, message):
        await self.bot.send_message(chat_id=self.userid, text=message, parse_mode= 'HTML')

# Get Market Price
def market_price(item_id, action):

    payload = {
        "action": action,
        "item_id": item_id
    }

    return requests.post(
        url='https://www.mousehuntgame.com/managers/ajax/users/marketplace.php',
        # Might be better to replace this with an alt account session
        headers={
            "cookie": "HG_TOKEN=NVL2CCHS2UADDOdt7fuVA70cosGG4yZ7f2WuQEPOfUtPf80889AFGepAmy4NX7xR; __utma=22815271.62290836.1654940521.1673995035.1674736318.1452; __utmz=22815271.1655206651.34.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _fbp=fb.1.1654940529042.1017060308; __gads=ID=9526a11783dd893f-22d97cf156d40029:T=1654940530:RT=1654940530:S=ALNI_MaRSLPFvUxO7IKCZnm3EYbf2Hb3sQ; __gpi=UID=0000068bfc747600:T=1654940530:RT=1674736320:S=ALNI_MZPQgO-_5jWzhgeBDXQeo8SYzccsQ; has_logged_in=true; _gcl_au=1.1.2028202828.1673615785; hg_session[startTime]=1674736314; hg_session[sessionId]=qKJygASmfLbVZzeiwc01eREd4RsQ0jXd; hg_session[sessionNum]=5116; __utmb=22815271.7.10.1674736318; __utmt=1; __utmc=22815271" },
        data= payload
    )

# Get My Listings
def listings():

    payload = {
        "action": "marketplace_info",
        "uh": "kkbjNp45"
    }

    my_listings = requests.post(
        url='https://www.mousehuntgame.com/managers/ajax/users/marketplace.php',
        # Might be better to replace this with an alt account session
        headers={
            "cookie": "HG_TOKEN=ScS7S3rkHO0V178jybtTIY65e8zWQX9I2x4bVSe0En36ZJ6wFO9yrA471lFyb8qw; __gads=ID=4c40522d98f5a160-2293b4a02ad3005d:T=1652427048:RT=1652427048:S=ALNI_MZYbyUAyrTNSnw8HSITy2HpUyC1gA; _fbp=fb.1.1652427047793.1382279138; has_logged_in=true; __utmz=22815271.1653389734.62.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _gcl_au=1.1.1771050419.1668820315; __utma=22815271.1814857960.1652427047.1673888252.1673932918.1353; __utmc=22815271; __utmt=1; __gpi=UID=000005514ac0dc17:T=1652524938:RT=1673932919:S=ALNI_MYeBnAYT-MqKKf0ryttTHz7c2AKTw; __utmb=22815271.2.10.1673932918"
        },
        data= payload
    )

    return my_listings.json()["marketplace_my_listings"]

def cancel_listing(listing_id):
    payload = {
        "sn": "Hitgrab",
        "hg_is_ajax": "1",
        "action": "cancel",
        "listing_id": listing_id,
        "uh": "kkbjNp45"
    }
    
    return requests.post(
        url = "https://www.mousehuntgame.com/managers/ajax/users/marketplace.php",
        headers={
            "cookie": "HG_TOKEN=ScS7S3rkHO0V178jybtTIY65e8zWQX9I2x4bVSe0En36ZJ6wFO9yrA471lFyb8qw; __gads=ID=4c40522d98f5a160-2293b4a02ad3005d:T=1652427048:RT=1652427048:S=ALNI_MZYbyUAyrTNSnw8HSITy2HpUyC1gA; _fbp=fb.1.1652427047793.1382279138; has_logged_in=true; __utmz=22815271.1653389734.62.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _gcl_au=1.1.1771050419.1668820315; __utma=22815271.1814857960.1652427047.1673888252.1673932918.1353; __utmc=22815271; __utmt=1; __gpi=UID=000005514ac0dc17:T=1652524938:RT=1673932919:S=ALNI_MYeBnAYT-MqKKf0ryttTHz7c2AKTw; __utmb=22815271.2.10.1673932918"
        },
        data= payload
    )

def claim_listing(listing_id):
    payload = {
        "sn": "Hitgrab",
        "hg_is_ajax": "1",
        "action": "claim",
        "listing_id": listing_id,
        "uh": "kkbjNp45",
    }

    return requests.post(
        url = "https://www.mousehuntgame.com/managers/ajax/users/marketplace.php",
        headers={
            "cookie": "HG_TOKEN=ScS7S3rkHO0V178jybtTIY65e8zWQX9I2x4bVSe0En36ZJ6wFO9yrA471lFyb8qw; __gads=ID=4c40522d98f5a160-2293b4a02ad3005d:T=1652427048:RT=1652427048:S=ALNI_MZYbyUAyrTNSnw8HSITy2HpUyC1gA; _fbp=fb.1.1652427047793.1382279138; has_logged_in=true; __utmz=22815271.1653389734.62.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _gcl_au=1.1.1771050419.1668820315; __utma=22815271.1814857960.1652427047.1673888252.1673932918.1353; __utmc=22815271; __utmt=1; __gpi=UID=000005514ac0dc17:T=1652524938:RT=1673932919:S=ALNI_MYeBnAYT-MqKKf0ryttTHz7c2AKTw; __utmb=22815271.2.10.1673932918"
        },
        data= payload
    )

def purchase_order(item_id, price, unit):
    payload = {
        "sn": "Hitgrab",
        "hg_is_ajax": "1",
        "action": "create",
        "item_id": item_id,
        "unit_price": price,
        "quantity": unit,
        "listing_type": "buy",
        "uh": "kkbjNp45"
    }
    return requests.post(
        url = "https://www.mousehuntgame.com/managers/ajax/users/marketplace.php",
        headers={
            "cookie": "HG_TOKEN=ScS7S3rkHO0V178jybtTIY65e8zWQX9I2x4bVSe0En36ZJ6wFO9yrA471lFyb8qw; __gads=ID=4c40522d98f5a160-2293b4a02ad3005d:T=1652427048:RT=1652427048:S=ALNI_MZYbyUAyrTNSnw8HSITy2HpUyC1gA; _fbp=fb.1.1652427047793.1382279138; has_logged_in=true; __utmz=22815271.1653389734.62.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _gcl_au=1.1.1771050419.1668820315; __utma=22815271.1814857960.1652427047.1673888252.1673932918.1353; __utmc=22815271; __utmt=1; __gpi=UID=000005514ac0dc17:T=1652524938:RT=1673932919:S=ALNI_MYeBnAYT-MqKKf0ryttTHz7c2AKTw; __utmb=22815271.2.10.1673932918"
        },
        data= payload
    )

def sale_order(item_id, price, unit):
    payload = {
        "sn": "Hitgrab",
        "hg_is_ajax": "1",
        "action": "create",
        "item_id": item_id,
        "unit_price": price,
        "quantity": unit,
        "listing_type": "sell",
        "uh": "kkbjNp45"
    }
    return requests.post(
        url = "https://www.mousehuntgame.com/managers/ajax/users/marketplace.php",
        headers={
            "cookie": "HG_TOKEN=ScS7S3rkHO0V178jybtTIY65e8zWQX9I2x4bVSe0En36ZJ6wFO9yrA471lFyb8qw; __gads=ID=4c40522d98f5a160-2293b4a02ad3005d:T=1652427048:RT=1652427048:S=ALNI_MZYbyUAyrTNSnw8HSITy2HpUyC1gA; _fbp=fb.1.1652427047793.1382279138; has_logged_in=true; __utmz=22815271.1653389734.62.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _gcl_au=1.1.1771050419.1668820315; __utma=22815271.1814857960.1652427047.1673888252.1673932918.1353; __utmc=22815271; __utmt=1; __gpi=UID=000005514ac0dc17:T=1652524938:RT=1673932919:S=ALNI_MYeBnAYT-MqKKf0ryttTHz7c2AKTw; __utmb=22815271.2.10.1673932918"
        },
        data= payload
    )

def check_profit_aginst_threshold(buy, sell, sb_sell_price, threshold, message):
    profit = (sell - buy) / sb_sell_price
    message += "Profit: " + str(profit) + "\n"
    if profit > threshold:
        return 1, message
    else:
        return 0, message

def check_rebuy_condition(market, rebuy_price, listed_price, message):
    # Check if listed price is most expensive
    if int(rebuy_price) <= listed_price:
        message += "Listed most ex\n"
        return 0, message
    # Condition for item 50k or less; Bottled Wind
    # ToDo: Come back here
    if (int(rebuy_price) < 50000):
        message += "Less then 50k\n"
        quantity_condition = 50
        quantity = market[0]["quantity"]
        difference_condition = 50
        difference = market[0]["unit_price"]-listed_price
         
        message += "Difference " + str(difference) + "\n"
        message += "Quantity " + str(quantity) + "\n"
        if ((difference > difference_condition) or (quantity < quantity_condition)):
            message += "Difference too huge\n"
            return 0, message
        else:
            message += "Condition passeed\n"
            return 1, message
    message += "Condition passeed\n"
    return 1, message

# Need to add condition here
def check_resell_condition(market, resell_price, listed_price, message):
    # Check if listed price is most expensive

    if int(resell_price) >= listed_price:
        message += "Listed is cheapest\n"
        return 0, message

    # Condition for item 120k or less; Wild Tonic
    # ToDo: Come back here
    if (int(resell_price) < 120000):
        message += "Condition: Less then 120k\n"
        # Change to 20
        quantity_condition = 20
        quantity = market[0]["quantity"]
        difference_condition = 200
        difference = listed_price-market[0]["unit_price"]
        message += "Difference " + str(difference) + "\n"
        message += "Quantity " + str(quantity) + "\n"
        if ((difference > difference_condition) or (quantity < quantity_condition)):
            message += "Difference too huge\n"
            return 0, message
        else:
            message += "Condition passeed\n"
            return 1, message
    message += "Condition passeed\n"
    return 1, message

sb_market = market_price(sb_id, action="get_item_listings")
sb_sell_price = sb_market.json()["marketplace_item_listings"][sb_id]['sell'][0]["unit_price"]
sb_buy_price = sb_market.json()["marketplace_item_listings"][sb_id]['buy'][0]["unit_price"]


def to_buy(item_id, sb_sell_price, threshold, quantity, discord_price, message):
    market = market_price(item_id, action="get_item_listings")
    buy_price = market.json()["marketplace_item_listings"][item_id]['buy'][0]["unit_price"]
    sell_price = (sb_sell_price * discord_price) * 9/10
    
    my_listings = listings()
    for i in my_listings:
        if str(i["item_id"]) == item_id and str(i["listing_type"]) == "buy" and str(i["is_active"] == "1"):
            listing_id = i["listing_id"]
            my_listed_price = int(i["unit_price"])
            message += "Listed Price: " + str(my_listed_price) + "\n"

            _, message = check_profit_aginst_threshold(buy_price, sell_price, sb_sell_price, threshold, message)

            # Check conditions
            result, message = check_rebuy_condition(
                market.json()["marketplace_item_listings"][item_id]['buy'], 
                buy_price, 
                my_listed_price,
                message)
            
            if(result):
                to_list = buy_price + 1
                # Check if new price is profitable above threshold amount
                to_buy, message = check_profit_aginst_threshold(to_list, sell_price, sb_sell_price, threshold, message)
                if to_buy:
                    message += "Re-buying at " + str(to_list) + "each\n"
                    # Cancel existing listing
                    cancel_listing(listing_id)
                    # Make purchase order
                    purchase_order(item_id, to_list, quantity)
                else:
                    message += "Does not qualify profit threshold\n"
    return message

def to_sell(item_id, threshold, message):
    # Start testing here
    market = market_price(item_id, action="get_item_listings")
    sell_price = market.json()["marketplace_item_listings"][item_id]['sell'][0]["unit_price"]

    my_listings = listings()
    for i in my_listings:
        if str(i["item_id"]) == item_id and str(i["listing_type"]) == "sell" and str(i["is_active"] == "1"):
            listing_id = i["listing_id"]
            remaining_quantity = i["remaining_quantity"]
            gold_escrow = i["gold_escrow"]
            my_listed_price = int(i["unit_price"])

            # Claim gold escow
            if int(gold_escrow) > 0:
                message += "Gold Escow:" + str(gold_escrow) +"\n"
                claim_listing(listing_id)

            message += "Listed Price: " + str(my_listed_price) + "\n"

            result, message = check_resell_condition(
                market.json()["marketplace_item_listings"][item_id]['sell'],
                sell_price, 
                my_listed_price,
                message)

            if(result):
                to_list = sell_price - 1
                if (to_list > threshold):

                    message += "Re-Selling at " + str(to_list) + "each\n"
                    cancel_listing(listing_id)
                    sale_order(item_id, to_list, remaining_quantity)
                else:
                    message += "Does not qualify sale threshold\n"
    return message

# Periodically send the message
loop = asyncio.get_event_loop()
tele = Tele()

while True:

    message = ""
    message += "<b>Purchase Order</b>\n"

    message += "\n<u>Bottled Wind</u>\n"
    message = to_buy(
        item_id="3070",
        sb_sell_price=sb_sell_price,
        threshold=0.15,
        quantity=500,
        discord_price=(3.8),
        message = message
    )

    # GGC
    # message += "\n<u>GGC</u>\n"
    # message = to_buy(
    #     item_id="1733",
    #     sb_sell_price=sb_sell_price,
    #     threshold=0.05,
    #     quantity=1000,
    #     discord_price=(0.8),
    #     message = message
    # )

    message += "\n<u>Rare Map Crafter Kit</u>\n"
    message = to_buy(
        item_id="2670",
        sb_sell_price=sb_sell_price,
        threshold=950,
        quantity=1,
        discord_price=((415 * 40) + 200 + 1100),
        message = message
    )

    # message += "\n<u>Rare Map Dust</u>\n"
    # message = to_buy(
    #     item_id="926",
    #     sb_sell_price=sb_sell_price,
    #     threshold=10,
    #     quantity=5,
    #     discord_price=(420),
    #     message = message
    # )

    # message += "\n<u>Folklore Forest Large Supply Kit</u>\n"
    # message = to_buy(
    #     item_id="3440",
    #     sb_sell_price=sb_sell_price, 
    #     threshold=1000,
    #     quantity=1,
    #     discord_price=((650*17)+650+1150),
    #     message = message
    # )

    # message += "\n<u>Kalor'ignis Rib</u>\n"
    # message = to_buy(
    #     item_id="2833",
    #     sb_sell_price=sb_sell_price,
    #     threshold=250,
    #     quantity=1,
    #     discord_price=(3500),
    #     message = message
    # )

    # message += "\n<u>Timesplit Rune</u>\n"
    # message = to_buy(
    #     item_id="2340",
    #     sb_sell_price=sb_sell_price,
    #     threshold=15,
    #     quantity=8,
    #     discord_price=(190),
    #     message = message
    # )

    # message += "\n<u>Gilded Charm</u>\n"
    # message = to_buy(
    #     item_id="2174",
    #     sb_sell_price=sb_sell_price,
    #     threshold=0.8,
    #     quantity=1000,
    #     discord_price=(1.9),
    #     message = message
    # )

    message += "\n------\n"
    message += "<b>Sale Order</b>\n"

    message += "\n<u>Speedy Coggy Colby</u>\n"
    message = to_sell(
        item_id="3188",
        threshold = 86000,
        message = message
    )

    # message += "\n<u>Party Size Gilded Birthday Scroll Case</u>\n"
    # message = to_sell(
    #     item_id="3175",
    #     threshold = 62000000,
    #     message = message
    # )

    # message += "\n<u>Super Brie</u>\n"
    # message = to_sell(
    #     item_id="114",
    #     threshold = 15500,
    #     message = message
    # )

    # message += "\n<u>Wild Tonic</u>\n"
    # message = to_sell(
    #     item_id="2619",
    #     threshold = 121500,
    #     message = message
    # )

    message += "\n######\n"

    second = random.randint(100, 200)
    print("Running again at " + str(second) + "sec")
    message += "Running again at " + str(second) + "sec\n"

    loop.run_until_complete(tele.send_message(message))

    # Pause for 30mins 
    time.sleep(second)


# Previous Code

# Timesplit Rune
# print("Timesplit Rune")
# message += "\n<u>Timesplit Rune</u>\n"
# message = to_buy(
#     item_id="2340",
#     sb_sell_price=sb_sell_price,
#     threshold=15,
#     quantity=7,
#     discord_price=(195),
#     message = message
# )


# Folklore Forest Large Supply Kit
# Threshold = 80
# print("Folklore Forest Large Supply Kit")
# to_buy(
#     item_id="3440",
#     sb_sell_price=sb_sell_price, 
#     threshold=500,
#     quantity=1,
#     discord_price=((650*20) + 1180)
# )

# Rare Map Dust
# print("Rare Map Dust")
# to_buy(
#     item_id="926",
#     sb_sell_price=sb_sell_price,
#     threshold=20,
#     quantity=3,
#     discord_price=(420)
# )

# Angel of Apprehension Trap Skin
# print("Angel of Apprehension Trap Skin")
# to_buy(
#     item_id="3529",
#     sb_sell_price=sb_sell_price,
#     threshold=400,
#     quantity=1,
#     discord_price=(2500)
# )
