# Restaurant Kitchen Service
​
## Table of Contents
​
- [Program description](#program-description)
- [Functional](#functional)
- [Installation](#installation)
- [Technologies](#technologies)
​
## Program description
​
The Restaurant Kitchen Service project is a web application designed to facilitate
efficient navigation and organization in a restaurant kitchen. It aims to assist kitchen staff,
such as chefs and cooks, in managing various aspects of their daily tasks and operations.
​
## Functional
- Dish Management: The project allows users to create, view, and update 
various dishes served in the kitchen. Each dish can have a name, description,
price, and associated dish type.

- Dish Types: Users can categorize dishes based on their types (e.g., appetizers,
main courses, desserts). Dish types provide better organization and 
ease of access to relevant dishes.

- Staff Management: The application enables administrators to manage kitchen
staff, including chefs and cooks, by creating user accounts with specific roles and permissions.

- Kitchen Navigation: Users can easily navigate through the application's user-friendly
interface to access dish details, dish types, and staff information.

- Search and Filter: The project includes search and filtering functionalities, allowing 
users to find specific dishes or staff members based on various criteria.

- User Authentication: Robust user authentication and authorization mechanisms ensure
that only authorized users can access and modify sensitive information.
​
## Installation
​
1. Clone the repository:

     ```angular2html
    git clone https://github.com/Gvilion/restaurant-kitchen-service
    ```   

2. Create virtual environment and activate it:
    
    ```angular2html
    python -m venv venv
    venv\Scripts\activate (on Windows)
    source venv/bin/activate (on macOS)
    ```   
    
3. Install dependencies:
   ```angular2html
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```angular2html
   python manage.py migrate
   ```
5. Create superuser:
   ```angular2html
   python manage.py createsuperuser
   ```
6. Run django server using run button or type next command to the console:
   ```angular2html
   python manage.py runserver
   ```
​
## Technologies
1. Django: Django is the core framework used for building the web application.
It provides a high-level Python web development environment with built-in features like URL routing,
ORM (Object-Relational Mapping), and authentication.

2. Python: Python is the programming language used to develop the backend logic of the web application.
Django is built on Python, making it the primary language for writing server-side code.

3. HTML/CSS: HTML (Hypertext Markup Language) and CSS (Cascading Style Sheets) are used to structure the content 
and define the presentation of the web application's user interface.

4. SQLite and PostgreSQL: Django supports multiple database backends, and my project use SQLite or PostgreSQL
to store and manage data related to dishes, dish types, and kitchen staff. SQLite is used during development
and testing, while PostgreSQL used in production environments
​
