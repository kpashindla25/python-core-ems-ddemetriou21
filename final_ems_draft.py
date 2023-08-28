from abc import ABC, abstractmethod
from datetime import date
import json

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
                print("An event with the same number already exists.")
                continue
            event_name = input("Enter Event name: ")
            while True: 
                try:     # try/except block to handle incorrect date format/user errors
                    date_str = input("Enter Event date (yyyy-mm-dd): ")
                    year, month, day = map(int, date_str.split('-'))
                    event_date = date(year, month, day)
                    break 
                except ValueError:
                    print("Invalid date format. Please use yyyy-mm-dd format.")
            event_venue = Venue.create(Venue)
            event = Event(event_no, event_name, event_date, event_venue)
            events[event_no] = event
            print(f"\nEvent {event_no} created: {event_name}")
            break

#edit event method
    def edit(self):
        print(f"\nEditing Event No.: {self.event_no}, Event Name: {self.event_name}, Event Date: {self.event_date}, Event Venue: {self.event_venue[0]}, Venue Capacity: {self.event_venue[1]}, Venue Location: {self.event_venue[2]}")
        edit_choice = input("What would you like to edit? \n- Name \n- Date \n- Venue \n- All\n").lower() # user input for edit selection 
        if edit_choice == 'venue':
            self.edit_venue()
        elif edit_choice in {'name', 'date', 'all'}:
            if edit_choice == 'all':
                self.edit_details()
            elif edit_choice == 'date':
                while True:
                    try: # try / except block to handle incorrect date format / user inputs
                        date_str = input(f"Enter updated event date ({self.event_date.strftime('%Y-%m-%d')}): ")
                        year, month, day = map(int, date_str.split('-'))
                        self.event_date = date(year, month, day)
                        print("\nEvent date updated.")
                        break
                    except ValueError:
                        print("Invalid date format. Please use yyyy-mm-dd format.")
        else:
            new_value = input(f"Enter updated {edit_choice} ({getattr(self, 'event_' + edit_choice)}): ")
            setattr(self, 'event_' + edit_choice, new_value)
            print("\nEvent details updated.")

# edit event venue method     
    def edit_venue(self):
        new_venue_name = input(f"Enter updated venue name ({self.event_venue[0]}): ")
        while True:
            try:  # try / except block to handle incorrect capacity input / user inputs
                new_venue_capacity = int(input(f"Enter updated venue capacity ({self.event_venue[1]}): "))
                break 
            except ValueError:
                print("Invalid input. Please enter a valid integer for capacity.")
        new_venue_location = input(f"Enter updated venue location ({self.event_venue[2]}): ")
        self.event_venue = (new_venue_name, new_venue_capacity, new_venue_location)
        print("\nEvent venue updated.")

# edit event details method
    def edit_details(self):
        self.event_name = input(f"Updating event name from ({self.event_name}) to: ")
        while True:
            try:  # try / except block to handle incorrect date format / user inputs
                date_str = input(f"Enter updated event date ({self.event_date.strftime('%Y-%m-%d')}): ")
                year, month, day = map(int, date_str.split('-'))
                self.event_date = date(year, month, day)
                break
            except ValueError:
                print("Invalid date format. Please use yyyy-mm-dd format.")
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
                    print("Invalid input. Please enter a valid integer for capacity.")
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
        print(f"\nEditing Attendee No. {self.attendee_no}, Name: {self.name} for Event {self.event_no}:")
        edit_choice = input("\nWhat would you like to edit? \n- Name \n- Phone \n- Email \n- Event \n- All\n").lower()
        if edit_choice in {'name', 'phone', 'email', 'event', 'all'}:   
            if edit_choice == 'name':
                self.name = input(f"\nUpdating attendee name from ({self.name}) to: ")
            elif edit_choice == 'phone':
                while True:
                        try: # try/except block to handle value error for incorrect inputs for phone numbers
                            self.phone = int(input(f"\nUpdating phone from ({self.phone}) to: "))
                            print("\nAttendee phone number updated.")
                            break  
                        except ValueError:
                            print("Invalid input. Please enter a valid phone number.")
            elif edit_choice == 'email':
                self.email = input(f"\nUpdating email from ({self.email}) to: ")            
            elif edit_choice == 'event':
                    self.event_no = input(f"\nUpdating event no from ({self.event_no}) to: ")
                    print(f"\nAttendee moved to Event {self.event_no}.")
            elif edit_choice == 'all':  
                    self.name = input(f"\nUpdating attendee name from ({self.name}) to: ")
                    while True:
                        try: # try/except block to handle value error for incorrect inputs for phone numbers
                            self.phone = int(input(f"\nUpdating phone from ({self.phone}) to: "))
                            break  
                        except ValueError:
                            print("Invalid input. Please enter a valid phone number.")
                    self.email = input(f"\nUpdating email from ({self.email}) to: ")
                    self.event_no = input(f"\nUpdating event no from ({self.event_no}) to: ")
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

# empty dictionaries used to store any data for events/attendees
events = {}
attendees = {}

# function to list attendees based off of an event no.
def list_attendees(event_no):
    print(f"\nAttendees for Event {event_no}:")
    event = events.get(event_no)
    if event: # if statement checking if event is in records
        attendees_found = False 
        for attendee_no, attendee in attendees.items(): # for loop to iterate through dictionary 
            if attendee.event_no == event.event_no:
                print("------------------------------------")
                print(f"\nAttendee No. {attendee_no}: {attendee.name}")  
                attendees_found = True
        if not attendees_found:
            print("\nNo attendees found for this event.")
    else:
        print("\nEvent not found.")

# function listing all events using for loop to iterate through relevant dictionary
def list_all_events():
    if not events:
        print("\nNo events found.")
    else:
        for event_no, event in events.items():
            print('------------------------------------------------------------------------------------------------------------------------')
            print(f"\nEvent No. {event_no}: {event.event_name}, Venue Name: {event.event_venue[0]}, Capacity: {event.event_venue[1]}, Location: {event.event_venue[2]},  Date: {event.event_date}")


# function listing a singular event
def list_event():
    while True:
        user_input = input("\nEnter Event No. to list: ")
        try: # try / except block to handle any user errors
            event_no = user_input
            event = events.get(event_no)
            if event:
                print(f"\nEvent {event_no}: {event.event_name}, Venue Name: {event.event_venue[0]}, Capacity: {event.event_venue[1]}, Location: {event.event_venue[2]},  Date: {event.event_date}")
            else:
                print("Event not found.")
            break  
        except ValueError:
            print("Invalid input. Please enter a valid integer for Event No.")

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

# function saving the data to their appropriate files. 
def save_data_to_files():
    with open("events_data.json", "w") as events_file:
        json.dump(events, events_file, indent=4, default=serialize_event)
    
    with open("attendees_data.json", "w") as attendees_file:
        json.dump(attendees, attendees_file, indent=4, default=serialize_attendee)

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

# main function for the entire system
def main():
    while True: # while loop ensuring the program keeps running till user exits the system
        print("\n---------------------------")
        print("| Event Management System |")
        print("---------------------------")
        print("\nPlease select one of the following options: ")
        print("\n[1] List event(s)")
        print("[2] Create/Edit/Delete an event")
        print("[3] List attendees of an event")
        print("[4] Add/Delete/Edit an attendee from an event")  
        print("[E]xit")
        user_input = input("\n")

        if user_input.lower() == 'e' or user_input.lower() == 'exit':
            print("\nGoodbye!")
            break

        elif user_input == '1':
            load_data_from_files() # calling load data function 
            while True: 
                event_listing = input("\nSelect an option: \n- All Events  \n- Event \n")
                if event_listing.lower() == 'all' or event_listing.lower() == 'all events':
                    list_all_events() # calling list all events function 
                    break
                elif event_listing.lower() == 'event':
                    list_event() # calling list event function 
                    break
                else:
                    print("Invalid choice. ")
                                           
        elif user_input == '2':
            load_data_from_files() # calling load data function 
            while True:
                user_choice = input("\nSelect an option: \n- Create an event \n- Edit an event \n- Delete an event\n")
                if user_choice.lower() == 'edit':
                        try:  # try / except block to handle any user errors or if event no is correct
                            event_no = input("\nEnter Event No. to edit: ")
                            event = events.get(event_no)
                            if event:
                                event.edit()
                                save_data_to_files() # calling save data function 
                                break
                            else:
                                ("Event not found.")
                        except ValueError:
                            print("Event not found. Please enter a valid Event No.")
                elif user_choice.lower() == 'create':
                    try: # try / except block for value error for the num_events prompt
                        num_events = int(input("\nEnter the number of events to create: ")) # user input to create a number of events 
                        for x in range(num_events):  # for loop to create number of events based off of user input 
                            Event.create(Event)      # calling create event method 
                            save_data_to_files()     # calling save data function 
                        break
                    except ValueError:
                        print("Invalid input. Please provide valid inputs for event creation.")
                elif user_choice.lower() == 'delete':
                    try: # try / except block for type error for event_no
                        event_no = input("\nEnter Event No. to delete: ")
                        event = events[event_no]
                        if event:
                            event.delete() # calling event delete method
                            save_data_to_files() # calling save data function 
                            break  
                        else:
                            print("Event not found.")
                    except TypeError:
                        print("Invalid input. Please enter a valid Event No.")
                else:
                    print("Invalid choice.")

        elif user_input == '3':
            load_data_from_files() # load data function 
            while True:
                list_all_events() # list all events function 
                event_no = input("\nEnter Event no. to list attendees: ")
                if event_no in events:
                    list_attendees(event_no) # list attendees function with event no. as argument 
                    break 
                else:
                    print("\nEvent not found. Please enter a valid event number.")

        elif user_input == '4':
            load_data_from_files() # load data function 
            user_edit = input("\nSelect an option: \n- Add an attendee  \n- Delete an attendee \n- Edit an attendee\n")
            if user_edit.lower() == 'add':
                event_no = input("\nEnter Event No. to add attendee: ")
                while True:
                    try: # try / except block for value error on num_attendees
                        num_attendees = int(input("\nEnter the number of attendees to create: ")) # user input to create a number of attendees
                        break
                    except ValueError:
                        print("Invalid number. Please enter a valid number.")
                for x in range(num_attendees):  # for loop to create a number of attendees based of user input 
                    Attendee.create(event_no)  # create attendee method with event no. as argument 
                    save_data_to_files() # save data function 
            elif user_edit.lower() == 'edit':
                attendee_no = input("\nEnter Attendee No. you wish to edit: ")
                attendee = attendees.get(attendee_no) # getting attendee no. from attendee dictionary 
                if attendee:
                    attendee.edit() # edit attendee method 
                    save_data_to_files() # save data function 
                else:
                    print("Attendee not found.")
            elif user_edit.lower() == 'delete': 
                attendee_no = input("\nEnter Attendee No. you wish to delete from event: ")
                attendee = attendees.get(attendee_no) # getting attendee no. from attendee dictionary 
                if attendee:
                    attendee.delete() # calling delete attendee method 
                    save_data_to_files() # save data function 
                else:
                    print("Attendee not found.")

        else:
            print("\nInvalid choice.")

if __name__ == "__main__":  # calling main function 
    main()
