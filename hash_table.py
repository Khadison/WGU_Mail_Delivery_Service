import csv
from datetime import datetime, time, timedelta

class HashTable:
    def __init__(self, size=40):
        # Initialize the hash table as a list of empty lists
        self.size = size
        # Create a list of empty lists (buckets)
        self.table = [[] for _ in range(self.size)]

    # Hash function to calculate index for a given key (package_id)
    def hash(self, key):
        return hash(key) % self.size
    
    # Insert a package into the hash table
    def insert(self, package_id, package_data):
        index = self.hash(package_id)
        package_info = (
            str(package_id),
            package_data[0],  # Address, city, state, and zipcode
            package_data[1] if len(package_data) > 1 else "",  # Deadline
            package_data[2] if len(package_data) > 2 else "",  # Weight
            package_data[3] if len(package_data) > 3 and package_data[3] != "" else "No special notes",  # special notes
            "At hub",  # Status
            None,      # Delivery_time, initially None
            None       # Departure_time, initially None
        )

        # Check if the package already exists in the bucket and update it if found
        for i, item in enumerate(self.table[index]):
            if item[0] == str(package_id):
                self.table[index][i] = package_info
                return
        self.table[index].append(package_info)

    # Load package data from a CSV file into the hash table
    def load_package_data(self, filename):
        with open(filename, 'r', newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                package_id = row[0]
                full_address = f"{row[1]}, {row[2]}, {row[3]} {row[4]}"  # Combine address, city, state, and zip
                deadline = row[5]
                weight = row[6]
                special_notes = row[7] if len(row) > 7 else ""
                package_data = [full_address, deadline, weight, special_notes]
                self.insert(package_id, package_data)
                
    # Print all packages stored in the hash table with headers for better readability        
    def print_all_packages(self):
        # Print header 
        print("\n{:<10} {:<40} {:<12} {:<12} {:<30} {:<12} {:<12} {:<12}".format(
            "Package ID", "Address", "Deadline", "Weight (kg)", "Special Notes", "Status", "Delivery Time", "Departure Time"))

        print("-" * 150)  # Separator line 

        # Iterate through all packages in the hash table
        for index, bucket in enumerate(self.table):
            if bucket:  
                for package in bucket:
                    delivery_time = package[6]
                    departure_time = package[7]
                    
                    # Format times as HH:MM:SS or keep them as None
                    formatted_delivery = delivery_time.strftime('%H:%M:%S') if isinstance(delivery_time, datetime) else str(delivery_time)
                    formatted_departure = departure_time.strftime('%H:%M:%S') if isinstance(departure_time, datetime) else str(departure_time)
                    
                    # Abbreviate long addresses and special notes
                    abbreviated_address = (package[1][:37] + '...') if len(package[1]) > 40 else package[1]
                    abbreviated_notes = (package[4][:27] + '...') if len(package[4]) > 30 else package[4]
                    
                    # Print each package's details in a formatted way
                    print("{:<10} {:<40} {:<12} {:<12} {:<30} {:<12} {:<12} {:<12}".format(
                        package[0], abbreviated_address, package[2], package[3], abbreviated_notes, package[5], formatted_delivery, formatted_departure))


    # Look up a specific package by its ID and return its details
    def lookup(self, package_id):
        index = self.hash(package_id)
        for package in self.table[index]:
            if str(package[0]) == str(package_id):
                return package
        return None
    
    # Update details of a specific package (status, delivery time, departure time, or address)
    def update_package_details(self, package_id, status=None, delivery_time=None, departure_time=None, new_address=None):
        index = self.hash(package_id)
        for i, package in enumerate(self.table[index]):
            if str(package[0]) == str(package_id):
                package_list = list(package)

                if status:
                    # Checks if status updates
                    #print(f"Updating status for Package {package_id} to {status}")
                    package_list[5] = status

                if delivery_time:
                    # Checks if delivery time updates
                    #print(f"Updating delivery time for Package {package_id} to {delivery_time}")
                    delivery_time = self._parse_time(delivery_time)
                    package_list[6] = delivery_time

                if departure_time:
                    # Checks if departure time updates
                    #print(f"Updating departure time for Package {package_id} to {departure_time}")
                    departure_time = self._parse_time(departure_time)
                    package_list[7] = departure_time

                # Special condition for package #9
                if package_id == '9' and new_address:
                    current_time = departure_time or package_list[7]
                    update_time = datetime.combine(datetime.min, time(10, 20))
                    
                    if isinstance(current_time, timedelta):
                        current_datetime = datetime.min + current_time
                    elif isinstance(current_time, datetime):
                        current_datetime = current_time
                    else:
                        print(f"Unexpected time format for Package 9: {current_time}")
                        return False

                    if current_datetime >= update_time:
                        package_list[1] = new_address
                        print(f"Updated address for Package 9 at {current_datetime.time()}")
                    else:
                        print(f"Address update for Package 9 is scheduled for 10:20 AM. Current time: {current_datetime.time()}")
                elif new_address:
                    # Checks if address updates
                    #print(f"Updating address for Package {package_id} to {new_address}")
                    package_list[1] = new_address

                self.table[index][i] = tuple(package_list)
                return True

        return False

    # Helper function to parse time strings into datetime objects
    def _parse_time(self, time_value):
        if isinstance(time_value, str):
            try:
                return datetime.strptime(time_value, '%H:%M:%S')
            except ValueError as e:
                print(f"Error parsing time: {e}")
                return None
        return time_value    
    
        
    # Check_time must be in the format of a datetime object to perform comparisons with departure_time and delivery_time    
    def check_package_status(self, package_id, check_time=None):
        package = self.lookup(package_id)
        
        if not package:
            return f"Package {package_id} not found"

        # Extract times and status from the package tuple
        departure_time = package[7]  
        delivery_time = package[6]   
        status = package[5]          
        
        # Use current time if no check time is provided
        if check_time is None:
            check_time = datetime.now()

        # Checks if times and status are updated
        #print(f"Package {package_id}, Check time={check_time}, Departure time={departure_time}, Delivery time={delivery_time}, Status={status}")

        if isinstance(departure_time, timedelta):
            departure_time = datetime.combine(check_time.date(), datetime.min.time()) + departure_time
        
        if isinstance(delivery_time, timedelta):
            delivery_time = datetime.combine(check_time.date(), datetime.min.time()) + delivery_time

        if departure_time is None:
            return f"Package {package_id} is at the hub as of {check_time.strftime('%I:%M %p')}"

        if delivery_time is None:
            if check_time >= departure_time:
                return f"Package {package_id} is en route as of {check_time.strftime('%I:%M %p')}"
            else:
                return f"Package {package_id} is at the hub as of {check_time.strftime('%I:%M %p')}"

        # Check if the package has been delivered
        if check_time >= delivery_time:
            return f"Package {package_id} was delivered at {delivery_time.strftime('%I:%M %p')}"

        # Check if the package is en route
        elif departure_time <= check_time < delivery_time:
            return f"Package {package_id} is en route as of {check_time.strftime('%I:%M %p')}"

        # If none of these conditions are met, it's still at the hub
        else:
            return f"Package {package_id} is at the hub as of {check_time.strftime('%I:%M %p')}"   
    
    # Check the status of all packages on a given truck at a specific time and update their details
    def check_all_truck_packages(self, truck, check_time):
        print(f"\n--- Checking status of all packages on truck {truck.id} at {check_time.strftime('%I:%M:%S %p')} ---")
        
        for package_id in truck.packages:
            package_id_str = str(package_id)
            
            # Call check_package_status to get the current status
            status = self.check_package_status(package_id_str, check_time)
            
            # Print the status of each individual package
            print(f"{status}")  
            
            # Lookup the package again to update its details if necessary
            package = self.lookup(package_id_str)
            
            if package:
                departure_time = package[7]  
                delivery_time = package[6]   
                
                # Convert departure_time and delivery_time to datetime if they are timedelta
                if isinstance(departure_time, timedelta):
                    departure_time = datetime.combine(check_time.date(), datetime.min.time()) + departure_time
                
                if isinstance(delivery_time, timedelta):
                    delivery_time = datetime.combine(check_time.date(), datetime.min.time()) + delivery_time

                # Update departure or delivery times based on current status
                if "en route" in status.lower() and departure_time is None:
                    self.update_package_details(package_id_str, departure_time=check_time.strftime('%H:%M:%S'))
                
                elif "delivered" in status.lower() and delivery_time is None:
                    self.update_package_details(package_id_str, delivery_time=check_time.strftime('%H:%M:%S'))

