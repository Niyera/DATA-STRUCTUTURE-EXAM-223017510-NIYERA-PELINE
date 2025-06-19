/*
C++ OOP Final Project – Hotel Room Reservation System

Task Description:
-----------------
The goal of this project is to develop a hotel room reservation system using Object-Oriented Programming in C++. 
The system should:
- Allow adding and removing different types of rooms (Standard, Premium).
- Let users reserve a room for specific dates.
- Prevent double-booking for the same room on the same date.

How It Was Implemented:
------------------------
We used the following OOP concepts:
- Inheritance: Room types inherit from a base class.
- Polymorphism: Virtual functions allow dynamic behavior.
- Encapsulation: Reservation data is managed internally.
- Dynamic memory: Rooms and dates are managed manually (without STL).

Code Overview:
--------------
The code includes:
- A `Date` struct for storing reservation dates.
- A base class `RoomBase` for shared room behavior.
- Derived classes `StandardRoom` and `PremiumSuite`.
- A `Hotel` class to manage rooms and reservations.
- A `main()` function demonstrating usage.
*/

#include <iostream>
using namespace std;

// Struct to store a reservation date
struct Date {
    int day, month, year;

    // Overloaded equality operator to compare two dates
    bool operator==(const Date& d) const {
        return day == d.day && month == d.month && year == d.year;
    }
};

// Abstract base class for rooms
class RoomBase {
protected:
    Date* reservedDates = nullptr; // Array of reserved dates
    int count = 0; // Number of reserved dates

public:
    // Destructor to free dynamically allocated memory
    virtual ~RoomBase() {
        delete[] reservedDates;
    }

    // Check if a date is already reserved
    virtual bool isReserved(const Date* date) const {
        for (int i = 0; i < count; ++i) {
            if (*(reservedDates + i) == *date) return true;
        }
        return false;
    }

    // Reserve a date if it's not already reserved
    virtual void reserve(const Date* date) {
        if (isReserved(date)) {
            cout << "Date already reserved.\n";
            return;
        }

        // Allocate new memory and copy old dates
        Date* newDates = new Date[count + 1];
        for (int i = 0; i < count; ++i)
            *(newDates + i) = *(reservedDates + i);

        // Add the new reservation date
        *(newDates + count) = *date;

        // Replace old array with new one
        delete[] reservedDates;
        reservedDates = newDates;
        ++count;

        cout << "Reserved date: " << date->day << "/" << date->month << "/" << date->year << "\n";
    }

    // Pure virtual function to display room type
    virtual void info() const = 0;
};

// A standard room type
class StandardRoom : public RoomBase {
public:
    void info() const override {
        cout << "Standard Room\n";
    }
};

// A premium suite room type
class PremiumSuite : public RoomBase {
public:
    void info() const override {
        cout << "Premium Suite\n";
    }
};

// Class that represents the hotel and manages all rooms
class Hotel {
    RoomBase** rooms = nullptr; // Dynamic array of room pointers
    int size = 0; // Number of rooms

public:
    // Destructor to delete all rooms and free memory
    ~Hotel() {
        for (int i = 0; i < size; ++i)
            delete rooms[i];
        delete[] rooms;
    }

    // Add a new room
    void addRoom(RoomBase* room) {
        RoomBase** newRooms = new RoomBase*[size + 1];

        // Copy existing rooms
        for (int i = 0; i < size; ++i)
            newRooms[i] = rooms[i];

        // Add new room
        newRooms[size] = room;

        // Replace old array
        delete[] rooms;
        rooms = newRooms;
        ++size;
    }

    // Remove a room by ID
    void removeRoom(int id) {
        if (id < 0 || id >= size) {
            cout << "Invalid room ID\n";
            return;
        }

        delete rooms[id];

        RoomBase** newRooms = new RoomBase*[size - 1];
        for (int i = 0, j = 0; i < size; ++i) {
            if (i != id)
                newRooms[j++] = rooms[i];
        }

        delete[] rooms;
        rooms = newRooms;
        --size;
    }

    // Reserve a room by ID and date
    void reserveRoom(int id, const Date* date) {
        if (id < 0 || id >= size) {
            cout << "Invalid room ID\n";
            return;
        }

        if (!rooms[id]->isReserved(date))
            rooms[id]->reserve(date);
        else
            cout << "Date already reserved for this room.\n";
    }

    // Print info for all rooms
    void printRooms() const {
        for (int i = 0; i < size; ++i) {
            cout << "Room " << i << ": ";
            rooms[i]->info();
        }
    }
};

// Main function to demonstrate functionality
int main() {
    Hotel hotel;

    // Add two types of rooms
    hotel.addRoom(new StandardRoom());
    hotel.addRoom(new PremiumSuite());

    // Define some reservation dates
    Date d1{15, 6, 2025};
    Date d2{16, 6, 2025};

    // Display rooms
    hotel.printRooms();

    // Make some reservations
    hotel.reserveRoom(0, &d1);  // Reserve Standard Room
    hotel.reserveRoom(1, &d1);  // Reserve Premium Suite
    hotel.reserveRoom(1, &d2);  // Reserve another date
    hotel.reserveRoom(0, &d1);  // Try duplicate

    // Remove a room and show remaining rooms
    hotel.removeRoom(0);
    hotel.printRooms();

    return 0;
}
