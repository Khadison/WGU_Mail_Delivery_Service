import csv
import math
import re

# Normalize address by removing city, state, and zip code, replacing abbreviations, and standardizing format
def normalize_address(address):
    # Remove city, state, and zip code by splitting on commas and taking only street part
    address = address.split(',')[0]
    
    # Replace common abbreviations and remove special characters
    address = (address.strip().replace(' ST', ' STREET').replace(' AVE', ' AVENUE'))
    
    # Remove extra spaces, punctuation, and standardize case
    return re.sub(r'[\W_]+', ' ', address).strip().lower()

# Load distance data from a CSV file and return a symmetric distance matrix
def load_distance_data(filename='CSV/distance.csv'):
    distances = []
    
    with open(filename, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            distance_row = []
            for d in row:
                if d.strip():  
                    try:
                        distance_row.append(float(d))
                    except ValueError:
                        print(f"Warning: Invalid distance value '{d}', treating as None.")
                        distance_row.append(None)
                else:
                    distance_row.append(None)
            distances.append(distance_row)
    
    # Fill in the lower triangle of the matrix (since it's symmetric)
    for i in range(len(distances)):
        for j in range(i):
            if distances[i][j] is None:
                distances[i][j] = distances[j][i]
    
    # Consistency check: fill None values where possible
    for i in range(len(distances)):
        for j in range(len(distances)):
            if distances[i][j] is None and distances[j][i] is not None:
                distances[i][j] = distances[j][i]  # Fill in the distance
    
    return distances

# Load address data from a CSV file and map addresses to indices for lookup purposes
def load_address_data(filename='CSV/address.csv'):
    global address_to_index
    address_to_index = {}
    
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        next(reader)  
        
        for row in reader:
            index = int(row[0])
            name = normalize_address(row[1])  # Normalize location name
            address = normalize_address(row[2])  # Normalize street address
            
            # Store both name and address in dictionary
            address_to_index[name] = index
            address_to_index[address] = index

# Get the index of a normalized address from the global dictionary          
def get_address_index(address):
    normalized_address = normalize_address(address)
    
    if normalized_address in address_to_index:
        return address_to_index[normalized_address]
    
    print(f"Warning: Address '{address}' normalized to '{normalized_address}' not found.")
    return None  

# Find the nearest neighbor package to deliver next based on current truck location and distance matrix
def nearest_neighbor(truck, packages, distances):
    undelivered = truck.packages.copy()
    route = []
    current_location = get_address_index("4001 South 700 East")  # Start at hub

    while undelivered:  # Loop until all packages are delivered
        nearest = None  # Variable to store nearest package ID
        min_distance = float('inf')

        for package_id in undelivered:
            package = packages.lookup(str(package_id))
            if package:
                address_index = get_address_index(package[1])
                if address_index is not None:
                    distance = distances[current_location][address_index]
                    # Checks if the distance from current location to delivery address is working
                    #print(f"Debug: Distance from {current_location} to {address_index} ({package[1]}): {distance}")
                    
                    if distance is None or distance == math.inf:
                        continue
                    
                    if distance < min_distance:
                        min_distance = distance
                        nearest = package_id
        
        if nearest is None:
            print(f"Warning: No valid package found. Remaining packages: {undelivered}")
            break

        route.append(nearest)  # Add nearest package to delivery route
        package = packages.lookup(str(nearest))
        current_location = get_address_index(package[1])  # Update current location to new delivery destination
        if current_location is None:
            print(f"Error: Invalid current location for package {nearest}: {package[1]}")
            break
        undelivered.remove(nearest)

    return route

# Simulate delivering packages for each truck based on their routes and update their statuses/times accordingly.
def deliver_packages(trucks, route, packages, distances):
    # Sort trucks based on departure time
    sorted_trucks = sorted(trucks, key=lambda truck: truck.depart_time)
    
    for i in range(0, len(sorted_trucks), 2):
        selected_trucks = sorted_trucks[i:i+2]  # Process trucks in pairs (two at a time)

        for truck in selected_trucks:
            if len(truck.packages) == 0: # Skip trucks with no packages
                continue

            for package_id in route:
                if package_id not in truck.packages:
                    continue
                
                package = packages.lookup(str(package_id))
                
                if package:
                    from_index = get_address_index(truck.current_location)
                    to_index = get_address_index(package[1])  
                    
                    if from_index is not None and to_index is not None:
                        # Update package to "En route" with departure time
                        packages.update_package_details(
                            str(package_id), 
                            status="En route", 
                            departure_time=truck.time  # Set departure time when the truck begins delivery
                        )
                        # Debug statement does same thing on update_package_details
                        #print(f"Updating package {package_id} status to en route at {truck.time}")  

                        # Calculate distance and simulate delivery
                        distance = distances[from_index][to_index]
                        delivery_time = truck.deliver(package_id, distance, package[1])

                        # Update package to "Delivered" with delivery time
                        if delivery_time:
                            packages.update_package_details(
                                str(package_id), 
                                status="Delivered", 
                                delivery_time=delivery_time
                            )
                            # Debug statement does same thing on update_package_details
                            #print(f"Package {package_id} delivered at {delivery_time}")
                    else:
                        print(f"Warning: Unable to calculate distance for Package {package_id}")
                else:
                    print(f"Warning: Package {package_id} not found")
            
            # Return truck to hub after deliveries
            hub_index = get_address_index("4001 South 700 East")
            if hub_index is not None and get_address_index(truck.current_location) is not None:
                return_distance = distances[get_address_index(truck.current_location)][hub_index]
                truck.return_to_hub(return_distance)
            else:
                print("Warning: Unable to calculate return distance to hub")

# Calculate and print total mileage traveled by all trucks after deliveries are completed.              
def calculate_and_print_total_mileage(trucks):
    total_mileage = sum(truck.mileage for truck in trucks)
    print(f"Total mileage for all trucks: {total_mileage:.2f} miles")

