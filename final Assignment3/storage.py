from tkinter import messagebox
import pickle
import os

# Defining the path where data files will be stored
data_path = "data"
if not os.path.exists(data_path):
    os.makedirs(data_path)



# Functions to save and load employee data
def save_data(employees):
    try:
        with open(os.path.join(data_path, 'employees.pkl'), 'wb') as dumpf:
            pickle.dump(employees, dumpf)
    except Exception as e:
        print("An error occurred while saving the data:", e)

def load_data():
    try:
        with open(os.path.join(data_path, 'employees.pkl'), 'rb') as loadf:
            return pickle.load(loadf)
    except FileNotFoundError:
        print("Employee data file not found. Starting with an empty dataset.")
        return {}
    except Exception as e:
        print("An error occurred while loading the data:", e)
        return {}


# Functions to save and load event data
def save_event_data(events):
    try:
        with open(os.path.join(data_path, 'events.pkl'), 'wb') as dumpf:
            pickle.dump(events, dumpf)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving event data: {e}")

def load_event_data():
    try:
        with open(os.path.join(data_path, 'events.pkl'), 'rb') as loadf:
            return pickle.load(loadf)
    except FileNotFoundError:
        messagebox.showinfo("Information", "Event data file not found. Starting with an empty event dataset.")
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading event data: {e}")
        return {}


# Functions to save and load supplier data
def save_supplier_data(suppliers):
    try:
        with open(os.path.join(data_path, 'suppliers.pkl'), 'wb') as dumpf:
            pickle.dump(suppliers, dumpf)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving supplier data: {e}")

def load_supplier_data():
    try:
        with open(os.path.join(data_path, 'suppliers.pkl'), 'rb') as loadf:
            return pickle.load(loadf)
    except FileNotFoundError:
        messagebox.showinfo("Information", "Supplier data file not found. Starting with an empty supplier dataset.")
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading supplier data: {e}")
        return {}


# Functions to save and load guest data
def save_guest_data(guests):
    try:
        with open(os.path.join(data_path, 'guests.pkl'), 'wb') as dumpf:
            pickle.dump(guests, dumpf)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving guest data: {e}")

def load_guest_data():
    try:
        with open(os.path.join(data_path, 'guests.pkl'), 'rb') as loadf:
            return pickle.load(loadf)
    except FileNotFoundError:
        messagebox.showinfo("Information", "Guest data file not found. Starting with an empty guest dataset.")
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading guest data: {e}")
        return {}


# Functions to save and load client data
def save_client_data(clients):
    try:
        with open(os.path.join(data_path, 'clients.pkl'), 'wb') as dumpf:
            pickle.dump(clients, dumpf)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving client data: {e}")

def load_client_data():
    try:
        with open(os.path.join(data_path, 'clients.pkl'), 'rb') as loadf:
            return pickle.load(loadf)
    except FileNotFoundError:
        messagebox.showinfo("Information", "Client data file not found. Starting with an empty client dataset.")
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading client data: {e}")
        return {}


# Functions to save and load venue data
def save_venue_data(venues):
    try:
        with open(os.path.join(data_path, 'venues.pkl'), 'wb') as dumpf:
            pickle.dump(venues, dumpf)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving venue data: {e}")

def load_venue_data():
    try:
        with open(os.path.join(data_path, 'venues.pkl'), 'rb') as loadf:
            return pickle.load(loadf)
    except FileNotFoundError:
        messagebox.showinfo("Information", "Venue data file not found. Starting with an empty venue dataset.")
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading venue data: {e}")
        return {}
