import requests
import pandas as pd
import json

# Get Item ID name 
def item_name(id):
    with open("./item_id.json", "r") as json_file:
        data = json.load(json_file)
    return data[id]

# API for mousehunt marketplace
def market_price(item_id, action):
    file_path = 'cookie.txt'  # Change this to your file's path
    with open(file_path, 'r') as file:
        # Read the entire content of the file
        file_content = file.read()

    payload = {
        "action": action,
        "item_id": item_id
    }

    return requests.post(
        url='https://www.mousehuntgame.com/managers/ajax/users/marketplace.php',
        # Might be better to replace this with an alt account session
        headers={
            "cookie": file_content
        },
        data= payload
    )

# Get Total Listed Quantity
def get_item_summary(item_id):
    result = market_price(item_id, action="get_item_details").json()

    yesterday_vol = result["marketplace_item_history_summary"]["yesterday"]
    current_sell_vol = result["marketplace_item_sum_listings"][item_id]['sell']["quantity"]
    return current_sell_vol, yesterday_vol

def sell_buy_price(items):
    # Super Brie 
    sb_id = "114"
    sb_market = market_price(sb_id, action="get_item_listings")
    sb_sell_price = sb_market.json()["marketplace_item_listings"][sb_id]['sell'][0]["unit_price"]
    sb_buy_price = sb_market.json()["marketplace_item_listings"][sb_id]['buy'][0]["unit_price"]

    temp=dict()
    for item_id in items:
        market = market_price(item_id, action="get_item_listings")
        price_list = market.json()["marketplace_item_listings"][item_id]
        temp[item_id] = price_list

    #Sell on Discord (B>), Buy on Marketplace")
    #Make sure discord price is more then here")
    headers_sell=[
        'Item ID', 
        'Listing No',
        'SB After Tax (Buy/Buy Price) -', 
        'SB After Tax (Sell/Buy Price)', 
        "SB After Tax (Buy/Sell Price)", 
        "SB After Tax (Sell/Sell Price)",
        "Quantity"] 
    dataset_sell = pd.DataFrame(columns=headers_sell)
    for item_id in temp:
        if len(temp[item_id]['sell']) != 0:
            item_temp = []
            for i in range(len(temp[item_id]['sell'])):
                item_temp.append([
                    # Based on aga-ation here
                    item_name(item_id), 
                    (i+1),
                    str(round((temp[item_id]['sell'][i]["unit_price"] / sb_buy_price)  * 11/10,3)),
                    str(round((temp[item_id]['sell'][i]["unit_price"] / sb_sell_price)  * 11/10,3)),
                    str(round((temp[item_id]['buy'][i]["unit_price"] / sb_buy_price)  * 11/10,3)),
                    str(round((temp[item_id]['buy'][i]["unit_price"] / sb_sell_price)  * 11/10,3)),
                    temp[item_id]['sell'][i]["quantity"]
                ]) 
            df_row = pd.DataFrame(item_temp, columns=headers_sell)
            dataset_sell = dataset_sell.append(df_row)

    # Buy on Discord (S>), Sell on Marketplace
    # Make sure discord price is less then here
    headers_buy = [
        'Item ID', 
        'Listing No',
        'SB (Sell Price) -> Buy', 
        "SB (Buy Price) -> Buy", 
        'SB (Sell Price) -> Sell', 
        "SB (Buy Price) -> Sell",
        "Quantity"]
    dataset_buy = pd.DataFrame(columns=headers_buy)
    for item_id in temp:
        # Check if there's any listing
        if len(temp[item_id]['sell']) != 0:
            item_temp = []
            for i in range(len(temp[item_id]['buy'])):
                item_temp.append([
                    item_name(item_id), 
                    (i+1),
                    str(round(temp[item_id]['buy'][i]["unit_price"] * (9/10) / sb_sell_price,3)),
                    str(round(temp[item_id]['buy'][i]["unit_price"] * (9/10) / sb_buy_price,3)),
                    str(round(temp[item_id]['sell'][i]["unit_price"] * (9/10) / sb_sell_price,3)),
                    str(round(temp[item_id]['sell'][i]["unit_price"] * (9/10) / sb_buy_price,3)),
                    temp[item_id]['sell'][i]["quantity"]
                ])
        df_row = pd.DataFrame(item_temp, columns=headers_buy)
        dataset_buy = dataset_buy.append(df_row)
    return dataset_sell, dataset_buy