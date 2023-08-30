from datetime import date
import json
from abc import ABC, abstractmethod

# Abstract Base Class for all objects in the system, abstract methods
class BaseObject(ABC):
    def __init__(self, entity_no):
        self.entity_no = entity_no

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def edit(self):
        pass

    @abstractmethod
    def delete(self):
        pass

class Event(BaseObject):   # defining event class and inheriting from base class
    def __init__(self, event_no, event_name, event_date, event_venue):
        super().__init__(event_no) 
        self.event_no = event_no
        self.event_name = event_name
        self.event_date = event_date
        self.event_venue = event_venue
        self.attendees = []

# create method for adding events into the system
    def create(self):
        while True:
            event_no = input("\nEnter Event No. : ")
            if event_no in events:      # if statement checking validity of Event No.
                print("\nAn event with the same number already exists.")
                continue
            event_name = input("Enter Event name: ")
            while True: 
                try:     # try/except block to handle incorrect date format/user errors
                    date_str = input("Enter Event date (yyyy-mm-dd): ")
                    year, month, day = map(int, date_str.split('-'))
                    event_date = date(year, month, day)
                    break 
                except ValueError:
                    print("\nInvalid date format. Please use yyyy-mm-dd format.\n")
            event_venue = Venue.create(Venue)
            event = Event(event_no, event_name, event_date, event_venue)
            events[event_no] = event
            print(f"\nEvent {event_no} created: {event_name}")
            break

#edit event method
    def edit(self):
        print(f"\nEditing Event No.: {self.event_no}, Event Name: {self.event_name}, Event Date: {self.event_date}, Event Venue: {self.event_venue[0]}, Venue Capacity: {self.event_venue[1]}, Venue Location: {self.event_venue[2]}")
        edit_choice = input("\nWhat would you like to edit?\n \n[1] Name \n[2] Date \n[3] Venue \n[4] All\n").lower() # user input for edit selection 
        if edit_choice == 'name' or edit_choice =='1':
            self.event_name = input(f"\nUpdating event name from ({self.event_name}) to: ")
        elif edit_choice == 'date' or edit_choice == '2':
            while True:
                try: # try / except block to handle incorrect date format / user inputs
                    date_str = input(f"Enter updated event date ({self.event_date.strftime('%Y-%m-%d')}): ")
                    year, month, day = map(int, date_str.split('-'))
                    self.event_date = date(year, month, day)
                    print("\nEvent date updated.")
                    break
                except ValueError:
                    print("\nInvalid date format. Please use yyyy-mm-dd format.")
        elif edit_choice == 'venue' or edit_choice == '3':
            self.edit_venue()   
        elif edit_choice == 'all' or edit_choice == '4':
                self.edit_details()
        else:
            print("Invalid choice.")

# edit event venue method     
    def edit_venue(self):
        new_venue_name = input(f"\nEnter updated venue name ({self.event_venue[0]}): ")
        while True:
            try:  # try / except block to handle incorrect capacity input / user inputs
                new_venue_capacity = int(input(f"Enter updated venue capacity ({self.event_venue[1]}): "))
                break 
            except ValueError:
                print("\nInvalid input. Please enter a valid integer for capacity.")
        new_venue_location = input(f"Enter updated venue location ({self.event_venue[2]}): ")
        self.event_venue = (new_venue_name, new_venue_capacity, new_venue_location)
        print("\nEvent venue updated.")

# edit event details method
    def edit_details(self):
        self.event_name = input(f"\nUpdating event name from ({self.event_name}) to: ")
        while True:
            try:  # try / except block to handle incorrect date format / user inputs
                date_str = input(f"Enter updated event date ({self.event_date.strftime('%Y-%m-%d')}): ")
                year, month, day = map(int, date_str.split('-'))
                self.event_date = date(year, month, day)
                break
            except ValueError:
                print("\nInvalid date format. Please use yyyy-mm-dd format.")
        self.edit_venue()
        print("\nEvent details updated.")

# delete event method
    def delete(self):
        print(f"\nEvent {self.event_no}: {self.event_name} deleted.")
        global events, attendees
        if self.event_no in events:
            del events[self.event_no]
            attendees_to_delete = [attendee_no for attendee_no, attendee in attendees.items() if attendee.event_no == self.event_no]
            for attendee_no in attendees_to_delete:
                del attendees[attendee_no]               
        else:
            print("Event not found.")

    @classmethod # decorator for class specific method used to create an instance of Event from the dictionary.
    def from_dict(cls, event_dict):
        event_no = event_dict['event_no']
        event_name = event_dict['event_name'] 
        event_date_str = event_dict.get('date', '')  # Get the date string from the dictionary
        try: # try / except block to check format of date
            year, month, day = map(int, event_date_str.split('-'))
            event_date = date(year, month, day)
        except (ValueError, IndexError):
            print(f"Invalid date format: {event_date_str}. Using default date.")
            event_date = date.today()  
        event_venue = event_dict['event_venue']
        event = cls(event_no, event_name, event_date, event_venue)
        return event

class Venue(BaseObject):  # defining venue class and inheriting from base class
    def __init__(self, venue_no, venue_name, venue_capacity, venue_location):
        super().__init__(venue_no)
        self.venue_name = venue_name
        self.venue_capacity = venue_capacity
        self.venue_location = venue_location

# create venue method 
    def create(self):
            venue_name = input("Enter Venue name: ")
            while True:
                try:  #try/except block to handle incorrect values for venue capacity
                    venue_capacity = int(input("Enter Capacity of Venue: "))
                    break
                except ValueError:
                    print("\nInvalid input. Please enter a valid integer for capacity.")
            venue_location = input("Enter Venue location: ")
            return venue_name, venue_capacity, venue_location

class Attendee(BaseObject):  # attendee class with base class inheritance

    def __init__(self, attendee_no, event_no, name, phone, email):
        super().__init__(attendee_no)
        self.attendee_no = attendee_no
        self.event_no = event_no
        self.name = name
        self.phone = phone
        self.email = email

# create attendee method 
    def create(event_no):
        while True:
            event = events.get(event_no)
            try:
                if event:
                    attendee_no = input("\nEnter Attendee No.: ")
                    if attendee_no in attendees:  # if statement to check existence of the attendee no in the records
                        print("An attendee with the same number already exists.")
                        continue
                    name = input("Enter Attendee name: ")
                    while True:
                        try:  # try/except block to handle value error for incorrect inputs for phone numbers
                            phone = int(input("Enter phone number: "))
                            break  
                        except ValueError:
                            print("Invalid phone number. Please enter a valid phone number.")
                    email = input("Enter email: ")
                    attendee = Attendee(attendee_no, event_no, name, phone, email)
                    attendees[attendee_no] = attendee
                    event.attendees.append(attendee_no)
                    print(f"\nAttendee {attendee_no} added to Event {event_no}: {event.event_name}")
                    break
            except ValueError:
                print("Invalid input. Please enter valid values.")

# edit attendee method altering specific or all details
    def edit(self):
        print(f"\nEditing Attendee No. {self.attendee_no}, Name: {self.name} for Event {self.event_no}")
        edit_choice = input("\nWhat would you like to edit? \n[1] Name \n[2] Phone \n[3] Email \n[4] Event \n[5] All\n").lower()   
        if edit_choice == 'name' or edit_choice == '1':
            self.name = input(f"\nUpdating attendee name from ({self.name}) to: ")
        elif edit_choice == 'phone' or edit_choice == '2':
            while True:
                try: # try/except block to handle value error for incorrect inputs for phone numbers
                    self.phone = int(input(f"\nUpdating phone from ({self.phone}) to: "))
                    print("\nAttendee phone number updated.")
                    break  
                except ValueError:
                    print("Invalid input. Please enter a valid phone number.")
        elif edit_choice == 'email' or edit_choice == '3':
            self.email = input(f"\nUpdating email from ({self.email}) to: ")            
        elif edit_choice == 'event' or edit_choice == '4':
            new_event_no = input(f"\nEnter new event no: ")
            if new_event_no in events:
                self.event_no = new_event_no
                print(f"\nAttendee moved to Event {self.event_no}.")
            else:
                print(f"Event {new_event_no} not found.")
        elif edit_choice == 'all' or edit_choice == '5':  
            self.name = input(f"\nUpdating attendee name from ({self.name}) to: ")
            while True:
                try: # try/except block to handle value error for incorrect inputs for phone numbers
                    self.phone = int(input(f"\nUpdating phone from ({self.phone}) to: "))
                    break  
                except ValueError:
                    print("Invalid input. Please enter a valid phone number.")
            self.email = input(f"\nUpdating email from ({self.email}) to: ")
            new_event_no = input(f"\nEnter new event no: ")
            if new_event_no in events:
                self.event_no = new_event_no
                print(f"\nAttendee moved to Event {self.event_no}.")
            else:
                print(f"Event {new_event_no} not found.")
            print("\nAttendee details updated.")
        else:
            print("Invalid option.")


# delete attendee method
    def delete(self):
        global attendees
        if self.attendee_no in attendees:
            del attendees[self.attendee_no]
            print(f"Deleted Attendee {self.attendee_no}: {self.name} from {self.event_no}")
        else:
            print("Attendee not found.")

    @classmethod   # decorator for class specific method, used to create an instance of Attendee from the dictionary.
    def from_dict(cls, attendee_dict):
        attendee_no = attendee_dict['attendee_no']
        event_no = attendee_dict['event_no']
        name = attendee_dict['name']
        phone = attendee_dict['phone']
        email = attendee_dict['email']
        attendee = cls(attendee_no, event_no, name, phone, email)
        return attendee

class User():
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email 

    def create_user(users):
        username = input('Enter a username: ')
        if username in users:
            ('Username already exists. Please chose another username.')
        password = input('Enter a password: ')
        email = input('Enter an email: ')
        users[username] = User(username, password, email)
        print('User creation successful.')
        save_data_to_files()

    @staticmethod
    def login(users):
        login_attempts = 0
        while True:
            username = input('\nEnter your username: ')
            password = input('Enter your password: ')
            user = users.get(username)
            if user and user.password == password:
                print('\nLogin successful.')
                return True, login_attempts
            else:
                print('\nLogin unsuccessful. Check spelling for username and/or password.')
                login_attempts += 1
                if login_attempts == 3:
                    print('\nSeek help from an admin.')
                    return False, login_attempts


    @classmethod   # decorator for class specific method, used to create an instance of Attendee from the dictionary.
    def from_dict(cls, users_dict):
        username = users_dict['username']
        password = users_dict['password']
        email = users_dict['email']
        user = cls(username, password, email)
        return user
# empty dictionaries used to store any data for events/attendees
events = {}
attendees = {}
users = {}

# function to list attendees based off of an event no.
def list_attendees(event_no):
    event = events.get(event_no)
    if event: # if statement checking if event is in records
        attendees_found = False 
        for attendee_no, attendee in attendees.items(): # for loop to iterate through dictionary 
            if attendee.event_no == event.event_no:
                print(f"\nAttendees for Event {event_no}:")
                print("------------------------------------")
                print(f"Attendee No. {attendee_no}: {attendee.name}")  
                attendees_found = True
        if not attendees_found:
            print("\nNo attendees found for event.")
    else:
        print("\nEvent not found.")

# function listing all events using for loop to iterate through relevant dictionary
def list_all_events():
    if not events:
        print("\nNo events found.")
    else:
        for event_no, event in events.items():
            print('------------------------------------------------------------------------------------------------------------------------')
            print(f"Event No. {event_no}: {event.event_name}, Venue Name: {event.event_venue[0]}, Capacity: {event.event_venue[1]}, Location: {event.event_venue[2]},  Date: {event.event_date}")

# function listing a singular event
def list_event():
    user_input = input("\nEnter Event No. to list: ")    
    event_no = user_input
    event = events.get(event_no)
    if event:
        print("------------------------------------------------------------------------------------------------------------------------")
        print(f"Event {event_no}: {event.event_name}, Venue Name: {event.event_venue[0]}, Capacity: {event.event_venue[1]}, Location: {event.event_venue[2]},  Date: {event.event_date}")
    else:
        print("\nEvent not found.")  

# function that loads data from events and attendees files
def load_data_from_files():
    try:   # try / except block displaying error message if no file was found and starting with an empty dictionary.
        with open("events_data.json", "r") as events_file:
            events_data = json.load(events_file)
            global events
            events = {event_no: Event.from_dict(event_data) for event_no, event_data in events_data.items()}
    except FileNotFoundError:
        print("Events data file not found. Starting with empty events dictionary.")
        events = {event_no: Event.from_dict(event_data) for event_no, event_data in events.items()}

    try:  # try / except block displaying error message if no file was found and starting with an empty dictionary.
        with open("attendees_data.json", "r") as attendees_file:
            attendees_data = json.load(attendees_file)
            global attendees
            attendees = {attendee_no: Attendee.from_dict(attendee_data) for attendee_no, attendee_data in attendees_data.items()}
    except FileNotFoundError:
        print("\nAttendees data file not found. Starting with empty attendees dictionary.")
        attendees = {attendee_no: Attendee.from_dict(attendee_data) for attendee_no, attendee_data in attendees.items()}

    try:  # try / except block displaying error message if no file was found and starting with an empty dictionary.
        with open("users_data.json", "r") as users_file:
            users_data = json.load(users_file)
            global users
            users = {username: User.from_dict(users_data) for username, users_data in users_data.items()}
    except FileNotFoundError:
        print("\nUsers data file not found. Starting with empty attendees dictionary.")
        users = {username: User.from_dict(users_data) for username, users_data in users.items()}

# function saving the data to their appropriate files. 
def save_data_to_files():
    with open("events_data.json", "w") as events_file:
        json.dump(events, events_file, indent=4, default=serialize_event)
    
    with open("attendees_data.json", "w") as attendees_file:
        json.dump(attendees, attendees_file, indent=4, default=serialize_attendee)

    with open("users_data.json", "w") as users_file:
        json.dump(users, users_file, indent=4, default=serialize_user)

def serialize_user(obj):
    if isinstance(obj, User):
        return {
            "username": obj.username,
            "password": obj.password,
            "email" : obj.email
        }
    raise TypeError("Object of type Users is not JSON serializable")

# function that handles the data to be inputted in the correct format for the attendees JSON file 
def serialize_attendee(obj):
    if isinstance(obj, Attendee):
        return {
            "attendee_no": obj.attendee_no,
            "event_no": obj.event_no,
            "name": obj.name,
            "phone": obj.phone,
            "email": obj.email
        }
    raise TypeError("Object of type Attendee is not JSON serializable")

# function that handles the data to be inputted in the correct format for the events JSON file 
def serialize_event(obj):
    if isinstance(obj, Event):
        return {
            "event_no": obj.event_no,
            "event_name": obj.event_name,
            "date": obj.event_date.strftime("%Y-%m-%d") if isinstance(obj.event_date, date) else obj.event_date, 
            "event_venue": obj.event_venue,
            "attendees": obj.attendees
        }
    raise TypeError("Object of type Event is not JSON serializable")

def main_menu():
    while True: # while loop ensuring the program keeps running till user exits the system
        print("\n---------------------------\n| Event Management System |\n---------------------------")
        print("\nPlease select one of the following options: \n[1] List Events \n[2] List Attendees \n[3] Customize Events \n[4] Customize Atteendees \n[5] Logout")
        user_input = input("\n")

        # if / elif statements based on user input 
        if user_input == '5' or user_input.lower() == 'logout':
            print('\nLogging out of the EMS.')
            break

        elif user_input == '1':
            load_data_from_files() # calling load data function 
            while True: 
                event_listing = input("\nSelect an option: \n[1] All Events  \n[2] Event\n")
                if event_listing.lower() == 'all' or event_listing.lower() == 'all events' or event_listing == '1':
                    list_all_events() # calling list all events function 
                    break
                elif event_listing.lower() == 'event' or event_listing == '2':
                    list_event() # calling list event function 
                    break
                else:
                    print("\nInvalid choice. ")

        elif user_input == '2':
            load_data_from_files() # load data function
            list_all_events() # calling list all events function so user knows event numbers 
            while True:
                event_no = input("\nEnter Event no. to list attendees: ")
                if event_no in events:
                    list_attendees(event_no) # list attendees function with event no. as argument 
                    break 
                else:
                    print("\nEvent not found.")
                    break
                                   
        elif user_input == '3':
            load_data_from_files() # calling load data function 
            while True:
                user_choice = input("\nSelect an option: \n[1] Create an event \n[2] Edit an event \n[3] Delete an event\n")
                if user_choice.lower() == 'create' or user_choice == '1':
                    try: # try / except block for value error for the num_events prompt
                        num_events = int(input("\nEnter the number of events to create: ")) # user input to create a number of events 
                        for x in range(num_events):  # for loop to create number of events based off of user input 
                            Event.create(Event)      # calling create event method 
                            save_data_to_files()     # calling save data function 
                        break
                    except ValueError:
                        print("Invalid input. Please provide valid inputs for event creation.")
                elif user_choice.lower() == 'edit' or user_choice == '2':
                            event_no = input("\nEnter Event No. to edit: ")
                            event = events.get(event_no)
                            if not event:
                                print("\nEvent not found.")
                            else:
                                event.edit()
                                save_data_to_files() # calling save data function 
                                break
                elif user_choice.lower() == 'delete' or user_choice == '3':
                    event_no = input("\nEnter Event No. to delete: ")
                    event = events.get(event_no)
                    if event:
                        event.delete(event_no) # calling event delete method
                        save_data_to_files() # calling save data function 
                        break  
                    else:
                        print("\nEvent not found.")
                else:
                    print("Invalid choice.")

        elif user_input == '4':
            load_data_from_files() # load data function 
            user_edit = input("\nSelect an option: \n[1] Add an attendee  \n[2] Delete an attendee \n[3] Edit an attendee\n")
            if user_edit.lower() == 'add' or user_edit == '1':
                list_all_events()  # call list all events function so user knows which events are available
                while True:
                    event_no = input("\nEnter Event No. to add attendee: ")
                    if event_no not in events:
                        print("\nEvent not found.")
                        break
                    else:
                        while True:
                            try: # try / except block for value error on num_attendees
                                num_attendees = int(input("\nEnter the number of attendees to create: ")) # user input to create a number of attendees
                                break
                            except ValueError:
                                print("Invalid number. Please enter a valid number.")
                        for x in range(num_attendees):  # for loop to create a number of attendees based of user input 
                            Attendee.create(event_no)  # create attendee method with event no. as argument 
                            save_data_to_files() # save data function 
                        break
            elif user_edit.lower() == 'delete' or user_edit == '2': 
                attendee_no = input("\nEnter Attendee No. you wish to delete: ")
                attendee = attendees.get(attendee_no) # getting attendee no. from attendee dictionary 
                if attendee:
                    attendee.delete() # calling delete attendee method 
                    save_data_to_files() # save data function 
                else:
                    print("\nAttendee not found.")            
            elif user_edit.lower() == 'edit' or user_edit == '3':
                attendee_no = input("\nEnter Attendee No. you wish to edit: ")
                attendee = attendees.get(attendee_no) # getting attendee no. from attendee dictionary 
                if attendee:
                    attendee.edit() # edit attendee method 
                    save_data_to_files() # save data function 
                else:
                    print("\nAttendee not found.")
            
        else:
            print("\nInvalid choice.")
  
# main function for the entire system
def main():
    load_data_from_files()
    while True: # while loop ensuring the program keeps running till user exits the system
        print("\n---------------------------\n| Event Management System |\n---------------------------")
        print('\nPlease select an option: \n[1] Login \n[2] Register \n[3] Exit\n')
        user_login = input("")
        if user_login == '1':
            login_successful, login_attempts = User.login(users)
            if login_successful:
                main_menu()
            elif login_attempts == 3:
                continue
        elif user_login == '2': 
            User.create_user(users)
            save_data_to_files()
        elif user_login == '3':
            print('Goodbye!')
            break
        else: 
            print('Invalid choice.')

if __name__ == "__main__":  # calling main function 
    main()
