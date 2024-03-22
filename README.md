Event Calendaring API
Welcome to the Event Calendaring API, built with Django 5.0.2! Our API is designed to facilitate the organization and management of events, rooms, and seating arrangements. Tailored for event planners, conference organizers, or anyone needing to manage event spaces and attendee seating, our API provides a comprehensive toolkit for room, chair, and event management.

Features
Room Management: Create, list, and manage rooms. Activate or deactivate rooms as needed.
Chair Management: Assign chairs within rooms, set chair pricing, and manage chair status (available, taken, VIP).
Event Scheduling: Schedule events, assign them to rooms, and specify chair arrangements, ensuring efficient utilization of space and resources

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8 or later
Django 5.0.2

Installation
Clone the repository:
git clone https://github.com/ByteRaider/CalendaringAPI.git

Navigate to the project directory:
cd event-calendaring-api

Install the required dependencies:
pip install -r requirements.txt

Migrate the database:
python manage.py migrate

Start the development server:
python manage.py runserver

Usage
Creating a Room
To create a room, send a POST request to /api/rooms/ with the following JSON payload:
{
  "name": "Conference Hall 1",
  "isActive": true,
  "user": "User ID"
}

Adding a Chair to a Room
To add a chair to a room, send a POST request to /api/chairs/ with the following JSON payload:
{
  "room": "Room ID",
  "chair_number": 1,
  "price": 100.00,
  "isTaken": false,
  "isVIP": false,
  "user": "User ID"
}

Scheduling an Event
To schedule an event and associate it with a room (and optionally specify chairs), send a POST request to /api/events/ with the following JSON payload:

{
  "title": "Annual Conference",
  "description": "This is the annual gathering...",
  "room": "Room ID",
  "start_time": "YYYY-MM-DD HH:MM:SS",
  "end_time": "YYYY-MM-DD HH:MM:SS",
  "user": "User ID",
  "content_type": "chair or room",
  "object_id": "ID of the chair"
}

License:
Free4All!
