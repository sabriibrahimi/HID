# Exam Task 
## Cake Shop

You are tasked with creating a management system for a cake shop. The system on the first page should list all available cakes (see index.html). Each cake has a name, price, weight, description and picture.

The system also has users (bakers) who can add new cakes. Each of these users has a name, surname, contact phone number and email address. It is known exactly which baker added which cake. Only the baker who added the cake can make changes to it.

In order to better demonstrate the application, you should have added at least two bakers and the cakes defined on the index page.

It also requires some customization in the Django admin panel. At the same time, within the admin panel, you need to provide the following functionalities:
- Bakeries can only be added, modified and deleted by super-users.
- A baker can have a maximum of 10 cakes at a given time.
- When a baker is deleted, his cakes are randomly added to the rest of the bakeries.
- The total price of the cakes of one baker must not exceed 10,000.
- Cakes can only be modified by the bakers who added them, and other bakers can only see those cakes.
- A baker cannot add a cake if there is already a cake with the same name.
- Bakeries with less than 5 cakes are shown to super users in the Admin panel.

The web application consists of a home page, shown in the image below, which displays all available cakes and a page for adding a new cake.

---
### `index.html`
<img src="img1.jpeg">

---

### `add.html`
<img src="img2.jpeg">