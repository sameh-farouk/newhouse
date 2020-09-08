# NewHouse
#### Rent / Sell Property Online

*property listing web application*

<img src="https://cdn.pixabay.com/photo/2019/09/25/14/01/house-for-sale-4503756_960_720.jpg" width="300" height="300">

a property listing web application wherein you can post free property listing online and do custom search and filtration within the listing database.

this django project contains two apps, accounts app that responsible for users authorizations operations, like signup, login, logout, reset passwords, edit profile and scocial login using facebook oAuth2 or alternatively facebook connect.

the second app is listings app, the main app that responsible for show users listings, and enable custom search and fileration of the listings to find the house that fit user needs, also registerd users can add listing for property including uploading images for the property, edit own listings or delete it. users can create favourite list.
<img src="https://github.com/sameh-farouk/newhouse/raw/master/screenshots/my_project_visualized.png" width="700">


- most of the views uses the newer classes based views.
- model signals was used.
- custom template filters was used.
- library used in front end includes bootstrap and friconix.
- fetch api in vanila javaScript used in front end to call json endpoint to togole favourite status for the listings
- third-party django-library used includes extra-views to manage multible modelform in one page, and -django-smart-select to enable group "chained" models.

<img src="https://github.com/sameh-farouk/newhouse/raw/master/screenshots/Screen%20Shot%202020-09-08%20at%202.37.38%20PM.png" width="300" height="300">

<img src="https://github.com/sameh-farouk/newhouse/raw/master/screenshots/Screen%20Shot%202020-09-08%20at%202.38.16%20PM.png" width="300" height="300">

this is WIP.
Project Kicked off: august 22, 2020

