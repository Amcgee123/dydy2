# StockCheck: the stock report for the college shop.
# It prints every item, with LOW beside anything at the warning level or below.

SHOP_NAME = "Campus Shop"
LOW_STOCK = 10

stock = {
    "Milk": 10,
    "Bread": 4,
    "Crisps": 22,
    "Apples": 5,
}

print(f"{SHOP_NAME}: stock report")
for item, count in stock.items():
    if count <= LOW_STOCK:
        print(f"{item}: {count} left  LOW")
    else:
        print(f"{item}: {count} left")
