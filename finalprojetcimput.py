import csv
from datetime import datetime

class InventoryItem:
    def __init__(self, item_id, manufacturer, item_type, price, service_date, damaged):
        self.item_id = item_id
        self.manufacturer = manufacturer
        self.item_type = item_type
        self.price = price
        self.service_date = service_date
        self.damaged = damaged

def read_csv_data():
    manufacturer_dict = {}
    price_dict = {}
    service_date_dict = {}

    with open('ManufacturerList.csv') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            item_id = row[0]
            manufacturer = row[1]
            item_type = row[2]
            damaged = row[3] if len(row) > 3 else ''
            manufacturer_dict[item_id] = {
                'manufacturer': manufacturer,
                'item_type': item_type,
                'damaged': damaged
            }

    with open('PriceList.csv') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            item_id = row[0]
            price = row[1]
            price_dict[item_id] = float(price) if price else 0.0

    with open('ServiceDatesList.csv') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            item_id = row[0]
            service_date = row[1]
            service_date_dict[item_id] = datetime.strptime(service_date, '%m/%d/%Y') if service_date else None

    return manufacturer_dict, price_dict, service_date_dict

def create_inventory_items(manufacturer_dict, price_dict, service_date_dict):
    items = {}
    for item_id, details in manufacturer_dict.items():
        price = price_dict.get(item_id, 0.0)
        service_date = service_date_dict.get(item_id, None)
        items[item_id] = InventoryItem(item_id, details['manufacturer'], details['item_type'], price, service_date, details['damaged'])
    return items

def write_csv(file_name, header, rows):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

def sort_by_manufacturer(item):
    return item.manufacturer

def sort_by_item_id(item):
    return item.item_id

def sort_by_service_date(item):
    return item.service_date if item.service_date else datetime.max

def sort_by_price(item):
    return item.price

def process_inventory():
    manufacturer_dict, price_dict, service_date_dict = read_csv_data()
    items = create_inventory_items(manufacturer_dict, price_dict, service_date_dict)

    # FullInventory.csv
    full_inventory = list(items.values())
    full_inventory.sort(key=sort_by_manufacturer)
    full_inventory_rows = [
        [item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime('%m/%d/%Y') if item.service_date else '', 'Damaged' if item.damaged else '']
        for item in full_inventory
    ]
    write_csv('FullInventory.csv', ['Item ID', 'Manufacturer', 'Item Type', 'Price', 'Service Date', 'Damaged'], full_inventory_rows)

    # LaptopInventory.csv
    laptop_inventory = [item for item in items.values() if item.item_type == 'laptop']
    laptop_inventory.sort(key=sort_by_item_id)
    laptop_inventory_rows = [
        [item.item_id, item.manufacturer, item.price, item.service_date.strftime('%m/%d/%Y') if item.service_date else '', 'Damaged' if item.damaged else '']
        for item in laptop_inventory
    ]
    write_csv('LaptopInventory.csv', ['Item ID', 'Manufacturer', 'Price', 'Service Date', 'Damaged'], laptop_inventory_rows)

    # PastServiceDateInventory.csv
    today = datetime.now()
    past_service_inventory = [item for item in items.values() if item.service_date and item.service_date < today]
    past_service_inventory.sort(key=sort_by_service_date)
    past_service_inventory_rows = [
        [item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime('%m/%d/%Y') if item.service_date else '', 'Damaged' if item.damaged else '']
        for item in past_service_inventory
    ]
    write_csv('PastServiceDateInventory.csv', ['Item ID', 'Manufacturer', 'Item Type', 'Price', 'Service Date', 'Damaged'], past_service_inventory_rows)

    # DamagedInventory.csv
    damaged_inventory = [item for item in items.values() if item.damaged]
    damaged_inventory.sort(key=sort_by_price, reverse=True)
    damaged_inventory_rows = [
        [item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime('%m/%d/%Y') if item.service_date else '']
        for item in damaged_inventory
    ]
    write_csv('DamagedInventory.csv', ['Item ID', 'Manufacturer', 'Item Type', 'Price', 'Service Date'], damaged_inventory_rows)

if __name__ == "__main__":
    process_inventory()
