import requests
import base64
import json
import pyodbc

# API endpoints
BASE_URL = "https://tna.comarch.com"
OAUTH_URL = f"{BASE_URL}/api/oauth/token"
EMPLOYEES_URL = f"{BASE_URL}/api/v2/users"
REPORT_URL_TEMPLATE = f"{BASE_URL}/api/v2/reports/users/{{user_hash}}"

def get_token():
    """Obtain an OAuth 2.0 access token using client credentials."""
    auth_str = f"{IDENTYFIKATOR_KLUCZA}:{KLUCZ}"
    b64_auth_str = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {b64_auth_str}"
    }
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(OAUTH_URL, headers=headers, data=data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("Access token obtained successfully.")
        return token
    else:
        raise Exception(f"Error obtaining token: {response.status_code} {response.text}")

def get_employees(token):
    """Retrieve the list of employees."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(EMPLOYEES_URL, headers=headers)
    if response.status_code == 200:
        employees = response.json()
        print(f"Retrieved {len(employees)} employees.")
        return employees
    else:
        raise Exception(f"Error retrieving employees: {response.status_code} {response.text}")

def get_employee_report(token, user_hash, from_date, till_date):
    """Retrieve the attendance report for a specific employee."""
    url = REPORT_URL_TEMPLATE.format(user_hash=user_hash)
    params = {"fromDate": from_date, "tillDate": till_date}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error retrieving report for {user_hash}: {response.status_code} {response.text}")

def format_time(time_str):
    """Format the time string (e.g., remove seconds if desired).
       Here, we assume the time is in HH:MM:SS and we return HH:MM.
    """
    if time_str and len(time_str.split(":")) >= 2:
        parts = time_str.split(":")
        return f"{parts[0]}:{parts[1]}"
    return time_str

def main():
    try:
        # Step 1: Get OAuth token.
        token = get_token()
        
        # Step 2: Retrieve list of employees (without filtering by active status).
        employees = get_employees(token)
        print(f"Processing {len(employees)} employees.")
        
        # Use a list of tuples to store attendance data.
        # Each tuple: (user_hash, date, check_in, check_out)
        attendance_data = []
        
        # Step 3: Loop through each employee and get attendance data.
        for employee in employees:
            user_hash = employee.get("userHash")
            if not user_hash:
                continue  # Skip if no userHash is provided.
            
            try:
                report = get_employee_report(token, user_hash, FROM_DATE, TILL_DATE)
                days = report.get("days", [])
                if not days:
                    print(f"No attendance data for employee {user_hash} in the specified date range.")
                    continue
                
                for day in days:
                    date = day.get("date")
                    check_in = day.get("in")
                    check_out = day.get("out")
                    
                    # Only include the day if at least one of check-in or check-out is present.
                    if not check_in and not check_out:
                        continue
                    
                    check_in_formatted = format_time(check_in) if check_in else "N/A"
                    check_out_formatted = format_time(check_out) if check_out else "N/A"
                    
                    attendance_data.append((user_hash, date, check_in_formatted, check_out_formatted))
                    
            except Exception as e:
                print(f"Error processing employee {user_hash}: {e}")
        
        # Step 4: Insert the results into a Microsoft SQL Server database.
        sql_connection_string = input("Enter SQL Server connection string: ")
        conn = pyodbc.connect(sql_connection_string)
        cursor = conn.cursor()
        
        # Create a new table (drop if exists) for the attendance report.
        cursor.execute("IF OBJECT_ID('dbo.AttendanceReport', 'U') IS NOT NULL DROP TABLE dbo.AttendanceReport;")
        cursor.execute("""
            CREATE TABLE dbo.AttendanceReport (
                UserHash NVARCHAR(50),
                ReportDate DATE,
                CheckIn NVARCHAR(10),
                CheckOut NVARCHAR(10)
            )
        """)
        conn.commit()
        
        # Insert attendance data into the table.
        insert_query = "INSERT INTO dbo.AttendanceReport (UserHash, ReportDate, CheckIn, CheckOut) VALUES (?, ?, ?, ?)"
        cursor.executemany(insert_query, attendance_data)
        conn.commit()
        
        print("Attendance report inserted successfully into the Microsoft SQL database.")
        
        cursor.close()
        conn.close()
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Ask the user for API credentials and date range.
    IDENTYFIKATOR_KLUCZA = input("Enter IDENTYFIKATOR_KLUCZA: ")
    KLUCZ = input("Enter KLUCZ: ")
    FROM_DATE = input("Enter FROM_DATE (YYYY-MM-DD): ")
    TILL_DATE = input("Enter TILL_DATE (YYYY-MM-DD): ")
    
    main()