# Expense Tracker: A Personal Finance Application 💰
This is a Flask-based web application designed to help users manage their personal finances by tracking expenses. The application allows users to register, log in, add, edit, and delete expenses. It also provides a dashboard with a summary of total expenses and a monthly breakdown. Additionally, it features a budget prediction tool using machine learning to forecast future spending.

## Features ✨
1. **User Authentication:** Secure user registration and login.
2. **CRUD for Expenses:** Easily add, view, edit, and delete your expenses.
3. **Expense Dashboard:** A overview of your spending, including total expenses and a monthly summary.
4. **Budget Prediction:** Uses a machine learning model (RandomForestRegressor) to predict your next month's budget based on historical spending.
5. **Admin Access:** A separate admin login to view all registered users.

## Technologies Used 💻
1. **Frontend:** HTML, CSS
2. **Backend:** Python, Flask
3. **Database:** MySQL
4. **Data Science:** Pandas, Scikit-learn

## How to use 🚀
By following these steps, you can obtain a copy of the project installed and running on your local computer.

### Prerequisites
1. Python 3.6 or higher
2. MySQL server running on your system

### Installation
1. Clone the repository
```sh
    git clone [https://github.com/rmall2003/Expense_Tracker.git](https://github.com/rmall2003/Expense_Tracker.git)
    cd Expense_Tracker
```
2. Create a virtual environment
```sh
    python -m venv venv
```
3. Activate the virtual environment
   - Windows:
     ```sh
     venv\Scripts\activate
     ```
   - macOS/Linux:
    ```sh
    source venv/bin/activate
    ```
    
4. Install the required packages
   ```sh
   pip install -r requirements.txt
   ```
   
5. Configure your database
   Open the app.py file and locate the following line:
   ```sh
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:<yoursqlpassword>@localhost/expense_tracker_db'
   ```
   Change <yoursqlpassword> to your actual MySQL root password.
   
6. Initialize the database:
   Create a database named expense_tracker_db in your MySQL server. The application will automatically create the necessary tables (user and expense) when you run it for the first time.
   SQL Code:
   ```sh
   CREATE DATABASE IF NOT EXISTS expense_tracker_db;
   ```
   Simply run this command in your MySQL client.
   
7. Run the Application
   ```sh
   python app.py
   ```

8. Access the application
   Open your web browser and navigate to
   ```sh
   http://127.0.0.1:5000/
   ```
## File Structure
1. **app.py:** The main Flask application file with all the routes and logic.
2. **db.py:** Initializes the SQLAlchemy database object to avoid circular imports.
3. **model.py:** Defines the User and Expense database models.
4. **forms.py:** Defines the Flask-WTF forms for registration, login, and expenses.
5. **static/:** Contains the CSS file- *style.css*.
6. **templates/:** Contains all the HTML templates for the application's pages.
7. **requirements.txt:** Lists all the Python packages required for the project.

## Snapshots
1. **Home Page:** The welcome page that introduces the Expense Tracker application.
<img width="1919" height="830" alt="image" src="https://github.com/user-attachments/assets/658860e1-84b4-4e6e-ad06-fd7cc43bc783" />

2. **User Register and Login Page:** A view of the secure registration and login forms.
<img width="1891" height="827" alt="image" src="https://github.com/user-attachments/assets/16207eeb-d957-4b86-864e-62d8e62a07cc" />
<img width="1919" height="826" alt="image" src="https://github.com/user-attachments/assets/b2f67731-d094-46b2-a97f-c0340e86269c" />

3. **Add Expense:** The form for adding a new expense, including fields for amount, description, and category.
<img width="1896" height="822" alt="image" src="https://github.com/user-attachments/assets/2ec87ad4-f2b5-4b3f-84ab-ac9d67e3df58" />

4. **Dashboard:** The main dashboard showing a summary of total expenses, monthly breakdowns, and a list of all expenses.
<img width="1919" height="826" alt="image" src="https://github.com/user-attachments/assets/f81598e1-8557-4565-b34b-cedc57e4ba35" />

5. **Predict Budget:** The page displaying the predicted budget for the next month.
<img width="1916" height="823" alt="image" src="https://github.com/user-attachments/assets/cee143b1-387f-48e8-8b27-713fec947d7f" />

6. **User Profile Page:** The profile page that shows user details.
<img width="959" height="417" alt="image" src="https://github.com/user-attachments/assets/3c982013-1cd6-4554-ae48-45b7779a4432" />

7. **Admin Login:** The separate login page for administrators.
<img width="400" height="500" alt="image" src="https://github.com/user-attachments/assets/4d0d8c3b-28f1-4761-b5aa-e57a55f9a410" />
