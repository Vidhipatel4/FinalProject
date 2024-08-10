from datetime import datetime
import csv
import os

# Define the Item class
class Item:
    def __init__(self, item_id, manufacturer, item_type, price, service_date, damaged=False):
        self.item_id = item_id
        self.manufacturer = manufacturer
        self.item_type = item_type
        self.price = price
        self.service_date = service_date
        self.damaged = damaged

    def __repr__(self):
        return f"Item({self.item_id}, {self.manufacturer}, {self.item_type}, {self.price}, {self.service_date}, {self.damaged})"

# Load data from ManufacturerList.csv
def load_manufacturer_list(filename):
    inventory = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            item_id = row[0]
            manufacturer = row[1]
            item_type = row[2]
            damaged = len(row) > 3 and row[3].lower() == 'damaged'
            inventory[item_id] = Item(item_id, manufacturer, item_type, None, None, damaged)
    return inventory

# Load data from PriceList.csv
def load_price_list(filename, inventory):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            item_id = row[0]
            try:
                price = float(row[1])  # Changed to float to accommodate decimal prices
                if item_id in inventory:
                    inventory[item_id].price = price
            except ValueError:
                print(f"Warning: Could not convert price '{row[1]}' for item ID '{item_id}'.")

# Load data from ServiceDatesList.csv
def load_service_dates_list(filename, inventory):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            item_id = row[0]
            try:
                service_date = datetime.strptime(row[1], "%m/%d/%Y")
                if item_id in inventory:
                    inventory[item_id].service_date = service_date
            except ValueError:
                print(f"Warning: Could not parse service date '{row[1]}' for item ID '{item_id}'.")

# Generate FullInventory.csv
def generate_full_inventory_csv(inventory, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Item ID", "Manufacturer", "Item Type", "Price", "Service Date", "Damaged"])
        sorted_items = sorted(inventory.values(), key=lambda x: x.manufacturer)
        for item in sorted_items:
            writer.writerow([item.item_id, item.manufacturer, item.item_type, item.price,
                             item.service_date.strftime("%m/%d/%Y") if item.service_date else "",
                             "damaged" if item.damaged else ""])

# Generate LaptopInventory.csv
def generate_laptop_inventory_csv(inventory, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Item ID", "Manufacturer", "Price", "Service Date", "Damaged"])
        laptop_items = [item for item in inventory.values() if item.item_type.lower() == 'laptop']
        sorted_items = sorted(laptop_items, key=lambda x: x.item_id)
        for item in sorted_items:
            writer.writerow([item.item_id, item.manufacturer, item.price,
                             item.service_date.strftime("%m/%d/%Y") if item.service_date else "",
                             "damaged" if item.damaged else ""])

# Generate PastServiceDateInventory.csv
def generate_past_service_date_inventory_csv(inventory, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Item ID", "Manufacturer", "Item Type", "Price", "Service Date", "Damaged"])
        today = datetime.today()
        past_service_items = [item for item in inventory.values() if item.service_date and item.service_date < today]
        sorted_items = sorted(past_service_items, key=lambda x: x.service_date)
        for item in sorted_items:
            writer.writerow([item.item_id, item.manufacturer, item.item_type, item.price,
                             item.service_date.strftime("%m/%d/%Y") if item.service_date else "",
                             "damaged" if item.damaged else ""])

# Generate DamagedInventory.csv
def generate_damaged_inventory_csv(inventory, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Item ID", "Manufacturer", "Item Type", "Price", "Service Date"])
        damaged_items = [item for item in inventory.values() if item.damaged]
        sorted_items = sorted(damaged_items, key=lambda x: x.price if x.price is not None else 0, reverse=True)
        for item in sorted_items:
            writer.writerow([item.item_id, item.manufacturer, item.item_type, item.price,
                             item.service_date.strftime("%m/%d/%Y") if item.service_date else ""])

# Main function to load data and generate the required CSV files
import os

def main():
    # Load data
    inventory = load_manufacturer_list('ManufacturerList.csv')
    load_price_list('PriceList.csv', inventory)
    load_service_dates_list('ServiceDatesList.csv', inventory)

    # Define the output directory
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Define file paths
    full_inventory_path = os.path.join(output_dir, 'FullInventory.csv')
    laptop_inventory_path = os.path.join(output_dir, 'LaptopInventory.csv')
    past_service_date_inventory_path = os.path.join(output_dir, 'PastServiceDateInventory.csv')
    damaged_inventory_path = os.path.join(output_dir, 'DamagedInventory.csv')

    # Generate and save files
    print("Generating FullInventory.csv...")
    generate_full_inventory_csv(inventory, full_inventory_path)
    
    print("Generating LaptopInventory.csv...")
    generate_laptop_inventory_csv(inventory, laptop_inventory_path)
    
    print("Generating PastServiceDateInventory.csv...")
    generate_past_service_date_inventory_csv(inventory, past_service_date_inventory_path)
    
    print("Generating DamagedInventory.csv...")
    generate_damaged_inventory_csv(inventory, damaged_inventory_path)
    
    print("All files generated successfully.")

if __name__ == "__main__":
    main()
