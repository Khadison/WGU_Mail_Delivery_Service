# Student ID: 01148973
import csv
from datetime import datetime, timedelta
from hash_table import HashTable
from truck import Truck
from delivery_logic import calculate_and_print_total_mileage, load_address_data, load_distance_data, nearest_neighbor, deliver_packages

def load_package_data(filename, hash_table):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        
        for row in reader:
            # Get the package ID from the first column
            package_id = row[0]
            # Insert the package into the hash table
            hash_table.insert(package_id)

def main():
    
    # Load package data
    package_hash = HashTable()
    package_hash.load_package_data('CSV/package.csv')
    
    # Load address data first
    load_address_data('CSV/address.csv')
    
    # Load distance data
    distances = load_distance_data('CSV/distance.csv')
    

   
    # Create truck objects
    truck1 = Truck(1, 16, 18, 0, "4001 South 700 East", ['14', '15', '19', '16', '13', '20', '40', '5', '8', '10', '11', '12', '37', '21', '24', '1'], timedelta(hours = 8))
    truck2 = Truck(2, 16, 18, 0, "4001 South 700 East", ['3', '6', '18', '36', '38', '2', '22', '23', '26', '29', '30', '31', '33', '34', '17', '25'], timedelta(hours = 9, minutes = 5))
    truck3 = Truck(3, 16, 18, 0, "4001 South 700 East", ['9', '28', '32', '35', '39', '4', '7', '27'], timedelta(hours = 10, minutes = 50))
    
    
    trucks = [truck1, truck2, truck3]
    
    # Run delivery simulation for each truck
    for truck in trucks:
            route = nearest_neighbor(truck, package_hash, distances)
            deliver_packages(trucks, route, package_hash, distances)
            
    # Update address for package delivery
    package_hash.update_package_details('9',  new_address="410 S. State St., Salt Lake City, UT 84111")
    
    # User Interface
    print("\nWelcome to Western Governors University Parcel Service (WGUPS)")

    while True:
        print("\nPlease choose an option:")
        print("1. Check the status of an individual package.")
        print("2. Check the status of all packages on each truck.")
        print("3. View delivery route details and total mileage.")
        print("4. View detailed information about a specific package.")
        print("5. Print details of all packages.")
        print("6. Exit the program.")

        user_choice = input("\nEnter your choice (1/2/3/4/5/6): ").strip()

        if user_choice == "1":
            try:
                # Ask for a specific package ID
                solo_input = input("\nEnter the numeric package ID (e.g., 9): ").strip()
                package_id = str(solo_input)
                
                # Ask for a specific time to check the status
                user_time = input("Enter the time to check status (HH:MM:SS): ").strip()
                (h, m, s) = user_time.split(":")
                check_time = datetime.strptime(f"{h}:{m}:{s}", '%H:%M:%S')

                # Check and print status of that specific package
                status = package_hash.check_package_status(package_id, check_time)
                print(f"\n{status}")
            except ValueError:
                print("\nInvalid entry. Please try again.")

        elif user_choice == "2":
            try:
                # Ask for a specific time to check the status of all packages on each truck
                user_time = input("Enter the time to check status (HH:MM:SS): ").strip()
                (h, m, s) = user_time.split(":")
                check_time = datetime.strptime(f"{h}:{m}:{s}", '%H:%M:%S')

                # Loop through each truck and display the status of its packages at the specified time
                for truck in trucks:
                    package_hash.check_all_truck_packages(truck, check_time)

            except ValueError:
                print("\nInvalid time format or error occurred. Please try again.")

        elif user_choice == "3":
            # View delivery route details for each truck and display total mileage
            print("\n--- Delivery Route Details ---")
            total_mileage = sum(truck.mileage for truck in trucks)
            
            for truck in trucks:
                print(f"Truck {trucks.index(truck) + 1}")
                route = nearest_neighbor(truck, package_hash, distances)
                
                # Print truck delivery route and mileage after deliveries
                print(f"Route: {route}")
                print(f"Truck mileage after deliveries: {truck.mileage:.2f}")
                
                # Print the time after finishing all deliveries for this truck
                print(f"Time after finishing truck {trucks.index(truck) + 1} delivery: {truck.time}\n")

            # Print total mileage after displaying all routes
            print(f"Total mileage traveled by all trucks: {total_mileage:.2f} miles")

        elif user_choice == "4":
            try:
                # Input package ID that you want details on
                solo_input = input("\nEnter the numeric package ID (e.g., 9): ").strip()
                package_id = str(solo_input)
                
                # Lookup and display detailed information about the package
                package = package_hash.lookup(package_id)
                
                if package:
                    print("\n--- Package Details ---")
                    print(f"Package ID: {package[0]}")
                    print(f"Delivery Address: {package[1]}")
                    print(f"Delivery Deadline: {package[2]}")
                    print(f"Package Weight: {package[3]} kg")
                    print(f"Special Notes: {package[4] if package[4] else 'No special notes'}")
                    print(f"Delivery Status: {package[5]}")
                    print(f"Delivery Time: {package[6]}")
                    print(f"Departure Time: {package[7]}")
                else:
                    print(f"\nPackage {package_id}: Not found")
            except ValueError:
                print("\nInvalid entry. Please try again.")

        elif user_choice == "5":
            # Call the method to print details of all packages
            package_hash.print_all_packages()

        elif user_choice == "6":
            print("\nThank you for using WGUPS. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a valid option (1/2/3/4/5/6).")
        
    # Test different times for checking status (including date)
    test_times = [
        datetime.strptime('2024-11-08 09:00:00', '%Y-%m-%d %H:%M:%S'),  # Before first delivery
        datetime.strptime('2024-11-08 10:00:00', '%Y-%m-%d %H:%M:%S'),  # Just before a known delivery
        datetime.strptime('2024-11-08 12:30:00', '%Y-%m-%d %H:%M:%S'),  # Just after a known delivery
    ]
    
    # For section D screenshot of showing status of packages in each truck at a given time
    for test_time in test_times:
        for truck in trucks:
            package_hash.check_all_truck_packages(truck, test_time)
     
if __name__ == "__main__":
    main()
    