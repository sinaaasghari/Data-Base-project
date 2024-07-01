# Restaurant Database Project

## Overview

Welcome to the Restaurant Database Project! This project involves the creation and management of a database system for a restaurant. The primary objectives were to design an ER diagram, convert it into database tables, implement views, triggers, and procedures, create a logging mechanism, and finally connect the database to Streamlit for enhanced user visualization.

## Project Structure

1. **ER Diagram Creation**: 
    - We started by understanding the stakeholder requirements and created an Entity-Relationship (ER) diagram to model the restaurant's database.
  
2. **Table Conversion**:
    - The ER diagram was then converted into relational database tables, capturing all necessary entities and relationships.

3. **Views, Triggers, and Procedures**:
    - Views were added to the database to simplify data retrieval and enhance security.
    - Triggers and procedures were implemented to handle automated actions and enforce business logic.
  
4. **Logging Mechanism**:
    - A log table was created, and triggers were set up to log user activities for monitoring and auditing purposes.

5. **Streamlit Integration**:
    - The database was connected to a Streamlit application to provide a user-friendly interface for visualization and interaction.

## Getting Started

### Prerequisites

Ensure you have the following software installed on your machine:
- Python 3.1
- Streamlit
- A relational database system (SQL Server)

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/sinaaasghari/Data-Base-project.git
    cd restaurant-database
    ```
2. **Setup the Database**:
    - Create a new database in your preferred RDBMS.
    - Run the SQL scripts provided in the `database` folder to create tables, views, triggers, and procedures.

3. **Run the Application**:
    Start the Streamlit application:
    ```bash
    streamlit run run.py
    ```

## Contributors

- [Shadmehr Salehi](https://github.com/shadmehr-salehi)
- [Sina Asghari](https://github.com/sinaaasghari)
- [Foozhan Fahimzade](https://github.com/FoozhanFahimzade)

## Additional Notes

- The `database` folder contains all SQL scripts used for creating the tables, views, triggers, and procedures.
- The `app` folder includes the Streamlit application files.
- The `log` table is crucial for auditing user actions and maintaining the integrity of operations.

Feel free to fork the repository and contribute to the project. For any issues or feature requests, please open an issue on GitHub.

---

Thank you for checking out our project! We hope you find it useful and insightful.
