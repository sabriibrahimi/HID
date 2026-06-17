

# Exam Task 
## Repair shop

Create a Django application to manage a car repair shop. Each scheduled repair is
characterized by a mandatory code, date when the repair was reported, description of the repair
problem, user who reported the problem, image of the problem, information about the car to be
repaired, and workshop selected to make the repair. For each car, the type of car, the manufacturer
of the car, the maximum allowed speed and the color of the car are kept. For the workshop, its
name, year of establishment and information whether it repairs oldtimer vehicles are kept. For each
car manufacturer, information about it’s name, a link to the official website, country of origin and
name of the owner are kept.

Additionally, information for workshop is kept about the car manufacturers whose cars
they specializes in repairing. One manufacturer can cooperate with several workshops.

---

### Part 1:
Create the appropriate models to enable the system functionality.

It is necessary to enable the addition of objects through the Admin panel, with the note that
the manufacturers specialization of an workshop are added to the section for the workshop. In
addition, within the Admin panel you need to provide the following functionalities:

- When creating the repair, the user is assigned automatically according to the logged in
user
- Once a workshop is saved, it can not be changed and deleted
- Only super user can add car manufacturers
- For the manufacturers in the list only their name is displayed, and for the cars the type
and the allowed speed are displayed


---

### Part 2: 
Using the Bootstrap framework, create 2 templates to display system informations.
Respectively:
- `/index/` - display of general system information, shown in Image 1
- `/repairs/` - display of all necessary repairs created by the logged in user where the type
of car is "Sedan". In this view, there is also a form for adding a new repair, shown in
Figure 2 

---

Once you have created the system, create a .zip file for entire project with all its
accompanying elements. The database in the project remains the one defined by Django, SQLite.
Create several objects from the models to test their functionality and let them stay in the database
when attaching.

---
### `index.html`
<img src="img1.png">

---

### `repairs.html`
<img src="img2.png">

