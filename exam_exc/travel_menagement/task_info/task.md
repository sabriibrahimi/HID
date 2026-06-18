# Travel Management System

You are tasked with creating a Travel Management System. The system should display all current trips on the home page (see `index.html`). Each trip contains the following information:

- Destination (place of travel)
- Price
- Duration
- Image

The system also includes users called **Tour Guides** who can add trips. Each tour guide has the following attributes:

- First Name
- Last Name
- Contact Phone Number
- Email Address

It must be known exactly which tour guide created each trip. Only the assigned tour guide is allowed to add trips and make modifications to the trips they have created.

To better demonstrate the application, the database should initially contain at least **two tour guides** and the trips defined in the provided `index.html` page.

In addition, some customization of the Django Administration Panel is required.

## Required Admin Panel Functionalities

- Tour guides can be added, edited, and deleted **only by superusers**.
- A tour guide can manage a maximum of **5 destinations** at any given time.
- When a tour guide is deleted, all of their destinations should be randomly reassigned to the remaining tour guides.
- The total price of all destinations assigned to a single tour guide must not exceed **50,000**.
- Destinations can only be edited by the tour guide responsible for that destination. Other tour guides may only view those destinations.
- A tour guide cannot add a destination if another destination with the same name already exists.
- In the Django Admin panel, superusers should only see tour guides who have **fewer than 3 destinations** assigned to them.

## Web Application Pages

The web application consists of:

### 1. Home Page
Displays all available destinations/trips, including:

- Destination name
- Price
- Duration
- Image

### 2. Add Destination Page
Allows authorized tour guides to add a new destination to the system.

The layout and text content of the provided pages should remain unchanged unless functionality requires otherwise.

<img src="img.png">

<img src="img_1.png"> 