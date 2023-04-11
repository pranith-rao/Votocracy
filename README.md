# Vote!
This website is an online platform that allows users to vote on various topics or issues. Users can register and access a list of voting options, choose their preferred option, and submit their vote. It provides a convenient and accessible way for people to participate in democratic decision-making processes.

To have a glimpse on how this website works watch this https://www.youtube.com/watch?v=cJN9HYrEWTY

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

## Operations that can be performed
### BY USER:
1. Click on Signup from the Signup/Login dropdown list and fill the form.
2. Make sure you use a unique username and mail id as each of them can be used by only one user.Same username and mail id can't be used by two users.
3. After filling the form click on register. If all the requirements are met you will get a success alert and will be directed to the login page.Remember you need to be 18 years to register and cast your vote.
4. Enter the username and password, the ones used while registering and click on login.
5. On successfull login you will be directed to the home page.CLick on 'Candidates' on the navbar to check the candidates participating in the election. Remember you can cast your vote only once.
6. After deciding whom to vote, click on the vote button below your go-to candidate details and done.You have successfully casted your vote.
7. You even get the options to update the profile and change the password if necessary.
8. Once everything is done click the dropdown list next to your name in the navbar and click on the logout option to logout.

### BY ADMIN:
1. Click on Signup from the Admin dropdown list and fill the form.
2. Enter the secret key as "URADMIN" and make sure that a unique mail id is used as same mail id cannot be used by two admins.
3. On clicking register if all requirements are met you will be directed to the login page. Enter the details and click login.
4. On successfull login, you will be directed to the home page where you will find options to add and update candidates under the manage dropdown list, edit your profile,change password of your account and more importantly view the results of the election under the droplist list near your name.
5. In update candidate option the admin can edit the details of the candidate and delete a candidate if they decide to withdraw from the election.
6. Once everything is done click the dropdown list next to your name in the navbar and click on the logout option to logout.

## Snapshots
### Home Page
![Index Page](https://user-images.githubusercontent.com/65860350/231240171-a01f80ce-14cf-4cfe-94b0-2c321def755c.png)
![Screenshot (1839)](https://user-images.githubusercontent.com/65860350/231240189-b97a323e-5bab-4c4b-9f82-e9c59823fa54.png)
![Screenshot (1840)](https://user-images.githubusercontent.com/65860350/231240221-c57f2174-ef9a-419d-bfdd-7c9ae241a989.png)
### About Page
![Screenshot (1841)](https://user-images.githubusercontent.com/65860350/231240705-1f9e1a29-13f2-44d4-bff0-5a9b309ed22b.png)
### List of Candidates
![List of candidates](https://user-images.githubusercontent.com/65860350/231240830-95be215d-5583-4a4d-a3fc-f40c7c63ce38.png)
### User Registration & Login
![Screenshot (1842)](https://user-images.githubusercontent.com/65860350/231241690-2e6b5168-f402-4394-9442-1d01eca9fcc0.png)
![Screenshot (1843)](https://user-images.githubusercontent.com/65860350/231241708-1cb142eb-57c0-413f-a88b-bf62ac80268d.png)
### Admin Registration & Login
![Screenshot (1844)](https://user-images.githubusercontent.com/65860350/231241801-a0bc4485-0b0e-4f70-9326-ed5fbbc0178a.png)
![Screenshot (1845)](https://user-images.githubusercontent.com/65860350/231241833-9d395f02-04ac-4eed-ba14-8df14f9c2420.png)
### Admin Dashboard
#### Add Candidate
![Screenshot (1846)](https://user-images.githubusercontent.com/65860350/231243897-382bffd8-5b11-453f-ba40-bdf8bee21aff.png)
#### Manage Candidates
![Screenshot (1847)](https://user-images.githubusercontent.com/65860350/231243985-d1a5b89e-0364-437a-9424-bb6b2a710672.png)
#### Edit Candidate
![Screenshot (1849)](https://user-images.githubusercontent.com/65860350/231244066-7e96eddd-d4cb-4f16-91db-89d37582dfda.png)
#### Delete Candidate
![Screenshot (1848)](https://user-images.githubusercontent.com/65860350/231244163-3bb70ea1-c7df-493d-8fb1-cdf08ff4e744.png)
#### Results Page
![Vote Results](https://user-images.githubusercontent.com/65860350/231246220-ce499ed5-170e-4133-9752-a8e788e35d06.png)
### User Dashboard
#### Candidates to vote for
![Screenshot (1851)](https://user-images.githubusercontent.com/65860350/231245732-a925b77e-a06f-4e15-baf8-683c80bac94e.png)
#### Vote Confirmation
![Screenshot (1852)](https://user-images.githubusercontent.com/65860350/231245844-075925f1-9eca-47b3-8f4a-e4822f4ee70c.png)
#### Update Profile
![Screenshot (1853)](https://user-images.githubusercontent.com/65860350/231245927-ca59cec3-4a8d-40a0-919b-af208ac3bb01.png)
### Sweet Alert for actions confirmation
![Screenshot (1854)](https://user-images.githubusercontent.com/65860350/231246918-abc5ba9b-286a-4d17-a249-c54fd16ee1aa.png)
### Password Recovery
![Screenshot (1855)](https://user-images.githubusercontent.com/65860350/231247105-408bd23c-7451-405e-9d09-8824aa3315e8.png)
