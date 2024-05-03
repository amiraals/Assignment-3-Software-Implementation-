import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from storage import (
    load_data, save_data, load_client_data, save_client_data,
    load_event_data, save_event_data, load_supplier_data, save_supplier_data,
    load_guest_data, save_guest_data, load_venue_data, save_venue_data
)
from classes import Employee, Client, Event, Supplier, Guest, Venue


class ManagementApp:
    """Class to represent the main application for managing employees, events, suppliers, guests, and clients."""
    def __init__(self, root):
        # Constructor
        self.root = root  # Storing the root window object
        self.root.title("The Best Events Company Management System")  # Setting the title of the main window
        # Loading existing data from pickle files for different categories
        self.employees = load_data()
        self.events = load_event_data()
        self.suppliers = load_supplier_data()
        self.guests = load_guest_data()
        self.clients = load_client_data()
        self.venues = load_venue_data()

        # Creating a label widget and placing it at the top of the window
        ttk.Label(root, text="Welcome to the Management System").grid(row=0, column=0, columnspan=2)
        # Creating another label widget that prompts the user to select a system to enter
        ttk.Label(root, text="Please select the system you want to enter:").grid(row=1, column=0, sticky='w')
        self.system_var = tk.StringVar()
        # Defining the options that will appear in the drop-down menu
        system_options = ['Employee', 'Event', 'Supplier', 'Client', 'Guest', 'Venue']  # Added 'Venue'
        # Creating an OptionMenu widget
        self.system_menu = tk.OptionMenu(root, self.system_var, *system_options)
        # Placing the OptionMenu in the GUI
        self.system_menu.grid(row=1, column=1)
        # Creating a button to confirm user selection
        ttk.Button(root, text="Enter", command=self.enter_system).grid(row=2, column=0, columnspan=2)


        # Initializing ID counters
        self.employee_id_counter = self.initialize_id_counter(self.employees, "employeeID", 2)
        self.supplier_id_counter = self.initialize_id_counter(self.suppliers, "supplier_id", 2)
        self.event_id_counter = self.initialize_id_counter(self.events, "event_id", 2)
        self.guest_id_counter = self.initialize_id_counter(self.guests, "guestID", 1)
        self.client_id_counter = self.initialize_id_counter(self.clients, "clientID", 1)
        self.venue_id_counter = self.initialize_id_counter(self.venues, "venue_id", 1)


    def initialize_id_counter(self, items, id_attr, slice_start):
        if items:
            return max(int(getattr(item, id_attr)[slice_start:]) for item in items.values()) + 1
        return 1

    # A function to navigate to the selected system interface based on user input from the OptionMenu
    def enter_system(self):
        # This method retrieves the user's selection and opens the corresponding system management interface.

        # Retrieving the value selected in the OptionMenu by the user
        selected_system = self.system_var.get()
        if selected_system == 'Employee':
            self.open_employee_system()
        elif selected_system == "Event":
            self.open_event_system()
        elif selected_system == "Supplier":
            self.open_supplier_system()
        elif selected_system == "Guest":
            self.open_guest_system()
        elif selected_system == "Client":
            self.open_client_system()
        elif selected_system == "Venue":
            self.open_venue_system()


    def open_employee_system(self):
        # Opening the Employee management system interface if the user selects 'Employee' from the main menu setting up the GUI elements for employee management

        # Reloading the employee data from the storage file to ensure the data is up to date
        self.employees = load_data()

        # Creating a Treeview widget for displaying the list of employees in a tabular format
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Department", "Job Title", "Salary"),
                                 show="headings")
        # Defining the headings for each column in the Treeview
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Job Title", text="Job Title")
        self.tree.heading("Salary", text="Salary")
        self.tree.grid(row=3, column=0, columnspan=2, sticky='nsew')

        # Creating and placing a button to add new employee
        ttk.Button(self.root, text="Add Employee", command=self.open_add_employee_form).grid(row=4, column=0)
        # Creating and placing a button to modify existing employee details
        ttk.Button(self.root, text="Modify Employee", command=self.modify_employee).grid(row=4, column=1)
        # Creating and placing a button to remove  employee record
        ttk.Button(self.root, text="Remove Employee", command=self.remove_employee).grid(row=5, column=0)
        # Creating and placing a button to find an employee by their ID
        ttk.Button(self.root, text="Find by ID", command=self.find_employee).grid(row=5, column=1)

        # Refreshing the table to display the current data in the Treeview
        self.refresh_table()


    # A function to refreshes the data displayed in the Treeview widget by first clearing all existing entries and then repopulating it with updated data from the employees dictionary
    def refresh_table(self):
        # Clearing all existing entries in the Treeview.
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Looping through the employees dictionary and inserting each employee's data into the Treeview
        for emp_id, emp in self.employees.items():
            employee_id = getattr(emp, 'employeeID', 'No ID')
            name = emp.get_full_name()
            department = getattr(emp, 'department', 'No Department')
            job_title = getattr(emp, 'jobTitle', 'No Job Title')
            salary = getattr(emp, 'salary', 'No Salary')

            # Inserting the employee's data into the Treeview
            self.tree.insert("", "end", values=(employee_id, name, department, job_title, salary))


    # A function to open a new window to add a new employee
    def open_add_employee_form(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Add New Employee")

        # Defining labels for the input fields and initial dropdown selections
        labels = ['First Name:', 'Last Name:', 'Phone Number:', 'Gender:', 'Department:', 'Job Title:', 'Salary:']
        self.entries = {}
        departments = ["Marketing", "Operations", "Human Resources", "Finance", "Logistics", "Sales", "Event Planning"]
        job_titles = ["Event Coordinator", "Event Manager", "Marketing Specialist", "Operations Manager", "HR Manager",
                      "Registration Coordinator"]

        # Creating label and appropriate entry or dropdown for each field
        for i, label in enumerate(labels):
            ttk.Label(self.add_window, text=label).grid(row=i, column=0)
            if label == 'Gender:':
                gender_var = tk.StringVar()
                gender_menu = ttk.OptionMenu(self.add_window, gender_var, "Select Gender", "Male", "Female")
                gender_menu.grid(row=i, column=1)
                self.entries[label] = gender_var
            elif label == 'Department:':
                department_var = tk.StringVar()
                department_menu = ttk.OptionMenu(self.add_window, department_var, *departments)
                department_menu.grid(row=i, column=1)
                self.entries[label] = department_var
            elif label == 'Job Title:':
                job_title_var = tk.StringVar()
                job_title_menu = ttk.OptionMenu(self.add_window, job_title_var, *job_titles)
                job_title_menu.grid(row=i, column=1)
                self.entries[label] = job_title_var
            else:
                entry = ttk.Entry(self.add_window)
                entry.grid(row=i, column=1)
                self.entries[label] = entry

        # A button to save the new employee data
        ttk.Button(self.add_window, text="Save Employee", command=self.add_employee).grid(row=len(labels), column=1)


    # A function that collects the data from the form, validates it, creates a new Employee object, saves the data,and refreshes the employee list
    def add_employee(self):
        try:
            # Attempting to retrieve data from entries with validation
            first_name = self.entries['First Name:'].get()
            last_name = self.entries['Last Name:'].get()
            phone_number = self.entries['Phone Number:'].get()
            gender = self.entries['Gender:'].get()
            department = self.entries['Department:'].get()
            job_title = self.entries['Job Title:'].get()
            salary = self.entries['Salary:'].get()

            # Checking for empty fields
            if not (first_name and last_name and gender and phone_number and department and job_title and salary):
                tk.messagebox.showerror("Input Error", "All fields must be filled out.")
                return

            # Validating salary as a float
            salary = float(salary)

            # Assigning a unique employee ID and incrementing the counter
            employee_id = f"EP{self.employee_id_counter}"
            self.employee_id_counter += 1

            # Creating a new Employee object
            emp = Employee(first_name, last_name, gender, phone_number, employee_id, department, job_title, salary)
            self.employees[emp.employeeID] = emp
            save_data(self.employees)

            # Refreshing the employee table and closing the form
            self.refresh_table()
            self.add_window.destroy()

        except ValueError:
            # Handling the error specifically if salary is not a valid numeric value
            tk.messagebox.showerror("Input Error", "Invalid salary input. Salary must be a numeric value.")


    # A function that allows modification for an existing employee's details
    def modify_employee(self):
        # Asking user to enter the ID of the employee they wish to modify
        emp_id = simpledialog.askstring("Modify Employee", "Enter the ID of the employee to modify")

        # Checking if the entered employee ID exists in the employee dictionary
        if emp_id in self.employees:
            emp = self.employees[emp_id]

            # Asking user for new department and update if provided
            new_dept = simpledialog.askstring("Modify Employee",
                                              f"Current Department: {emp.department}. Enter new department (leave blank to keep current):")
            if new_dept:
                emp.department = new_dept

            # Asking user for new job title and update if provided
            new_job = simpledialog.askstring("Modify Employee",
                                             f"Current Job Title: {emp.jobTitle}. Enter new job title (leave blank to keep current):")
            if new_job:
                emp.jobTitle = new_job

            # Asking user for new salary and update if provided, handling conversion errors
            new_salary = simpledialog.askstring("Modify Employee",
                                                f"Current Salary: {emp.salary}. Enter new salary (leave blank to keep current):")
            if new_salary:
                try:
                    emp.salary = float(new_salary)
                except ValueError:
                    messagebox.showerror("Error", "Invalid salary input. Salary must be a number.")
                    return

                    # Saving the modified employee data
            save_data(self.employees)
            self.refresh_table()
        else:
            messagebox.showerror("Error", "Employee not found")


    # A function that removes an employee from the system after the user inputs the employee's ID
    def remove_employee(self):
        # Asking the user to enter the ID of the employee they wish to remove
        emp_id = simpledialog.askstring("Remove Employee", "Enter the ID of the employee to remove")

        # Checking if the employee ID exists
        if emp_id in self.employees:
            # deleting the employee entry using their ID if found
            del self.employees[emp_id]
            # Saving the updated data
            save_data(self.employees)
            self.refresh_table()
        else:
            messagebox.showerror("Error", "Employee not found")


    # A function that searches for and displays the details of an employee by their ID
    def find_employee(self):
        emp_id = simpledialog.askstring("Find Employee", "Enter the ID of the employee to find")
        try:
            # Loading the current set of employee data from storage
            self.employees = load_data()

            # Checiking if the entered employee ID exists in the loaded data
            if emp_id in self.employees:
                # Retrieving the employee object based on the provided ID
                emp = self.employees[emp_id]
                details = emp.get_details()
                # Displaying the employee details in an information messagebox
                messagebox.showinfo("Employee Details", details)
            else:
                messagebox.showerror("Error", "Employee not found")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the data: {e}")


    # A functions that initializes and displays the event management system interface
    def open_event_system(self):
        # Loading event data into the application
        self.events = load_event_data()

        # Setting up a Treeview widget to display event details in a tabular format
        self.event_tree = ttk.Treeview(self.root, columns=("Event ID", "Type", "Date", "Time", "Duration"),
                                       show="headings")
        self.event_tree.heading("Event ID", text="Event ID")
        self.event_tree.heading("Type", text="Type")
        self.event_tree.heading("Date", text="Date")
        self.event_tree.heading("Time", text="Time")
        self.event_tree.heading("Duration", text="Duration")
        self.event_tree.grid(row=3, column=0, columnspan=2, sticky='nsew')

        # Creating buttons for adding, modifying, removing, and finding events
        ttk.Button(self.root, text="Add Event", command=self.open_add_event_form).grid(row=4, column=0)
        ttk.Button(self.root, text="Modify Event", command=self.modify_event).grid(row=4, column=1)
        ttk.Button(self.root, text="Remove Event", command=self.remove_event).grid(row=5, column=0)
        ttk.Button(self.root, text="Find Event by ID", command=self.find_event).grid(row=5, column=1)

        # Refreshing the displayed event data
        self.refresh_event_table()


    # A function to clear and update the event table with the latest event data.
    def refresh_event_table(self):
        # Removing all existing entries from the Treeview widget
        for i in self.event_tree.get_children():
            self.event_tree.delete(i)
        # Inserting updated data for each event into the Treeview widget
        for event_id, event in self.events.items():
            self.event_tree.insert("", "end", values=(
                event.event_id, event.event_type, event.date, event.time, event.duration))

    # A function that opens a new window for adding a new event
    def open_add_event_form(self):
        self.add_event_window = tk.Toplevel(self.root)
        self.add_event_window.title("Add New Event")

        # Defining labels for event properties
        labels = ['Type:', 'Date:', 'Time:', 'Duration:']
        self.event_entries = {}
        event_types = ["Wedding", "Birthday", "Themed Parties", "Graduation" ,"Conference", "Seminar", "Workshop"]

        # Iterating over the labels to create and place corresponding input widgets
        for i, label in enumerate(labels):
            ttk.Label(self.add_event_window, text=label).grid(row=i, column=0)
            if label == 'Type:':
                type_var = tk.StringVar()
                ttk.OptionMenu(self.add_event_window, type_var, event_types[0], *event_types).grid(row=i, column=1)
                self.event_entries[label] = type_var
            else:
                entry = ttk.Entry(self.add_event_window)
                entry.grid(row=i, column=1)
                self.event_entries[label] = entry

        ttk.Button(self.add_event_window, text="Save Event", command=self.add_event).grid(row=len(labels), column=1)


    # A functions that collects data from the form, validates it, creates a new Event object, saves the data,
    #  and refreshes the event table
    def add_event(self):
        try:
            event_type = self.event_entries['Type:'].get().strip()
            date = self.event_entries['Date:'].get().strip()
            time = self.event_entries['Time:'].get().strip()
            duration = self.event_entries['Duration:'].get().strip()

            # Validating all fields are filled
            if not (event_type and date and time and duration):
                raise ValueError("All fields must be completed.")

            event_id = f"EV{self.event_id_counter}"
            self.event_id_counter += 1

            # Creating and saving the new event
            event = Event(event_id, event_type, date, time, duration)
            self.events[event.event_id] = event
            save_event_data(self.events)
            self.refresh_event_table()
            self.add_event_window.destroy()

        except Exception as e:
            tk.messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


    # A function that allows the user to modify an existing event
    def modify_event(self):
        event_id = simpledialog.askstring("Modify Event", "Enter the ID of the event to modify")

        # Checking if the entered event ID exists in the events dictionary
        if event_id in self.events:
            event = self.events[event_id]  # Retrieving the event object

            # Asking for new event details
            new_type = simpledialog.askstring("Modify Event",  f"Current Type: {event.event_type}. Enter new type (leave blank to keep current):")
            if new_type:
                event.event_type = new_type

            new_date = simpledialog.askstring("Modify Event", f"Current Date: {event.date}. Enter new date (leave blank to keep current):")
            if new_date:
                event.date = new_date

            new_time = simpledialog.askstring("Modify Event", f"Current Time: {event.time}. Enter new time (leave blank to keep current):")
            if new_time:
                event.time = new_time

            new_duration = simpledialog.askstring("Modify Event",  f"Current Duration: {event.duration}. Enter new duration (leave blank to keep current):")
            if new_duration:
                event.duration = new_duration

            # Saving the updated event data back to the storage
            save_event_data(self.events)
            self.refresh_event_table()

        else:
            messagebox.showerror("Error", "Event not found")


    #  A function to remove an event from the system after the user inputs the event's ID
    def remove_event(self):
        event_id = simpledialog.askstring("Remove Event", "Enter the ID of the event to remove")
        # Checking if the entered event ID exists
        if event_id in self.events:
            # If the event ID exists, delete the event from the dictionary
            del self.events[event_id]
            # Saving the updated events details
            save_event_data(self.events)
            self.refresh_event_table()
        else:
            messagebox.showerror("Error", "Event not found")


    # A function that prompts the user to enter an event ID and displays the event details if found
    def find_event(self):
        event_id = simpledialog.askstring("Find Event", "Enter the ID of the event to find")
        try:
            # Loading the current set of event data from storage
            self.events = load_event_data()
            # Checking if the entered event ID exists in the events dictionary
            if event_id in self.events:
                event = self.events[event_id]
                details = event.get_details()
                # Displaying the details in an informational message box
                messagebox.showinfo("Event Details", details)
            else:
                messagebox.showerror("Error", "Event not found")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the event data: {e}")


    # A function that Initializes and displays the supplier management interface.
    def open_supplier_system(self):
        # Loading supplier data from storage
        self.suppliers = load_supplier_data()

        # Setting up a Treeview widget to display supplier details in a structured tabular format
        self.supplier_tree = ttk.Treeview(self.root, columns=("Supplier ID", "Name", "Service Type"), show="headings")
        self.supplier_tree.heading("Supplier ID", text="Supplier ID")
        self.supplier_tree.heading("Name", text="Name")
        self.supplier_tree.heading("Service Type", text="Service Type")
        self.supplier_tree.grid(row=3, column=0, columnspan=2, sticky='nsew')

        # Creating buttons for different functions
        ttk.Button(self.root, text="Add Supplier", command=self.open_add_supplier_form).grid(row=4, column=0)
        ttk.Button(self.root, text="Modify Supplier", command=self.modify_supplier).grid(row=4, column=1)
        ttk.Button(self.root, text="Remove Supplier", command=self.remove_supplier).grid(row=5, column=0)
        ttk.Button(self.root, text="Find Supplier by ID", command=self.find_supplier).grid(row=5, column=1)

        self.refresh_supplier_table()


    # A function that clears and refreshes the supplier table with the latest supplier data
    def refresh_supplier_table(self):
        for i in self.supplier_tree.get_children():
            self.supplier_tree.delete(i)
        for supplier_id, supplier in self.suppliers.items():
            self.supplier_tree.insert("", "end", values=(
                supplier.supplier_id, supplier.name, supplier.service_type))


    # A function to open a new window for adding a new supplier
    def open_add_supplier_form(self):
        # Creating a new window for adding a supplier
        self.add_supplier_window = tk.Toplevel(self.root)
        self.add_supplier_window.title("Add New Supplier")

        labels = ['Name:', 'Service Type:']
        service_types = ['Catering', 'Sound System', 'Decoration', 'Photography', 'Security']

        self.supplier_entries = {}
        for i, label in enumerate(labels):
            ttk.Label(self.add_supplier_window, text=label).grid(row=i, column=0)
            if label == 'Service Type:':
                self.service_type_var = tk.StringVar(self.add_supplier_window)
                self.service_type_var.set('Select Service Type')
                entry = tk.OptionMenu(self.add_supplier_window, self.service_type_var, *service_types)
            else:
                entry = ttk.Entry(self.add_supplier_window)

            entry.grid(row=i, column=1)
            self.supplier_entries[label] = entry

        ttk.Button(self.add_supplier_window, text="Save Supplier", command=self.add_supplier).grid(row=len(labels), column=1)


    # A function to collects data from the form, validates it, creates a new Supplier object, saves the data, and refreshes the supplier table.
    def add_supplier(self):
        try:
            name = self.supplier_entries['Name:'].get().strip()
            service_type = self.service_type_var.get().strip()

            # Checking if any of the fields are empty
            if not name or not service_type:
                raise ValueError("All fields must be completed.")

            # Validating that a service type is selected
            if service_type == 'Select Service Type':
                raise ValueError("Please select a valid service type.")

            # Generating a unique supplier ID and creating a new Supplier object
            supplier_id = f"SP{self.supplier_id_counter}"
            self.supplier_id_counter += 1
            supplier = Supplier(supplier_id, name, service_type)

            self.suppliers[supplier.supplier_id] = supplier
            save_supplier_data(self.suppliers)
            self.refresh_supplier_table()
            self.add_supplier_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


    # A function to modify the details of a selected supplier
    def modify_supplier(self):
        # Asking for the ID of the supplier to modify
        supplier_id = simpledialog.askstring("Modify Supplier", "Enter the ID of the supplier to modify")

        # Checking if the supplier ID exists in the list of suppliers
        if supplier_id in self.suppliers:
            supplier = self.suppliers[supplier_id]

            new_name = simpledialog.askstring("Modify Supplier", f"Current Name: {supplier.name}. Enter new name (leave blank to keep current):")
            if new_name:
                supplier.name = new_name
            new_service_type = simpledialog.askstring("Modify Supplier", f"Current Service Type: {supplier.service_type}. Enter new service type (leave blank to keep current):")
            if new_service_type:
                supplier.service_type = new_service_type
            # Saving the updated supplier data and refreshing the supplier table
            save_supplier_data(self.suppliers)
            self.refresh_supplier_table()
        else:
            messagebox.showerror("Error", "Supplier not found")


    # A function that removes a supplier from the system based on the entered ID
    def remove_supplier(self):
        supplier_id = simpledialog.askstring("Remove Supplier", "Enter the ID of the supplier to remove")
        # Checking if the supplier ID exists in the list of suppliers
        if supplier_id in self.suppliers:
            del self.suppliers[supplier_id]
            save_supplier_data(self.suppliers)
            self.refresh_supplier_table()
        else:
            messagebox.showerror("Error", "Supplier not found")

    # A function that finds and displays details of a supplier based on the entered ID
    def find_supplier(self):
        supplier_id = simpledialog.askstring("Find Supplier", "Enter the ID of the supplier to find")
        try:
            self.suppliers = load_supplier_data()
            if supplier_id in self.suppliers:
                supplier = self.suppliers[supplier_id]
                details = str(supplier)
                messagebox.showinfo("Supplier Details", details)
            else:
                messagebox.showerror("Error", "Supplier not found")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the supplier data: {e}")


    # A function that initializes and displays the guest management system interface
    def open_guest_system(self):
        self.guests = load_guest_data()
        # Setting up a Treeview widget to display guest details in a tabular format
        self.guest_tree = ttk.Treeview(self.root, columns=("Guest ID", "Name", "Phone Number", "Gender"),
                                       show="headings")
        self.guest_tree.heading("Guest ID", text="Guest ID")
        self.guest_tree.heading("Name", text="Name")
        self.guest_tree.heading("Phone Number", text="Phone Number")
        self.guest_tree.heading("Gender", text="Gender")
        self.guest_tree.grid(row=3, column=0, columnspan=2, sticky='nsew')

        # Creating buttons for adding, modifying, removing, and finding guests
        ttk.Button(self.root, text="Add Guest", command=self.open_add_guest_form).grid(row=4, column=0)
        ttk.Button(self.root, text="Modify Guest", command=self.modify_guest).grid(row=4, column=1)
        ttk.Button(self.root, text="Remove Guest", command=self.remove_guest).grid(row=5, column=0)
        ttk.Button(self.root, text="Find Guest by ID", command=self.find_guest).grid(row=5, column=1)

        self.refresh_guest_table()


    # A function that clears and updates the guest table with the latest guest data
    def refresh_guest_table(self):
        for i in self.guest_tree.get_children():
            self.guest_tree.delete(i)
        for guest_id, guest in self.guests.items():
            self.guest_tree.insert("", "end",
                                   values=(guest.guestID, guest.get_full_name(), guest._phoneNumber, guest._gender))


    # A function that opens a new window for adding a new guest
    def open_add_guest_form(self):
        self.add_guest_window = tk.Toplevel(self.root)
        self.add_guest_window.title("Add New Guest")

        labels = ['First Name:', 'Last Name:', 'Gender:', 'Phone Number:']
        self.guest_entries = {}

        # Adding entry fields for guest information
        for i, label in enumerate(labels):
            ttk.Label(self.add_guest_window, text=label).grid(row=i, column=0)
            if label == 'Gender:':
                gender_var = tk.StringVar()
                gender_menu = ttk.OptionMenu(self.add_guest_window, gender_var, "Male", "Female")
                gender_menu.grid(row=i, column=1)
                self.guest_entries[label] = gender_var
            else:
                entry = ttk.Entry(self.add_guest_window)
                entry.grid(row=i, column=1)
                self.guest_entries[label] = entry

        ttk.Button(self.add_guest_window, text="Save Guest", command=self.add_guest).grid(row=len(labels), column=1)


    # A function that collects data from the form, creates a new Guest object, saves the data,and refreshes the guest table.
    def add_guest(self):
        try:
            first_name = self.guest_entries['First Name:'].get().strip()
            last_name = self.guest_entries['Last Name:'].get().strip()
            gender = self.guest_entries['Gender:'].get().strip()
            phone_number = self.guest_entries['Phone Number:'].get().strip()

            # Validating all fields are filled
            if not (first_name and last_name and gender and phone_number):
                raise ValueError("All fields must be completed.")

            guest_id = f"G{self.guest_id_counter}"
            self.guest_id_counter += 1

            # Creating and saving the new guest
            guest = Guest(first_name, last_name, gender, phone_number, guest_id)
            self.guests[guest.guestID] = guest
            save_guest_data(self.guests)
            self.refresh_guest_table()
            self.add_guest_window.destroy()

        except Exception as e:
            tk.messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


    # A function modifies guest information based on user input
    def modify_guest(self):
        guest_id = simpledialog.askstring("Modify Guest", "Enter the ID of the guest to modify")
        if guest_id in self.guests:
            guest = self.guests[guest_id]

            new_firstName = simpledialog.askstring("Modify Guest", f"Current First Name: {guest._firstName}. Enter new first name (leave blank to keep current):")
            if new_firstName:
                guest._firstName = new_firstName

            new_lastName = simpledialog.askstring("Modify Guest", f"Current Last Name: {guest._lastName}. Enter new last name (leave blank to keep current):")
            if new_lastName:
                guest._lastName = new_lastName

            new_phoneNumber = simpledialog.askstring("Modify Guest", f"Current Phone Number: {guest._phoneNumber}. Enter new phone number (leave blank to keep current):")
            if new_phoneNumber:
                guest._phoneNumber = new_phoneNumber

            # Saving changes and updating the guest table
            save_guest_data(self.guests)
            self.refresh_guest_table()
        else:
            messagebox.showerror("Error", "Guest not found")


    # A function that removes a guest from the guest list based on user input
    def remove_guest(self):
        guest_id = simpledialog.askstring("Remove Guest", "Enter the ID of the guest to remove")
        if guest_id in self.guests:
            del self.guests[guest_id]
            save_guest_data(self.guests)
            self.refresh_guest_table()
        else:
            messagebox.showerror("Error", "Guest not found")


    # A function that finds and displays guest details based on user input
    def find_guest(self):
        guest_id = simpledialog.askstring("Find Guest", "Enter the ID of the guest to find")
        if guest_id in self.guests:
            guest = self.guests[guest_id]
            details = guest.get_details()
            messagebox.showinfo("Guest Details", details)
        else:
            messagebox.showerror("Error", "Guest not found")

    # A function that opens the client management system interface
    def open_client_system(self):
        # Loading client data
        self.clients = load_client_data()
        # Initializing client treeview
        self.client_tree = ttk.Treeview(self.root, columns=("Client ID", "Name", "Phone", "Budget", "Events"),
                                        show="headings")
        self.client_tree.heading("Client ID", text="Client ID")
        self.client_tree.heading("Name", text="Name")
        self.client_tree.heading("Phone", text="Phone")
        self.client_tree.heading("Budget", text="Budget")
        self.client_tree.heading("Events", text="Events")
        self.client_tree.grid(row=3, column=0, columnspan=2, sticky='nsew')

        # Setting up buttons for client management
        ttk.Button(self.root, text="Add Client", command=self.open_add_client_form).grid(row=4, column=0)
        ttk.Button(self.root, text="Modify Client", command=self.modify_client).grid(row=4, column=1)
        ttk.Button(self.root, text="Remove Client", command=self.remove_client).grid(row=5, column=0)
        ttk.Button(self.root, text="Find Client by ID", command=self.find_client).grid(row=5, column=1)

        self.refresh_client_table()


    # A function to refreshe the client table with the latest client data
    def refresh_client_table(self):
        # Clearing existing entries in the client treeview
        for i in self.client_tree.get_children():
            self.client_tree.delete(i)
        # Inserting updated client data into the treeview
        for client_id, client in self.clients.items():
            self.client_tree.insert("", "end", values=(
            client.clientID, client.get_full_name(), client._phoneNumber, client.budget, client.numOf_events))

    # A function that opens a new window for adding a new client
    def open_add_client_form(self):

        # Creating a new window for adding a client
        self.add_client_window = tk.Toplevel(self.root)
        self.add_client_window.title("Add New Client")

        # Defining labels for client properties
        labels = ['First Name:', 'Last Name:', 'Gender:', 'Phone Number:', 'Budget:', 'Number of Events:']
        self.client_entries = {}
        self.gender_var = tk.StringVar(self.add_client_window)
        self.gender_var.set('Select Gender')

        # Creating input fields for client information
        for i, label in enumerate(labels):
            ttk.Label(self.add_client_window, text=label).grid(row=i, column=0)
            if label == 'Gender:':
                entry = ttk.OptionMenu(self.add_client_window, self.gender_var, 'Select Gender', 'Male', 'Female')
            else:
                entry = ttk.Entry(self.add_client_window)
            entry.grid(row=i, column=1)
            self.client_entries[label] = entry

        ttk.Button(self.add_client_window, text="Save Client", command=self.add_client).grid(row=len(labels), column=1)


    # A function that collects data from the form, validates it, creates a new Client object, saves the data, and refreshes the client table.
    def add_client(self):
        # Extracting data from the input fields
        first_name = self.client_entries['First Name:'].get()
        last_name = self.client_entries['Last Name:'].get()
        gender = self.gender_var.get()
        phone_number = self.client_entries['Phone Number:'].get()
        budget = self.client_entries['Budget:'].get()
        num_of_events = self.client_entries['Number of Events:'].get()

        # Validating and converting budget and number of events
        try:
            budget = float(budget) if budget.strip() else 0
            num_of_events = int(num_of_events) if num_of_events.strip() else 0
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Please ensure budget is a number and number of events is an integer.")
            return

        # Handling empty inputs
        if not (first_name and last_name and phone_number and gender and budget and num_of_events):
            messagebox.showerror("Invalid Input", "All fields must be filled.")
            return

        # Generating a unique client ID
        client_id = f"C{self.client_id_counter}"
        self.client_id_counter += 1

        # Creating and saving the new client
        client = Client(first_name, last_name, gender, phone_number, client_id, budget, num_of_events)
        self.clients[client.clientID] = client
        save_client_data(self.clients)
        self.refresh_client_table()
        self.add_client_window.destroy()


    # A function that allows modification of an existing client's budget and number of events based on user input
    def modify_client(self):
        client_id = simpledialog.askstring("Modify Client", "Enter the ID of the client to modify")
        # Checking if the client exists in the client dictionary
        if client_id in self.clients:
            client = self.clients[client_id]

            new_budget = simpledialog.askstring("Modify Client",  f"Current Budget: {client.budget}. Enter new budget (leave blank to keep current):")
            if new_budget:
                try:
                    # Attempting to convert the input to float and update the budget
                    client.update_budget(float(new_budget))
                except ValueError:
                    messagebox.showerror("Error", "Invalid budget input. Budget must be a number.")
                    return

            # Prompt for a new number of events, only update if a new value is provided
            new_num_of_events = simpledialog.askstring("Modify Client",  f"Current Number of Events: {client.numOf_events}. Enter new number of events (leave blank to keep current):")
            if new_num_of_events:
                try:
                    # Attempting to convert the input to integer and update the number of events
                    client.update_num_of_events(int(new_num_of_events))
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Number of events must be an integer.")
                    return

            # Saving the updated client data to storage
            save_client_data(self.clients)
            self.refresh_client_table()
        else:
            messagebox.showerror("Error", "Client not found")


    # A function that removes a client from the system based on their ID
    def remove_client(self):
        client_id = simpledialog.askstring("Remove Client", "Enter the ID of the client to remove")
        # Checking if the client exists in the database
        if client_id in self.clients:
            # Removing the client from the dictionary
            del self.clients[client_id]
            # Saving the updated client data to the database
            save_client_data(self.clients)
            self.refresh_client_table()
        else:
            messagebox.showerror("Error", "Client not found")


    # A function that searches for a client by ID and displays their detailed information if found.
    def find_client(self):
        client_id = simpledialog.askstring("Find Client", "Enter the ID of the client to find")
        # Checking if the client exists in the database
        if client_id in self.clients:
            client = self.clients[client_id]
            details = client.display_details()
            messagebox.showinfo("Client Details", details)
        else:
            messagebox.showerror("Error", "Client not found")


    # A function that opens the venue management system interface
    def open_venue_system(self):
        self.venues = load_venue_data()
        self.venue_tree = ttk.Treeview(self.root, columns=("Venue ID", "Address", "Min Guests", "Max Guests"),
                                       show="headings")
        self.venue_tree.heading("Venue ID", text="Venue ID")
        self.venue_tree.heading("Address", text="Address")
        self.venue_tree.heading("Min Guests", text="Min Guests")
        self.venue_tree.heading("Max Guests", text="Max Guests")
        self.venue_tree.grid(row=3, column=0, columnspan=2, sticky='nsew')

        ttk.Button(self.root, text="Add Venue", command=self.open_add_venue_form).grid(row=4, column=0)
        ttk.Button(self.root, text="Modify Venue", command=self.modify_venue).grid(row=4, column=1)
        ttk.Button(self.root, text="Remove Venue", command=self.remove_venue).grid(row=5, column=0)
        ttk.Button(self.root, text="Find Venue by ID", command=self.find_venue).grid(row=5, column=1)

        self.refresh_venue_table()


    # A function that refreshes the venue table with the latest venue data
    def refresh_venue_table(self):
        for i in self.venue_tree.get_children():
            self.venue_tree.delete(i)
        for venue_id, venue in self.venues.items():
            self.venue_tree.insert("", "end",
                                   values=(venue.venue_id, venue.address, venue.min_guests, venue.max_guests))


    # A function that opens a new window for adding a new venue.
    def open_add_venue_form(self):
        self.add_venue_window = tk.Toplevel(self.root)
        self.add_venue_window.title("Add New Venue")

        labels = ['Address:', 'Min Guests:', 'Max Guests:']
        self.venue_entries = {}

        for i, label in enumerate(labels):
            ttk.Label(self.add_venue_window, text=label).grid(row=i, column=0)
            entry = ttk.Entry(self.add_venue_window)
            entry.grid(row=i, column=1)
            self.venue_entries[label] = entry

        ttk.Button(self.add_venue_window, text="Save Venue", command=self.add_venue).grid(row=len(labels), column=1)


    # A function that collects data from the form, validates it, creates a new Venue object, saves the data, and refreshes the venue table
    def add_venue(self):
        address = self.venue_entries['Address:'].get()
        min_guests = self.venue_entries['Min Guests:'].get()
        max_guests = self.venue_entries['Max Guests:'].get()
        try:
            min_guests = int(min_guests)
            max_guests = int(max_guests)
            if not address:
                raise ValueError("Address cannot be empty.")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        venue_id = f"V{self.venue_id_counter}"
        self.venue_id_counter += 1

        venue = Venue(venue_id, address, min_guests, max_guests)
        self.venues[venue.venue_id] = venue
        save_venue_data(self.venues)
        self.refresh_venue_table()
        self.add_venue_window.destroy()


    # A functions that modifies venue information based on user input
    def modify_venue(self):
        venue_id = simpledialog.askstring("Modify Venue", "Enter the ID of the venue to modify")
        if venue_id in self.venues:
            venue = self.venues[venue_id]

            new_address = simpledialog.askstring("Modify Venue",
                                                 f"Current Address: {venue.address}. Enter new address (leave blank to keep current):")
            if new_address:
                venue.address = new_address

            new_min_guests = simpledialog.askstring("Modify Venue",
                                                    f"Current Min Guests: {venue.min_guests}. Enter new minimum guests (leave blank to keep current):")
            if new_min_guests:
                try:
                    venue.min_guests = int(new_min_guests)
                except ValueError:
                    messagebox.showerror("Error", "Minimum guests must be a number.")
                    return

            new_max_guests = simpledialog.askstring("Modify Venue",
                                                    f"Current Max Guests: {venue.max_guests}. Enter new maximum guests (leave blank to keep current):")
            if new_max_guests:
                try:
                    venue.max_guests = int(new_max_guests)
                except ValueError:
                    messagebox.showerror("Error", "Maximum guests must be a number.")
                    return

            save_venue_data(self.venues)
            self.refresh_venue_table()
        else:
            messagebox.showerror("Error", "Venue not found")


    # A function that removes a venue from the system based on its ID
    def remove_venue(self):
        venue_id = simpledialog.askstring("Remove Venue", "Enter the ID of the venue to remove")
        if venue_id in self.venues:
            del self.venues[venue_id]
            save_venue_data(self.venues)
            self.refresh_venue_table()
        else:
            messagebox.showerror("Error", "Venue not found")


    # A functions that finds and displays venue details based on the venue ID
    def find_venue(self):
        venue_id = simpledialog.askstring("Find Venue", "Enter the ID of the venue to find")
        if venue_id in self.venues:
            venue = self.venues[venue_id]
            details = str(venue)
            messagebox.showinfo("Venue Details", details)
        else:
            messagebox.showerror("Error", "Venue not found")



root = tk.Tk()
app = ManagementApp(root)
root.mainloop()
