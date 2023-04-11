# Voting-Site
A voting site built using flask that performs CRUD operations.


## Steps to run the application
1. Clone this repo into your local machine and open it using VS code or anyother editor of your choice.
2. Open the terminal and create a virtual environment using the command "python -m venv yourenvname".
3. Activate the virtual env created using the command "yourenvname\Scripts\activate".
4. Once activated, install all the packages using the command "pip install -r requirements.txt".
5. After all the installations, open the browser and install an application called Xampp for database management.
6. Open Xampp and start both Apache and MySQL and click on Admin of MySQL to open the database management UI.
7. Create a database named 'voting' by clicking 'new' on the left panel of the UI.
8. Once the DB is created, click import and choose the 'voting.sql' from the DB folder in this repository and click GO. Tables are created.
9. Finally, come back to VS Code and run the command "py app.py" to run the application. 
10. A link like http://127.0.0.1:5000/ will pop up in the terminal. Press Ctrl and click on the link to open it in the browser. Boom! You are on the landing page of the application.
