from django.shortcuts import redirect, render

from .manageFacility import delete_old_facility_details, get_current_facility_type, insert_office_details, insert_ops_details, update_office_details, update_ops_details

from .manageEmployee import insert_admin_staff_details, insert_doctor_details, insert_nurse_details, insert_other_hcp_details, update_employee_details
from .db_utils import execute_query
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
import datetime
from django.contrib import messages

def index(request):
    return render(request, 'intro.html')

# Employee Management Views
def view_employee(request):
    sql = "SELECT * FROM EMPLOYEE"
    employees = execute_query(sql, fetchall=True)
    
    paginator = Paginator(employees, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'employee/employee.html', {'employees': page_obj})

def view_doctor(request):
    base_sql = """
        SELECT 
            D.*,
            E.FirstName AS EmpFirstName,
            E.MiddleName AS EmpMiddleName,
            E.LastName AS EmpLastName,
            E.Street AS EmpStreet,
            E.City AS EmpCity,
            E.State AS EmpState,
            E.Zip AS EmpZip,
            E.Salary AS EmpSalary,
            E.Date_Hired AS EmpDateHired,
            E.SSN AS SSN,
            E.Fac_ID AS EmpFacilityID
        FROM 
            DOCTOR D
        INNER JOIN 
            EMPLOYEE E ON D.EmployeeID = E.EmployeeID
    """

    doctors = execute_query(base_sql, fetchall=True)
    
    paginator = Paginator(doctors, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'employee/doctor.html', {'doctors': page_obj})

def view_nurse(request):
    base_sql = """
        SELECT 
            N.*,
            E.FirstName AS EmpFirstName,
            E.MiddleName AS EmpMiddleName,
            E.LastName AS EmpLastName,
            E.Street AS EmpStreet,
            E.City AS EmpCity,
            E.State AS EmpState,
            E.Zip AS EmpZip,
            E.Salary AS EmpSalary,
            E.Date_Hired AS EmpDateHired,
            E.SSN AS SSN,
            E.Fac_ID AS EmpFacilityID
        FROM 
            NURSE N
        INNER JOIN 
            EMPLOYEE E ON N.EmployeeID = E.EmployeeID
    """

    nurses = execute_query(base_sql, fetchall=True)
    
    paginator = Paginator(nurses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'employee/nurse.html', {'nurses': page_obj})

def view_admin_staff(request):
    base_sql = """
        SELECT 
            A.*,
            E.FirstName AS EmpFirstName,
            E.MiddleName AS EmpMiddleName,
            E.LastName AS EmpLastName,
            E.Street AS EmpStreet,
            E.City AS EmpCity,
            E.State AS EmpState,
            E.Zip AS EmpZip,
            E.Salary AS EmpSalary,
            E.Date_Hired AS EmpDateHired,
            E.SSN AS SSN,
            E.Fac_ID AS EmpFacilityID
        FROM 
            ADMIN_STAFF A
        INNER JOIN 
            EMPLOYEE E ON A.EmployeeID = E.EmployeeID
    """
    admin_staff = execute_query(base_sql, fetchall=True)
    
    paginator = Paginator(admin_staff, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'employee/admin_staff.html', {'admin_staff': page_obj})

def view_hcp(request):
    base_sql = """
        SELECT 
            H.*,
            E.FirstName AS EmpFirstName,
            E.MiddleName AS EmpMiddleName,
            E.LastName AS EmpLastName,
            E.Street AS EmpStreet,
            E.City AS EmpCity,
            E.State AS EmpState,
            E.Zip AS EmpZip,
            E.Salary AS EmpSalary,
            E.Date_Hired AS EmpDateHired,
            E.SSN AS SSN,
            E.Fac_ID AS EmpFacilityID
        FROM 
            OTHER_HCP H
        INNER JOIN 
            EMPLOYEE E ON H.EmployeeID = E.EmployeeID
    """
    hcps = execute_query(base_sql, fetchall=True)
    
    paginator = Paginator(hcps, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'employee/hcp.html', {'other_hcp': page_obj})

def add_employee(request):
    if request.method == 'POST':
        ssn = request.POST.get('ssn')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        salary = request.POST.get('salary')
        date_hired = request.POST.get('date_hired')
        job_class = request.POST.get('job_class')
        facility_id = request.POST.get('facility_id')

        # Inserting into EMPLOYEE table
        employee_sql = """
        INSERT INTO EMPLOYEE (SSN, FirstName, MiddleName, LastName, Street, City, State, Zip, Salary, Date_Hired, Job_Class, Fac_ID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        employee_params = (ssn, first_name, middle_name, last_name, street, city, state, zip_code, salary, date_hired, job_class, facility_id)
        result = execute_query(employee_sql, params=employee_params, insert_new=True)
        print(result)
        if result == "Error":
            messages.error(request, 'Error inserting employee. Please try again.')
        else:
            employee_id = result
            # Inserting into specific table based on job class
            kwargs = {}
            if job_class == 'Doctor':
                kwargs['speciality'] = request.POST.get('speciality')
                kwargs['board_certification_date'] = request.POST.get('board_certification_date')
                result = insert_doctor_details(employee_id, **kwargs)
            elif job_class == 'Nurse':
                kwargs['certification'] = request.POST.get('certification')
                result = insert_nurse_details(employee_id, **kwargs)
            elif job_class == 'HCP':
                kwargs['practice_area'] = request.POST.get('practice_area')
                result = insert_other_hcp_details(employee_id, **kwargs)
            elif job_class == 'Admin':
                kwargs['job_title'] = request.POST.get('job_title')
                result = insert_admin_staff_details(employee_id, **kwargs)                

            if  result != "Error" :
                messages.success(request, 'Employee details inserted successfully.')
            else:
                messages.error(request, 'Error inserting employee proffesion. Please try again.')
        return redirect('add_employee')

    # Fetching facility IDs for dropdown
    facility_sql = "SELECT Facility_ID FROM FACILITY"
    facilities = execute_query(facility_sql, fetchall=True)
    return render(request, 'employee/add_employee.html', {'facilities': facilities})

def edit_employee(request):

    if request.method == 'POST':
        # Retrieve form data
        employee_id = request.POST.get('employee_id')
        ssn = request.POST.get('ssn')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        salary = request.POST.get('salary')
        date_hired = request.POST.get('date_hired')
        job_class = request.POST.get('job_class')
        
        # Construct kwargs based on job class
        kwargs = {}
        if job_class == 'Doctor':
            kwargs['speciality'] = request.POST.get('speciality')
            kwargs['board_certification_date'] = request.POST.get('board_certification_date')
        elif job_class == 'Nurse':
            kwargs['certification'] = request.POST.get('certification')
        elif job_class == 'HCP':
            kwargs['practice_area'] = request.POST.get('practice_area')
        elif job_class == 'Admin':
            kwargs['job_title'] = request.POST.get('job_title')

        result = update_employee_details(employee_id, job_class, **kwargs)
        
        if result != "Error":
            employee_sql = """
            UPDATE EMPLOYEE 
            SET SSN = %s, FirstName = %s, MiddleName = %s, LastName = %s, Street = %s, City = %s, State = %s, Zip = %s, Salary = %s, Date_Hired = %s, Job_Class = %s
            WHERE EmployeeID = %s
            """
            employee_params = (ssn, first_name, middle_name, last_name, street, city, state, zip_code, salary, date_hired, job_class, employee_id)
            result = execute_query(employee_sql, params=employee_params)
            
        if result != "Error":
            messages.success(request, 'Employee details updated successfully.')
        else:
            messages.error(request, 'Error updating employee details. Please try again.')

        return redirect('edit_employee')
    
    sql = "SELECT * FROM EMPLOYEE"
    employees = execute_query(sql, fetchall=True)
    employee_id = request.GET.get('employeeIdDropdown')
    if employee_id:
        emp = get_employee_details(employee_id)
        facility_sql = "SELECT Facility_ID FROM FACILITY"
        facilities = execute_query(facility_sql, fetchall=True)
        return render(request, 'employee/edit_employee.html', {'employee_details': emp, 'employees': employees, 'facilities': facilities})
    return render(request, 'employee/edit_employee.html', {'employees': employees})

def get_employee_details(employee_id):
        employee_query = """
        SELECT * FROM EMPLOYEE WHERE EmployeeID = %s
        """
        employee_data = execute_query(employee_query, [employee_id], fetchone=True)

        if employee_data:
            # Determine the job class of the employee
            job_class = employee_data['Job_Class']

            # Fetch additional details based on job class
            if job_class == 'Doctor':
                details_query = """
                SELECT Speciality, Board_Certification_Date FROM DOCTOR WHERE EmployeeID = %s
                """
            elif job_class == 'Nurse':
                details_query = """
                SELECT Certification FROM NURSE WHERE EmployeeID = %s
                """
            elif job_class == 'HCP':
                details_query = """
                SELECT Practice_Area FROM OTHER_HCP WHERE EmployeeID = %s
                """
            elif job_class == 'Admin':
                details_query = """
                SELECT Job_Title FROM ADMIN_STAFF WHERE EmployeeID = %s
                """

            additional_details = execute_query(details_query, [employee_id], fetchone=True)

            # Merge employee data with additional details
            employee_data.update(additional_details)

            return employee_data

def view_facility(request):
    sql = "SELECT * FROM FACILITY"
    facilities = execute_query(sql, fetchall=True)
    paginator = Paginator(facilities, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'facility/facility.html', {'facilities': page_obj})

def view_ob(request):
    sql = """
    SELECT f.*, ob.Office_Count 
    FROM FACILITY f 
    JOIN OFFICE_BUILDING ob ON f.Facility_ID = ob.Facility_ID
    """
    facilities = execute_query(sql, fetchall=True)
    paginator = Paginator(facilities, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'facility/office_building.html', {'facilities': page_obj})

def view_ops(request):
    sql = """
    SELECT f.*, ops.Room_Count, ops.Procedure_Code, ops.Description
    FROM FACILITY f 
    JOIN OUTPATIENT_SURGERY ops ON f.Facility_ID = ops.Facility_ID
    """
    facilities = execute_query(sql, fetchall=True)
    paginator = Paginator(facilities, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'facility/ops.html', {'facilities': page_obj})

def edit_facility(request):
    if request.method == 'POST':
        try:
            # Retrieve form data
            facility_id = request.POST.get('facility_id')
            street = request.POST.get('street')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip_code = request.POST.get('zip')
            facility_type = request.POST.get('facility_type')
            max_size = request.POST.get('size')
            facility_type = facility_type.replace("_", " ")

            # Check if facility type has changed
            current_facility_type = get_current_facility_type(facility_id)
            if current_facility_type != facility_type:
                # Delete old entry from the specific table based on the current facility type
                delete_old_facility_details(facility_id, current_facility_type)
                
                # Insert new entry into the updated specific table based on the new facility type
                if facility_type == 'Office':
                    office_count = request.POST.get('office_count')
                    result = insert_office_details(facility_id, office_count)
                elif facility_type == 'OP Surgery':
                    room_count = request.POST.get('room_count')
                    procedure_code = request.POST.get('procedure_code')
                    description = request.POST.get('description')
                    result = insert_ops_details(facility_id, room_count, procedure_code, description)
            else:
                # Update existing entry in the specific table based on the facility type
                if facility_type == 'Office':
                    office_count = request.POST.get('office_count')
                    result = update_office_details(facility_id, office_count)
                elif facility_type == 'OP Surgery':
                    room_count = request.POST.get('room_count')
                    procedure_code = request.POST.get('procedure_code')
                    description = request.POST.get('description')
                    result = update_ops_details(facility_id, room_count, procedure_code, description)

            if result != "Error":
                # Update FACILITY table
                facility_sql = """
                UPDATE FACILITY
                SET Street = %s, City = %s, State = %s, Zip = %s, Facility_Type = %s, MaxSize = %s
                WHERE Facility_ID = %s
                """
                facility_params = (street, city, state, zip_code, facility_type, max_size, facility_id)
                result = execute_query(facility_sql, params=facility_params)

            if result != "Error":
                messages.success(request, 'Facility details updated successfully.')
            else:
                messages.error(request, 'Error updating facility details. Please try again.')

            return redirect('edit_facility')
        except Exception as e:
            messages.error(request, f'Error updating facility details: {str(e)}')
            return redirect('edit_facility')

    # Retrieve all facilities to display in a dropdown for editing
    sql = "SELECT * FROM FACILITY"
    facilities = execute_query(sql, fetchall=True)
    facility_id = request.GET.get('facilityDropdown')
    if facility_id:
        facility_details = get_facility_details(facility_id)
        return render(request, 'facility/edit_facility.html', {'facility_details': facility_details, 'facilities': facilities})
    
    return render(request, 'facility/edit_facility.html', {'facilities': facilities})

def get_facility_details(facility_id):
    # First, get the facility type
    type_sql = "SELECT Facility_Type FROM FACILITY WHERE Facility_ID = %s"
    facility_type = execute_query(type_sql, params=(facility_id,), fetchone=True)

    if facility_type['Facility_Type'] == 'OP Surgery':
        # Query details for outpatient surgery
        sql = """
        SELECT f.*, ops.Room_Count, ops.Procedure_Code, ops.Description
        FROM FACILITY f
        LEFT JOIN OUTPATIENT_SURGERY ops ON f.Facility_ID = ops.Facility_ID
        WHERE f.Facility_ID = %s
        """
    else:
        # Query details for office building
        sql = """
        SELECT f.*, ob.Office_Count
        FROM FACILITY f
        LEFT JOIN OFFICE_BUILDING ob ON f.Facility_ID = ob.Facility_ID
        WHERE f.Facility_ID = %s
        """

    facility_details = execute_query(sql, params=(facility_id,), fetchone=True)
    return facility_details

def create_facility(request):
    if request.method == 'POST':
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        size = request.POST.get('size')
        facility_type = request.POST.get('facility_type')
        facility_type = facility_type.replace("_", " ")
        sql_insert_facility = """
        INSERT INTO FACILITY (Street, City, State, Zip, MaxSize, Facility_Type)
        VALUES (%s, %s, %s, %s, %s,  %s)
        """
        facility_id = execute_query(sql_insert_facility, (street, city, state, zip_code, size, facility_type), insert_new = True)
        result = "Success"
        if facility_type == 'Office':
            office_count = request.POST.get('office_count')
            result = insert_office_details(facility_id, office_count)
        elif facility_type == 'OP Surgery':
            room_count = request.POST.get('room_count')
            procedure_code = request.POST.get('procedure_code')
            description = request.POST.get('description')
            result = insert_ops_details(facility_id, room_count, procedure_code, description)

        if result != "Error":
            messages.success(request, 'Facility Created Successfully.')
        else:
            messages.error(request, 'Error while creating Facility. Please try again.')
        # Redirect to a new URL after POST
        return redirect('create_facility') 
    return render(request, 'facility/add_facility.html')

def view_insurance(request):
    sql = "SELECT * FROM INSURANCE_COMPANY"
    insurance_companies = execute_query(sql, fetchall=True)
    paginator = Paginator(insurance_companies, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'insurance/view_insurance.html', {'insurance_companies': page_obj})

def add_insurance(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        sql_add_insurance = """
        INSERT INTO INSURANCE_COMPANY (Name, Street, City, State, Zip)
        VALUES (%s, %s, %s, %s, %s)
        """
        result = execute_query(sql_add_insurance, (name, street, city, state, zip_code))
        if result != "Error":
            messages.success(request, 'Insurance Company Registed Successfully.')
        else:
            messages.error(request, 'Error while creating Insurance Company. Please try again.')
        return redirect('add_insurance')
    return render(request, 'insurance/add_insurance.html')

def edit_insurance(request):
    if request.method == 'POST':
        insurance_id = request.POST.get('insurance_id')
        name = request.POST.get('name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        sql_edit_insurance = """
        UPDATE INSURANCE_COMPANY
        SET Name = %s, Street = %s, City = %s, State = %s, Zip = %s
        WHERE InsuranceComp_ID = %s
        """
        param = (name, street, city, state, zip_code, insurance_id)
        result = execute_query(sql_edit_insurance, params=param)
        if result != "Error":
            messages.success(request, 'Insurance Company Details Updated Successfully.')
        else:
            messages.error(request, 'Error while updating Insurance Company Details. Please try again.')
        return redirect('edit_insurance')
    sql = "SELECT * FROM INSURANCE_COMPANY"
    insurance_companies = execute_query(sql, fetchall=True)
    #print("VIEWs.py FETCHED? ",len(insurance_companies))
    insurance_id = request.GET.get('insuranceDropdown')
    #print("VIEWs.py INSURANCE ID::",insurance_id)
    if insurance_id:
        insurance_details = get_insurance_details(insurance_id)
        return render(request, 'insurance/edit_insurance.html', {'insurance_details': insurance_details, 'insurance_companies': insurance_companies})
    return render(request, 'insurance/edit_insurance.html', {'insurance_companies': insurance_companies})

def get_insurance_details(insurance_id):
    #print("VIEWS.py COMPANY :: ",insurance_id)
    sql = """
    SELECT * FROM INSURANCE_COMPANY WHERE InsuranceComp_ID = %s
    """
    #print("SQL is ",sql)
    insurance_details = execute_query(sql, (insurance_id), fetchone=True)
    #print('Insurance Details ',insurance_details)
    return insurance_details

def view_patient(request):
    sql = "SELECT * FROM PATIENT"
    patients = execute_query(sql, fetchall=True)
    paginator = Paginator(patients, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'patient/patient.html', {'patients': page_obj})

def add_patient(request):
    doctors_sql = """
                    SELECT d.EmployeeID, e.FirstName, e.LastName
                    FROM DOCTOR d
                    JOIN EMPLOYEE e ON d.EmployeeID = e.EmployeeID 
                """
    doctors = execute_query(doctors_sql, fetchall=True)

    insurances_sql = "SELECT InsuranceComp_ID, Name FROM INSURANCE_COMPANY"
    insurances = execute_query(insurances_sql, fetchall=True)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST['last_name']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']
        first_visit_date = request.POST['first_visit_date']
        doctor_id = request.POST['doctor_id']
        incomp_id = request.POST['incomp_id']
        
        insert_patient_sql = """
        INSERT INTO PATIENT (FirstName, MiddleName, LastName, Street, City, State, Zip, First_Visit_Date, Doctor_ID, InComp_ID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        patient_params = (first_name, middle_name, last_name, street, city, state, zip_code, first_visit_date, doctor_id, incomp_id)
        result = execute_query(insert_patient_sql, patient_params)
        if result != "Error":
            messages.success(request, 'Patient Registed Successfully.')
        else:
            messages.error(request, 'Error while creating Patient. Please try again.')
        return redirect('add_patient')
    return render(request, 'patient/add_patient.html', {'doctors': doctors, 'insurances': insurances})

def edit_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        first_visit_date = request.POST.get('first_visit_date')
        doctor_id = request.POST.get('doctorIdDropdown')
        incomp_id = request.POST.get('insuranceDropdown')
        sql = """
        UPDATE PATIENT
        SET FirstName = %s, MiddleName = %s, LastName = %s, Street = %s, City = %s, State = %s, Zip = %s, First_Visit_Date = %s, Doctor_ID = %s, InComp_ID = %s
        WHERE Patient_ID = %s
        """
        params = (first_name, middle_name, last_name, street, city, state, zip_code, first_visit_date, doctor_id, incomp_id, patient_id)
        result = execute_query(sql, params)
        if result != "Error":
            messages.success(request, 'Patient Details Updated Successfully.')
        else:
            messages.error(request, 'Error while updating Patient Details. Please try again.')
        return redirect('edit_patient')
    patients_sql = "SELECT Patient_ID FROM PATIENT"
    patients = execute_query(patients_sql, fetchall=True)
    patient_id = request.GET.get('patientIdDropdown')
    if patient_id:
        patient_details = get_patient_details(patient_id)
        doctors_sql = """
                    SELECT d.EmployeeID, e.FirstName, e.LastName
                    FROM DOCTOR d
                    JOIN EMPLOYEE e ON d.EmployeeID = e.EmployeeID 
                """
        doctors = execute_query(doctors_sql, fetchall=True)
        insurances_sql = "SELECT InsuranceComp_ID, Name FROM INSURANCE_COMPANY"
        insurances = execute_query(insurances_sql, fetchall=True)
        return render(request, 'patient/edit_patient.html', {'patients': patients, 'patient_details': patient_details, 'doctors': doctors, 'insurances': insurances})
    return render(request, 'patient/edit_patient.html', {'patients': patients})

def get_patient_details(patient_id):
    sql = """
    SELECT * FROM PATIENT WHERE Patient_ID = %s
    """
    patient_details = execute_query(sql, [patient_id], fetchone=True)
    return patient_details


def view_appointment(request):

    sql = """
        SELECT
        P.Patient_ID,
        CONCAT(P.FirstName, ' ', P.LastName) AS Patient_Name,
        CONCAT(E.FirstName, ' ', E.LastName) AS Doctor_Name,
        MA.Fac_ID AS Facility_ID,
        MA.Reason AS Reason,
        MA.Date_Time AS Appointment_Date_Time,
        CASE
            WHEN ID.Cost IS NULL THEN 'None'
            ELSE ID.Cost
        END AS Appointment_Cost,
        CASE
            WHEN ID.Cost IS NULL THEN 'Pending'
            ELSE 'Completed'
        END AS Status
    FROM
        MAKES_APPOINTMENT MA
    INNER JOIN
        DOCTOR D ON MA.Doc_ID = D.EmployeeID
    INNER JOIN
        EMPLOYEE E ON D.EmployeeID = E.EmployeeID
    INNER JOIN
        PATIENT P ON MA.Pat_ID = P.Patient_ID
    LEFT JOIN
        INVOICE_DETAIL ID ON MA.InD_ID = ID.InvDetailID
    ORDER BY
        MA.Date_Time DESC;
        """
    apps = execute_query(sql, fetchall=True)
    paginator = Paginator(apps, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'patient/appointments.html', {'patients': page_obj})

def make_appointment(request):
    if request.method == 'POST':
        patient_id = request.POST['patient_id']
        doctor_id = request.POST['doctor_id']
        appointment_date = request.POST['appointment_date']
        appointment_time = request.POST['appointment_time']
        facility_id = request.POST['facility_id']
        reason = request.POST['reason']
        datetime = f"{appointment_date} {appointment_time}:00"
        invD_ID = None
        insert_appointment_sql = """
        INSERT INTO MAKES_APPOINTMENT (Pat_ID, Doc_ID, Date_Time, Fac_ID, InD_ID, Reason)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        appointment_params = (patient_id, doctor_id, datetime, facility_id, invD_ID, reason)
        result = execute_query(insert_appointment_sql, appointment_params, insert_new=True)
        if result != "Error":
            messages.success(request, 'Appointment Created Successfully.')
        else:
            messages.error(request, 'Error while creating appointment due to conflicts. Please try again.')
        return redirect('make_appointment')
    patients_sql = "SELECT Patient_ID FROM PATIENT"
    patients = execute_query(patients_sql, fetchall=True)
    doctors_sql = "SELECT EmployeeID FROM DOCTOR"
    doctors = execute_query(doctors_sql, fetchall=True)
    facilities_sql = "SELECT Facility_ID FROM FACILITY"
    facilities = execute_query(facilities_sql, fetchall=True)
    return render(request, 'patient/make_appointment.html', {'patients': patients, 'doctors': doctors, 'facilities': facilities})

def update_appointment(request):
    if request.method == 'POST':
            cost = request.POST['cost']
            patient_id = request.POST['patient_id']
            doctor_id = request.POST['doctor_id']
            facility_id = request.POST['facility_id']
            reason = request.POST['reason']
            appointment_date = request.POST['appointment_date']
            appointment_time = request.POST['appointment_time']
            datetime = f"{appointment_date} {appointment_time}:00"

            #old Values
            opatient_id = request.POST['opatient_id']
            odoctor_id = request.POST['odoctor_id']
            ofacility_id = request.POST['ofacility_id']
            oappointment_date = request.POST['oappointment_date']
            oappointment_time = request.POST['oappointment_time']
            odatetime = f"{oappointment_date} {oappointment_time}:00"

            ind_id = None            

            if cost: 
                insuranceComp_sql = """
                SELECT InComp_ID FROM PATIENT WHERE Patient_ID = %s
                """
                incomp_id = execute_query(insuranceComp_sql, [patient_id], fetchone=True)
                incomp_id = incomp_id['InComp_ID']
                
                getInvoiceID = """
                SELECT Inv_ID FROM INVOICE
                WHERE InComp_ID = %s and InvDate = %s
                """
                invoice_id = execute_query(getInvoiceID, (incomp_id, appointment_date), fetchone=True)
                invoiceId = invoice_id['Inv_ID'] if invoice_id else None
                if invoiceId is None:
                    insert_invoice_sql = """
                    INSERT INTO INVOICE (InvDate, InComp_ID)
                    VALUES (%s, %s)
                    """
                    latest_invoice_id = execute_query(insert_invoice_sql, (appointment_date, incomp_id), insert_new=True)
                    invoiceId = latest_invoice_id

                insert_invoice_details_sql = """
                INSERT INTO INVOICE_DETAIL (Inv_ID, Cost)
                VALUES (%s, %s)
                """
                ind_id = execute_query(insert_invoice_details_sql, (invoiceId, cost), insert_new=True)
            
            update_appointment_sql = """
            UPDATE MAKES_APPOINTMENT 
            SET InD_ID = %s, Reason = %s, Pat_ID = %s, Doc_ID = %s, Date_Time = %s, Fac_ID = %s
            WHERE Pat_ID = %s AND Doc_ID = %s AND Date_Time = %s AND Fac_ID = %s
            """
            appointment_params = (ind_id, reason, patient_id, doctor_id, datetime, facility_id, opatient_id, odoctor_id, odatetime, ofacility_id)
            result = execute_query(update_appointment_sql, appointment_params)
            if result != "Error":
                messages.success(request, 'Appointment Details Updated Successfully.')
            else:
                messages.error(request, 'Error while updating appointment details due to conflict. Please try again.')
            return redirect('update_appointment')
    
    patients_sql = "SELECT Patient_ID FROM PATIENT"
    patients = execute_query(patients_sql, fetchall=True)
    doctors_sql = "SELECT EmployeeID FROM DOCTOR"
    doctors = execute_query(doctors_sql, fetchall=True)
    facilities_sql = "SELECT Facility_ID FROM FACILITY"
    facilities = execute_query(facilities_sql, fetchall=True)
    
    patient_id = request.GET.get('patient_id')
    doctor_id = request.GET.get('doctor_id')
    facility_id = request.GET.get('facility_id')
    appointment_date = request.GET.get('appointment_date')
    appointment_time = request.GET.get('appointment_time')
    appointment_datetime = f"{appointment_date} {appointment_time}:00"
    if patient_id and doctor_id and facility_id and appointment_date and appointment_time:
        appointment_sql = """
            SELECT * FROM MAKES_APPOINTMENT
            WHERE Pat_ID = %s AND Doc_ID = %s AND Date_Time = %s AND Fac_ID = %s
        """
        appointment = execute_query(appointment_sql, (patient_id, doctor_id, appointment_datetime, facility_id), fetchone=True)

        if (appointment):
            Date_time = appointment['Date_Time']
            appointment['appointment_date_str'] = Date_time.strftime('%Y-%m-%d')
            appointment['appointment_time_str'] = Date_time.strftime('%H:%M')
            if(appointment['InD_ID'] is None):
                return render(request, 'patient/update_appointment.html', {'patients': patients, 'doctors': doctors, 'facilities': facilities, 'appointment': appointment})
            else:
                return render(request, 'patient/update_appointment.html', {'patients': patients, 'doctors': doctors, 'facilities': facilities, 'appointment': appointment, 'hascost': True})
    return render(request, 'patient/update_appointment.html', {'patients': patients, 'doctors': doctors, 'facilities': facilities})

def daily_inv(request):
    sql = """
            SELECT p.`Patient_ID`, p.`FirstName`, i.`InvDate`, ic.`Name`, SUM(id.`Cost`) AS 'TotalCost'
            FROM `PATIENT` p
            JOIN `MAKES_APPOINTMENT` ma ON p.`Patient_ID` = ma.`Pat_ID`
            JOIN `INVOICE_DETAIL` id ON ma.`InD_ID` = id.`InvDetailID`
            JOIN `INVOICE` i ON id.`Inv_ID` = i.`Inv_ID`
            JOIN `INSURANCE_COMPANY` ic ON p.`InComp_ID` = ic.`InsuranceComp_ID`
            GROUP BY i.`InvDate`, ic.`Name`, p.`Patient_ID`
            ORDER BY i.`InvDate` DESC
        """
    costs = execute_query(sql, fetchall=True)
    paginator = Paginator(costs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'patient/daily_inv.html', {'costs': page_obj})

def revenue_report_by_facility(request):
    selected_date = request.GET.get('selected_date')
    if (request.method == 'GET' and selected_date):
        sql = """
        SELECT
            SUM(INVOICE_DETAIL.Cost) AS Total_Revenue
        FROM
            MAKES_APPOINTMENT
            INNER JOIN INVOICE_DETAIL ON MAKES_APPOINTMENT.InD_ID = INVOICE_DETAIL.InvDetailID
        WHERE
            DATE(MAKES_APPOINTMENT.Date_Time) = %s
        """
        total_revenue = execute_query(sql, params=(selected_date,), fetchone=True)['Total_Revenue']        
        sql = """
        SELECT
            FACILITY.Facility_ID,
            FACILITY.City,
            FACILITY.State,
            SUM(INVOICE_DETAIL.Cost) AS Total_Revenue
        FROM
            MAKES_APPOINTMENT
            INNER JOIN INVOICE_DETAIL ON MAKES_APPOINTMENT.InD_ID = INVOICE_DETAIL.InvDetailID
            INNER JOIN FACILITY ON MAKES_APPOINTMENT.Fac_ID = FACILITY.Facility_ID
        WHERE
            DATE(MAKES_APPOINTMENT.Date_Time) = %s
        GROUP BY
            FACILITY.Facility_ID,
            FACILITY.City,
            FACILITY.State
        """
        revenue_by_facility = execute_query(sql, params=(selected_date,), fetchall=True)
        paginator = Paginator(revenue_by_facility, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'reports/reports1.html', {'revenue_by_facility': page_obj, 'selected_date': selected_date, 'total_revenue': total_revenue})

    return render(request, 'reports/reports1.html')

def appointments_by_date_and_physician(request):
    # Fetch physician IDs for dropdown
    physician_sql = "SELECT EmployeeID FROM Employee WHERE Job_Class IN ('Doctor')"
    physicians = execute_query(physician_sql, fetchall=True)
    selected_date = request.GET.get('selected_date')
    if request.method == 'GET' and selected_date:
        physician_id = request.GET.get('physician_id')
        sql0 = """
        SELECT
            EMPLOYEE.EmployeeID,
            CONCAT(EMPLOYEE.FirstName, ' ', EMPLOYEE.LastName) AS Employee_Name,
            CASE
                WHEN EMPLOYEE.Job_Class = 'Doctor' THEN DOCTOR.Speciality
                WHEN EMPLOYEE.Job_Class = 'HCP' THEN OTHER_HCP.Practice_Area
            END AS Job_Specific_Details,
            CASE
                WHEN EMPLOYEE.Job_Class = 'Doctor' THEN DOCTOR.Board_Certification_Date
                WHEN EMPLOYEE.Job_Class = 'HCP' THEN NULL
            END AS Certification_Date
        FROM
            EMPLOYEE
            LEFT JOIN DOCTOR ON EMPLOYEE.EmployeeID = DOCTOR.EmployeeID
            LEFT JOIN OTHER_HCP ON EMPLOYEE.EmployeeID = OTHER_HCP.EmployeeID
        WHERE
        EMPLOYEE.EmployeeID = %s"""
        doc_details = execute_query(sql0, [physician_id], fetchone=True)

        sql = """
            SELECT
            MAKES_APPOINTMENT.*,
            PATIENT.FirstName AS Patient_FirstName,
            PATIENT.LastName AS Patient_LastName,
            CONCAT(FACILITY.Street, ', ', FACILITY.City, ', ', FACILITY.State, ' ', FACILITY.Zip) AS Facility_Address,
            CASE
                WHEN MAKES_APPOINTMENT.InD_ID IS NOT NULL THEN 'Completed'
                ELSE 'Pending'
            END AS Status
        FROM
            MAKES_APPOINTMENT
            INNER JOIN PATIENT ON MAKES_APPOINTMENT.Pat_ID = PATIENT.Patient_ID
            INNER JOIN FACILITY ON MAKES_APPOINTMENT.Fac_ID = FACILITY.Facility_ID
        WHERE
            DATE(MAKES_APPOINTMENT.Date_Time) = %s
            AND MAKES_APPOINTMENT.Doc_ID = %s

        """
        appointments = execute_query(sql, params=(selected_date, physician_id), fetchall=True)
        paginator = Paginator(appointments, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'reports/reports2.html', {'physician': doc_details, 'appointments': page_obj, 'employees': physicians, 'selected_date': selected_date})

    return render(request, 'reports/reports2.html', {'employees': physicians})

def appointments_by_time_period_and_facility(request):
    # Fetch facility IDs for dropdown
    facility_sql = "SELECT Facility_ID FROM FACILITY"
    facilities = execute_query(facility_sql, fetchall=True)
    selected_start_date = request.GET.get('selected_start_date')
    selected_end_date = request.GET.get('selected_end_date')
    selected_facility_id = request.GET.get('selected_facility_id')
    if request.method == 'GET' and selected_start_date and selected_end_date and selected_facility_id:
        sql = """
        SELECT DATE(ma.Date_Time) as Date, TIME(ma.Date_Time) as Time,  d.EmployeeID as Doctor_ID, e.FirstName as Doctor, p.Patient_ID as Patient_ID, p.FirstName as Patient, ma.Reason as Description
        FROM MAKES_APPOINTMENT ma 
        JOIN DOCTOR d ON ma.Doc_ID = d.EmployeeID
        JOIN EMPLOYEE e ON d.EmployeeID = e.EmployeeID
        JOIN PATIENT p ON ma.Pat_ID = p.Patient_ID
        JOIN FACILITY f ON ma.Fac_ID = f.Facility_ID
        WHERE (ma.Date_Time BETWEEN %s AND %s) AND f.Facility_ID = %s
        """
        appointments = execute_query(sql, params=(selected_start_date, selected_end_date, selected_facility_id), fetchall=True)
        paginator = Paginator(appointments, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'reports/reports3.html', {'appointments': page_obj, 'facilities': facilities, 'selected_start_date':selected_start_date, 'selected_end_date':selected_end_date, 'selected_facility_id':selected_facility_id})

    return render(request, 'reports/reports3.html', {'facilities': facilities})

def best_revenue_days_for_month(request):
    selected_month = request.GET.get('selected_month')
    selected_year = request.GET.get('selected_year')
    print('selected_month', selected_month)
    print('selected_year', selected_year)
    if request.method == 'GET' and selected_month and selected_year:
        print('selected_month', selected_month)
        print('selected_year', selected_year)
        sql = """
        SELECT SUM(inv.`Total_Cost`) as Total_Revenue, inv.`InvDate` as InvDate
        FROM `INVOICE` inv
        WHERE YEAR(inv.`InvDate`) = %s and MONTH(inv.`InvDate`) = %s
        GROUP BY inv.`InvDate`
        ORDER BY Total_Revenue DESC
        LIMIT 5
        """
        best_days = execute_query(sql, params=(selected_year,selected_month,), fetchall=True)
        return render(request, 'reports/reports4.html', {'best_days': best_days, 'selected_month':selected_month,'selected_year':selected_year})
    return render(request, 'reports/reports4.html')

def average_daily_revenue_by_insurance_company(request):
    selected_start_date = request.GET.get('selected_start_date')
    selected_end_date = request.GET.get('selected_end_date')
    if request.method == 'GET' and selected_start_date and selected_end_date:
        print('selected_start_date', selected_start_date)
        print('selected_end_date', selected_end_date)
        number_of_days = (datetime.datetime.strptime(selected_end_date, '%Y-%m-%d') - datetime.datetime.strptime(selected_start_date, '%Y-%m-%d')).days + 1

        sql = """
            SELECT ic.Name as Name, SUM(inv.Total_Cost) / %s as Average_Cost 
            FROM INVOICE inv
            JOIN INSURANCE_COMPANY ic ON inv.InComp_ID = ic.InsuranceComp_ID
            WHERE inv.InvDate BETWEEN %s AND %s 
            GROUP BY inv.InComp_ID;
        """
        average_daily_revenue = execute_query(sql, params=(number_of_days, selected_start_date, selected_end_date), fetchall=True)
        paginator = Paginator(average_daily_revenue, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'reports/reports5.html', {'average_revenue': page_obj, 'selected_start_date': selected_start_date, 'selected_end_date': selected_end_date})

    return render(request, 'reports/reports5.html')



