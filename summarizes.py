from helper import sell_buy_price
from dis_cord import dis_cord_helper

import numpy as np

def summarizes():
    print("Get Discord Result")
    discord_status, discord_sell, discord_buy = dis_cord_helper()

    if discord_status == 200:
        sb_summary = ""
        buy_summary = ""
        sell_summary = ""
        buy_summary += f'''*Sell on Discord, For Quick Profit: Discord Buy Price More Then Quick Sell Price*
-------------------------------------
'''
        sell_summary += f'''*Buy on Discord, For Quick Profit: Quick Sell Price More Then Discord Buy Price*
-------------------------------------
'''

        # Get Disocrd ID
        item_id_sell = discord_sell['item_id'].unique()
        item_id_buy = discord_buy['item_id'].unique()
        item_id = np.append(item_id_sell, item_id_buy)
        item_id = np.unique(item_id)

        print("Get Marketplace result")
        sb, sell, buy = sell_buy_price(item_id)

        sb_string = sb.to_string(index=False)

        sb_summary += f'''*SB Market Summary*
        '''
        sb_summary += sb_string

        # Discord Buying
        discord_buy_group = discord_buy.groupby(['item_id'])
        for item_id, discord_buy_df in discord_buy_group:

            discord_buy_df.sort_values('price', ascending=False)
            rows_discord = sell[sell["item_id"] == item_id]

            # Check Profit
            if discord_buy_df["price"].iloc[0] > rows_discord["sell_sell"][0]:
                item_name = rows_discord["item_name"].iloc[0]
                name = ""
                discord_price = ""
                discord_quantity = ""
                for _, row in discord_buy_df.iterrows():
                    name = name + str(row["author"]) + " | "
                    discord_price = discord_price + str(row["price"]) + " | "
                    discord_quantity = discord_quantity + str(row["quantity"]) + " | "

                quick_price = ""
                quick_quantity = ""
                optimal_price = ""
                for _, row in rows_discord.iterrows(): 
                    quick_price = quick_price + str(row["buy_buy"]) + " | "
                    quick_quantity = quick_quantity + str(row["quantity"]) + " | "
                    optimal_price = optimal_price + str(row["sell_sell"]) + " | "

                buy_summary += f'''*Item Name:* {item_name}
    *Discord Name:* {name} 
    *Discord B Price:* {discord_price} 
    *Discord B Quantity:* {discord_quantity} 
    *Quick S Price:* {quick_price} 
    *Quick S Quantity:* {quick_quantity} 
    *Optimal S Price:* {optimal_price}

    '''

                # Discord Selling
                discord_sell_group = discord_sell.groupby(['item_id'])
                for item_id, discord_sell_df in discord_sell_group:

                    discord_sell_df.sort_values('price', ascending=False)
                    rows_discord = buy[buy["item_id"] == item_id]

                    # Check Profit
                    if discord_sell_df["price"].iloc[0] < rows_discord["sell_sell"][0]:
                        item_name = rows_discord["item_name"].iloc[0]
                        name = ""
                        discord_price = ""
                        discord_quantity = ""
                        for _, row in discord_sell_df.iterrows():
                            name = name + str(row["author"]) + " | "
                            discord_price = discord_price + str(row["price"]) + " | "
                            discord_quantity = discord_quantity + str(row["quantity"]) + " | "

                        quick_price = ""
                        quick_quantity = ""
                        optimal_price = ""
                        for _, row in rows_discord.iterrows(): 
                            quick_price = quick_price + str(row["buy_buy"]) + " | "
                            quick_quantity = quick_quantity + str(row["quantity"]) + " | "
                            optimal_price = optimal_price + str(row["sell_sell"]) + " | "

                        sell_summary += f'''*Item Name:* {item_name}
    *Discord Name:* {name} 
    *Discord B Price:* {discord_price} 
    *Discord B Quantity:* {discord_quantity} 
    *Quick S Price:* {quick_price} 
    *Quick S Quantity:* {quick_quantity} 
    *Optimal S Price:* {optimal_price}

    '''
                    
        return sb_summary, buy_summary, sell_summary
    else:
        return "Error, Check Code"
