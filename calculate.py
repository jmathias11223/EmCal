# Class for performing all necessary calculations with raw data

# Calculates C02 emissions in g/mile
def calculate_c02_emissions(mileage):
    return (8.8 / mileage) * 1000      # 8.8 kg/gallon * 1/mileage gallons/mile = kg/mile

# Arg0 = int; Arg1 = dictionary; Arg2 = distance traveled(int)
def calculate_cost(mileage, perGallonPrice, distance):
    gallonsUsed = float(distance) / mileage
    priceRange = "$%.2f to $%.2f" % (gallonsUsed * perGallonPrice["Lowest"], gallonsUsed * perGallonPrice["Average"])
    return priceRange

print(calculate_cost(37, {"Lowest":2.70, "Average":3.00}, 570))

