from helper import sell_buy_price

items = {
    "2174": "Gilded Charm",
    "2631": "Ember Charm"
}

sell, buy = sell_buy_price(items)

print("------------------------------------------------------------------------")

print("Sell on Discord (B>), Buy on Marketplace")
print("Make sure discord price is more then here")
print(sell)

print()

print("------------------------------------------------------------------------")

print("Buy on Discord (S>), Sell on Marketplace")
print("Make sure discord price is less then here")
print(buy)