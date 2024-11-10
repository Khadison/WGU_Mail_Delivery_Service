from datetime import timedelta

#Create truck class
class Truck:
    def __init__(self, id, capacity, speed, mileage, current_location, packages, depart_time):
        self.id = id
        self.capacity = capacity
        self.speed = speed  # Speed in miles per hour (mph)
        self.mileage = mileage
        self.current_location = current_location 
        self.packages = packages # List of packages on the truck
        self.depart_time = depart_time # Time when truck leaves the hub
        self.time = depart_time # Current time, intially set to departure time
    
    # Simulate delivering package by updating mileage and time based on distance traveled
    def deliver(self, package_id, distance, destination):
        # Check if the package is on the truck
        if package_id in self.packages:
            self.mileage += distance
            time_taken = timedelta(hours=distance / self.speed)
            self.time += time_taken
            self.current_location = destination
            return self.time
        else:
            print(f"Warning: Package {package_id} not found on Truck {self.id}.")
            return None


    # Simulate returning to hub by updating mileage and time based on distance traveled
    def return_to_hub(self, distance):
        self.mileage += distance
        self.time += timedelta(hours=distance / self.speed)
        self.current_location = "4001 South 700 East"   # Hub address
        return self.time
     
    
    # Provide a string representation of the truck's current state
    def __str__(self):
        return f"Truck {self.id}: Capacity={self.capacity}, Speed={self.speed}, Packages={len(self.packages)}, Location={self.current_location}, Time={self.time.strftime('%I:%M %p')}"

    