## Morris Health Services (MHS) Application

A comprehensive Django-based web application for managing the operations of a healthcare facility, including employee, facility, patient, insurance, appointment, and reporting modules. The system is designed to streamline administrative processes, ensure data integrity, and provide actionable business insights for Morris Health Services.

---

## Features

- **Employee Management:** Add, edit, and view doctors, nurses, admin staff, and other healthcare professionals. Each employee is associated with a facility and their respective roles/subclasses.
- **Facility Management:** Manage office buildings and outpatient surgery centers, including their specific attributes (office/room count, procedure codes, etc.).
- **Patient Management:** Register, edit, and view patients, including their assigned doctors and insurance companies.
- **Insurance Management:** Add, edit, and view insurance companies linked to patients and invoices.
- **Appointment Scheduling:** Create and update appointments, ensuring no scheduling conflicts for doctors or patients.
- **Invoice Generation:** Automated invoice creation and daily aggregation, with costs linked to appointments and insurance companies.
- **Comprehensive Reporting:** Generate reports on revenue by facility/date, appointments by physician/date, best revenue days, and average daily revenue by insurance company.
- **User-Friendly UI:** HTML-based templates with clear navigation, forms, and validation for all major operations.

---

## Architecture

- **Backend:** Python Django framework, with business logic in `views.py` and modular management code in `manageEmployee.py` and `manageFacility.py`.
- **Database:** MySQL, with a normalized schema and strict integrity constraints.
- **Frontend:** HTML templates organized by functional area (`employee`, `facility`, `insurance`, `patient`, `reports`).
- **Database Access:** Custom utility layer (`db_utils.py`) for executing queries, handling transactions, and error logging.
- **URL Routing:** Defined in `urls.py`, mapping endpoints to view functions for all operations.

---

## Database Schema

The database is designed for normalization, data integrity, and extensibility. Key tables include:

- **FACILITY:** Stores facility details (address, type, max size).
- **EMPLOYEE:** Base table for all staff, with subclass tables for Doctor, Nurse, Admin Staff, and Other HCP.
- **PATIENT:** Patient demographic and relational data.
- **INSURANCE_COMPANY:** Insurance provider information.
- **MAKES_APPOINTMENT:** Tracks appointments, enforcing unique constraints to prevent double-booking.
- **INVOICE & INVOICE_DETAIL:** Handles billing, costs, and links to insurance companies.
- **OFFICE_BUILDING / OUTPATIENT_SURGERY:** Specialized facility tables.

Refer to the provided SQL `CREATE TABLE` statements for full schema details.

![image](https://github.com/user-attachments/assets/963e7d76-488a-4c45-bfcf-63f46a72893e)

![image](https://github.com/user-attachments/assets/715f6557-9286-472b-94eb-b7df5fd1d2c8)

---

## Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/sruthivellore/mhsApp.git
   cd mhsApp
   ```

2. **Configure the Database:**
   - Install MySQL and create a database named `MHS`.
   - Update `settings.py` with your local MySQL credentials:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'MHS',
             'USER': 'root',
             'PASSWORD': 'your_password',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```

3. **Initialize the Database:**
   - Run the provided SQL scripts to create tables and insert sample data.

4. **Run the Application:**
   ```bash
   python manage.py runserver
   ```
   - Access the app at `http://localhost:8000/`

---

## Usage Guide

- **Navigation:** Use the top navigation bar to access Home, Employee, Facility, Insurance, Patient, and Reports sections.
- **Forms:** Required fields are clearly marked; validation is enforced (e.g., state codes, zip codes).
- **Employee/Facility/Patient Management:** Add, view, and edit records via intuitive forms and dropdowns.
- **Appointments:** Schedule or update appointments, with automatic conflict checking.
- **Invoices:** Costs are recorded and aggregated per insurance company and day.
- **Reports:** Access various analytics and exportable summaries from the Reports tab.

---

## Key Implementation Details

- **Database Utilities:** All SQL execution is abstracted in `db_utils.py` for consistency and robust error handling.
- **Views & Routing:** Business logic is in `views.py`, with each URL pattern mapped to a specific handler in `urls.py`.
- **Templates:** Organized by entity/functionality, supporting paginated lists and forms for CRUD operations.

---

## Reporting & Analytics

- **Revenue by Facility/Date:** View total and facility-wise revenue for a selected date.
- **Appointments by Physician/Date:** List all appointments for a doctor on a specific date.
- **Appointments by Time/Facility:** Filter appointments by time range and facility.
- **Best Revenue Days:** Top five revenue-generating days for a given month/year.
- **Average Daily Revenue by Insurance:** Calculate average daily revenue per insurance company over a date range.

---

[Link to User Guide and UI snapshots](./user_guide.pdf)
