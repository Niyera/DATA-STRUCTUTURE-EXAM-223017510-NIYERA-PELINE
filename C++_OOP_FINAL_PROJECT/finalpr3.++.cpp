#include <iostream>
using namespace std;

struct Date {
    int day, month, year;
    bool operator==(const Date& d) const {
        return day == d.day && month == d.month && year == d.year;
    }
};

class RoomBase {
protected:
    Date* reservedDates = nullptr;
    int count = 0;
public:
    virtual ~RoomBase() { delete[] reservedDates; }
    virtual bool isReserved(const Date* date) const {
        for (int i = 0; i < count; ++i) {
            if (*(reservedDates + i) == *date) return true;
        }
        return false;
    }
    virtual void reserve(const Date* date) {
        if (isReserved(date)) {
            cout << "Date already reserved.\n";
            return;
        }
        Date* newDates = new Date[count + 1];
        for (int i = 0; i < count; ++i)
            *(newDates + i) = *(reservedDates + i);
        *(newDates + count) = *date;
        delete[] reservedDates;
        reservedDates = newDates;
        ++count;
        cout << "Reserved date: " << date->day << "/" << date->month << "/" << date->year << "\n";
    }
    virtual void info() const = 0;
};

class StandardRoom : public RoomBase {
public:
    void info() const override { cout << "Standard Room\n"; }
};

class PremiumSuite : public RoomBase {
public:
    void info() const override { cout << "Premium Suite\n"; }
};

class Hotel {
    RoomBase** rooms = nullptr;
    int size = 0;
public:
    ~Hotel() {
        for (int i = 0; i < size; ++i) delete rooms[i];
        delete[] rooms;
    }
    void addRoom(RoomBase* room) {
        RoomBase** newRooms = new RoomBase*[size + 1];
        for (int i = 0; i < size; ++i) newRooms[i] = rooms[i];
        newRooms[size] = room;
        delete[] rooms;
        rooms = newRooms;
        ++size;
    }
    void removeRoom(int id) {
        if (id < 0 || id >= size) {
            cout << "Invalid room ID\n";
            return;
        }
        delete rooms[id];
        RoomBase** newRooms = new RoomBase*[size - 1];
        for (int i = 0, j = 0; i < size; ++i) {
            if (i != id) newRooms[j++] = rooms[i];
        }
        delete[] rooms;
        rooms = newRooms;
        --size;
    }
    void reserveRoom(int id, const Date* date) {
        if (id < 0 || id >= size) {
            cout << "Invalid room ID\n";
            return;
        }
        if (!rooms[id]->isReserved(date)) rooms[id]->reserve(date);
        else cout << "Date already reserved for this room.\n";
    }
    void printRooms() const {
        for (int i = 0; i < size; ++i) {
            cout << "Room " << i << ": ";
            rooms[i]->info();
        }
    }
};

int main() {
    Hotel hotel;
    hotel.addRoom(new StandardRoom());
    hotel.addRoom(new PremiumSuite());

    Date d1{15, 6, 2025};
    Date d2{16, 6, 2025};

    hotel.printRooms();
    hotel.reserveRoom(0, &d1);
    hotel.reserveRoom(1, &d1);
    hotel.reserveRoom(1, &d2);
    hotel.reserveRoom(0, &d1); // Duplicate reservation test

    hotel.removeRoom(0);
    hotel.printRooms();

    return 0;
}
