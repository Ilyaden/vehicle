import requests
from math import radians, cos, sin, sqrt, atan2

class Vehicle:
    def __init__(self, id, name, model, year, color, price, latitude, longitude):
        self.id = id
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>"

class VehicleManager:
    def __init__(self, url):
        self.url = url

    def get_vehicles(self):
        response = requests.get(f"{self.url}/vehicles")
        vehicles = []
        for vehicle_data in response.json():
        	vehicle = Vehicle(**vehicle_data)
        	vehicles.append(vehicle)
        return vehicles

    def filter_vehicles(self, params):
        vehicles = self.get_vehicles()
        for key, value in params.items():
            vehicles = [vehicle for vehicle in vehicles if getattr(vehicle, key) == value]
        return vehicles

    def get_vehicle(self, vehicle_id):
        response = requests.get(f"{self.url}/vehicles/{vehicle_id}")
        vehicle = Vehicle(**response.json())
        return vehicle

    def add_vehicle(self, vehicle):
    	response = requests.post(f"{self.url}/vehicles", json=vehicle.__dict__)
    	return response.json()

    def update_vehicle(self, vehicle):
        response = requests.put(f"{self.url}/vehicles/{vehicle.id}", json=vehicle.__dict__)
        return Vehicle(**response.json())

    def delete_vehicle(self, id):
        response = requests.delete(f"{self.url}/vehicles/{id}")
        return response.status_code 

    def get_distance(self, id1, id2):
        vehicle1 = self.get_vehicle(id1)
        vehicle2 = self.get_vehicle(id2)
        return self.calculate_distance(vehicle1.latitude, vehicle1.longitude, vehicle2.latitude, vehicle2.longitude)

    def get_nearest_vehicle(self, id):
        target_vehicle = self.get_vehicle(id)
        vehicles = self.get_vehicles()
        distances = [(self.calculate_distance(target_vehicle.latitude, target_vehicle.longitude, vehicle.latitude, vehicle.longitude), vehicle) for vehicle in vehicles if vehicle.id != id]
        return min(distances, key=lambda x: x[0])[1]

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371000 
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        return distance

