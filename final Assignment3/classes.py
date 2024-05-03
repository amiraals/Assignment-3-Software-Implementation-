class Person:
    """Class to represent a Person"""
    def __init__(self, firstName, lastName, gender, phoneNumber):
        # Constructor for Person class
        self._firstName = firstName
        self._lastName = lastName
        self._gender = gender
        self._phoneNumber = phoneNumber

    def get_full_name(self):
        # Return the full name of the person
        return f"{self._firstName} {self._lastName}"

    def get_details(self):
        # Return details of the person
        return f"Name: {self.get_full_name()}, Gender: {self._gender}, Phone: {self._phoneNumber}"

class Employee(Person):
    """Class to represent an Employee"""
    def __init__(self, firstName, lastName, gender, phoneNumber, employeeID, department, jobTitle, salary):
        # Constructor for Employee class
        super().__init__(firstName, lastName, gender, phoneNumber)
        self.employeeID = employeeID
        self.department = department
        self.jobTitle = jobTitle
        self.salary = salary

    def get_details(self):
        # Return details of the employee
        details = super().get_details()
        details += f"\nEmployee ID: {self.employeeID}\nDepartment: {self.department}\nJob Title: {self.jobTitle}\nSalary: {self.salary}"
        return details


class Guest(Person):
    """""Class to represent a Guest"""
    def __init__(self, firstName, lastName, gender, phoneNumber, guestID):
        # Constructor for Guest class
        super().__init__(firstName, lastName, gender, phoneNumber)
        self.guestID = guestID

    def get_details(self):
        # Return details of the guest
        return super().get_details() + f", Guest ID: {self.guestID}"

class Client(Person):
    """Class representing a client"""
    def __init__(self, firstName, lastName, gender, phoneNumber, clientID, budget, numOf_events):
        # Constructor for Client class
        super().__init__(firstName, lastName, gender, phoneNumber)
        self.clientID = clientID
        self.budget = budget
        self.numOf_events = numOf_events

    def update_budget(self, new_budget):
        self.budget = new_budget

    def update_num_of_events(self, new_num_of_events):
        self.numOf_events = new_num_of_events

    def display_details(self):
        # Return details of the client
        return super().get_details() + f", Client ID: {self.clientID}, Budget: {self.budget}, Number of Events: {self.numOf_events}"



class Supplier:
    """Class to represent a supplier for an event."""
    def __init__(self, supplier_id, name, service_type):
        # Constructor for Supplier class
        self.supplier_id = supplier_id
        self.name = name
        self.service_type = service_type

    def __str__(self):
        return f"Supplier ID: {self.supplier_id}, Name: {self.name}, Service Type: {self.service_type}"


class Venue:
    """Class to represent a venue for an event"""
    def __init__(self, venue_id, address, min_guests, max_guests):
        # Constructor for Venue class
        self.venue_id = venue_id
        self.address = address
        self.min_guests = min_guests
        self.max_guests = max_guests

    def __str__(self):
        return f"Venue ID: {self.venue_id}, Address: {self.address}, Min Guests: {self.min_guests}, Max Guests: {self.max_guests}"


class Event:
    """Class to represent an event, which includes multiple suppliers and venues"""
    def __init__(self, event_id, event_type, date, time, duration):
        # Constructor for Event class
        self.event_id = event_id
        self.event_type = event_type
        self.date = date
        self.time = time
        self.duration = duration
        self.suppliers = []
        self.venues = []
        self.guests = []

    def add_supplier(self, supplier_id, name, service_type):
        # Add a supplier to the event
        new_supplier = Supplier(supplier_id, name, service_type)
        self.suppliers.append(new_supplier)
        return new_supplier

    def remove_supplier(self, supplier_id):
        # Remove a supplier from the event
        self.suppliers = [supplier for supplier in self.suppliers if supplier.supplier_id != supplier_id]

    def add_venue(self, venue):
        # Add a venue to the event
        if venue not in self.venues:
            self.venues.append(venue)

    def remove_venue(self, venue):
        # Remove a venue from the event
        self.venues = [v for v in self.venues if v.venue_id != venue.venue_id]

    def add_guest(self, guest):
        # Add a guest to the event
        self.guests.append(guest)

    def remove_guest(self, guestID):
        # Remove a guest from the event
        self.guests = [guest for guest in self.guests if guest.guestID != guestID]

    def get_details(self):
        # Return details of the event
        details = f"Event ID: {self.event_id}, Type: {self.event_type}, Date: {self.date}, Time: {self.time}, Duration: {self.duration}"
        guest_details = ', '.join([guest.get_details() for guest in self.guests])
        return f"{details}\nGuests: {guest_details}"




"""This file includes a set of classes for managing the event management system. 
The Person class serves as a base class for Employee, Guest, and Client classes, 
each representing a different entity with specific attributes and behaviors. 
The Event class has an aggregation relationship with the Guest and Venue classes. 
This means that an event can have multiple guests and venues associated with it, 
and these guests and venues can exist independently of the event. 
The Event class has a composition relationship with the Supplier class. 
This means that an event can have multiple suppliers, and their lifetime is tightly
 bound to the event. The Event class owns and manages the Supplier objects,
facilitating coordination and payment with suppliers.
"""