from abc import ABC, abstractmethod
from datetime import date

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
        edit_choice = input("\nWhat would you like to edit? \n[1] Name \n[2] Date \n[3] Venue \n[4] All\n").lower() # user input for edit selection 
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
    def delete(self, event_no):
        if event_no in events:  # Check if event exists in events dictionary
            del events[event_no]  # Delete the event
            print(f"Event {event_no}: {self.event_name} deleted.")
            attendees_to_delete = [attendee_no for attendee_no, attendee in attendees.items() if attendee.event_no == event_no]
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

# empty dictionaries used to store any data for events/attendees
events = {}
attendees = {}