#QA Automation Platform

## Project overview

This is a Django-based QA Automation Platform Project designed to provide role-based access for users such as Admin, manager, Tester and support QA-related activities. The initial phase focuses on building a secure authentication and authorization system before implementing dashboard and test case management.

Current implementation includes:

- User login
- Role-based access
- JWT Authentication
- Protected API endpoint
- Token expiry testing

----

## Technologies used

- Python
- Django
- PostgresSQL
- simple JWT
- HTML
- Javascript
- pgAdmin
- Django REST Frameworks

---

## Objectives of Database Configuration

Set up PostgreSQL as the application's backend database.

Implementation:

PostgreSQL and pgAdmin were installed.
Django database settings were set up to connect to PostgreSQL.
created database tables by applying migrations.
confirmed that the database connection was successful.
pgAdmin was used to verify data persistence.

The result:
Instead of using SQLite, the program now uses PostgreSQL to store all user, role, session, and token data.

---

## User Authentication System Objective:

Give platform users safe ways to log in.
Login with your username
Users can use their username to log in.
Email Sign-in
Additionally, users can use their registered email address to log in.

Flow of Authentication:

After entering their username, email address, and password, the system verifies their credentials, authenticates them, and grants them access to the dashboard. Modified files include accounts/views.py and accounts/templates/login.html.

---

## Role-Based Access Control (RBAC) Objective:

Provide different dashboards and permissions based on user roles.

Roles Implemented:

Admin-Can access Admin Dashboard.
Manager-Can access Manager Dashboard.
Tester-Can access Tester Dashboard.

Implementation:
Created a UserProfile model that stores the role associated with each user.

Example:
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)

Login Flow:

User Login-->Read User Role-->Admin → Admin Dashboard
Manager → Manager Dashboard
Tester → Tester Dashboard

Files Modified:
accounts/models.py
accounts/views.py

---

## JWT Authentication objective

- Use JSON Web Tokens (JWT) to implement token-based authentication.

Why JWT?
- Without keeping authentication data in browser sessions, JWT enables safe authentication.
- Every user who has been verified gets:

Implementation of Access and Refresh Tokens
- using the Simple JWT package for the Django REST Framework.

Access Token
- used to gain access to resources that are protected.

Refresh Token
- used to create fresh access tokens following their expiration.

Files Modified:
config/settings.py
accounts/views.py
config/urls.py

JWT Generation Flow:

User Login-->Generate Access Token-->Generate Refresh Token-->Store Tokens in Database-->Redirect User to Dashboard

---

## JWT Token Storage in PostgreSQL Objective:

Store generated JWT tokens and session information for tracking and auditing purposes.

Model Created:
UserSessionToken

The model stores:
User
Session ID
Access Token
Refresh Token
Expiration Time
Created Time

Example Fields:
user
session_id
access_token
refresh_token
expires_at
created_at
Why Store Tokens?
Track active sessions
Maintain token history
Audit user activity
Support token refresh mechanism
Verification

Verified token records using:
pgAdmin
Django Admin Panel

---

## Session UUID Tracking Objective:
- Assign a unique identifier to each login session.
- Each new login creates a new Session ID.
- Token refresh operations use the same Session ID.

Implementation:
A UUID is generated whenever a user logs in.

Example:
session_id = uuid.uuid4()
Purpose
Identify user sessions uniquely
Track token refreshes for the same session
Improve auditing and session management

---

## Automatic JWT Token Refresh Objective:
- Automatically generate a new access token before expiration.

Problem:
- Access tokens expire after a short duration.

Without refresh:
User Login-->Token Expires-->User Logged Out

Solution:
Created a custom endpoint:

/refresh-session-token/

JavaScript periodically calls this API.

Workflow:
Dashboard Open-->Timer Executes-->Refresh API Called-->New Access Token Generated-->Token Stored in PostgreSQL-->User Remains Logged In

Verification:
- Confirmed successful refresh requests in Browser Network Tab.

Example:
POST /refresh-session-token/ 200
Verified new records inserted into PostgreSQL.

Files Modified:
accounts/views.py
dashboard HTML files

---

## Role Validation Objective:
- Prevent users from accessing dashboards assigned to other roles.

Example:
if request.user.userprofile.role != "admin":
    return HttpResponse("Access Denied")

Result:
Tester cannot access Admin Dashboard.
Manager cannot access Admin Dashboard.
Unauthorized access is blocked.

---

## Logout Functionality Objective:
- Allow users to securely end their session.

Implementation:
- Created logout view.

Example:

def logout_view(request):
    logout(request)
    return redirect("login")

Workflow:

User Clicks Logout-->Session Terminated-->Redirect to Login Page

Files Modified:
views.py
urls.py
dashboard templates

---

## Forgot Password Feature Objective:
- Allow users to recover access when they forget their password.

Pages Created:
forgot_password.html
reset_password.html

Workflow:
Forgot Password-->Enter Email Address-->Verify User Exists-->Open Reset Password Page-->Enter New Password-->Password Updated

---


## Reset Password Implementation Objective:
- Allow users to set a new password.

Password Update Logic:
- Used Django's built-in password hashing method:

user.set_password(new_password)
user.save()

Why?
- Passwords are never stored in plain text.
- Django automatically hashes the password before saving it.

---

## Password Validation Rules Objective:
- Prevent users from creating weak passwords.

Password must contain:
Minimum 8 characters
At least 1 uppercase letter
At least 1 lowercase letter
At least 1 number
At least 1 special symbol

Examples:
password123 - not accepted
test1234    - not accepted
Test1234    - not accepted
Test@123    - accepted
Qa@2026Admin - accepted

Validation Function:
- custom validation function using Python Regular Expressions.

Purpose:
- Improve security
- Prevent weak passwords
- Follow industry standards

---

## Change Password Feature Objective

Allow authenticated users to securely change their password without administrator intervention.

- Improve account security
- Allow users to update compromised passwords
- Enable self-service password management

Workflow:

User Login-->Open Change Password Page-->Enter Current Password-->Enter New Password-->Password Validation-->Password Updated Successfully

Result:Users can securely update their passwords while remaining authenticated.

Files Modified:
- accounts/views.py
- accounts/urls.py
- accounts/templates/accounts/change_password.html

---

## My Sessions Feature Objective

Allow users to view all active login sessions associated with their account.

Purpose:

- Improve account visibility
- Track active logins
- Support security auditing

Information Displayed:

- Session ID
- Login Time
- Access Token Expiration
- Refresh Token Expiration

Workflow:

User Login-->Open My Sessions Page-->Retrieve Session Records-->Display Active Sessions

Result:
Users can monitor active sessions associated with their account.

Files Modified:

- accounts/views.py
- accounts/templates/accounts/my_sessions.html

---

## Automatic UserProfile Creation Objective

Automatically create a UserProfile whenever a new user account is created.

Purpose:
- Eliminate manual profile creation
- Ensure every user has an assigned role
- Support role-based access control

Implementation:
Django signals are used to automatically create a UserProfile after user creation.

Workflow:

New User Created-->Signal Triggered-->UserProfile Created-->Default Role Assigned

Result:
Every user automatically receives a UserProfile record.

Files Modified:
- accounts/models.py
- accounts/signals.py
- accounts/apps.py

---

## Forgot Username Feature Objective
Allow users to recover their username using their registered email address.

Purpose:

- Help users regain access
- Reduce administrative support requests

Workflow:

User Opens Forgot Username Page-->Enter Registered Email-->Verify Email Exists-->Display Username

Result:
Users can recover forgotten usernames without contacting an administrator.

Files Modified:
- accounts/views.py
- accounts/urls.py
- accounts/templates/accounts/forgot_username.html

---

## Test Case Management Objective

Provide a centralized location for testers to upload, store, and manage QA test cases.

Features Implemented:

- Upload new test cases
- Store uploaded files
- Track test case details
- View uploaded test cases
- Associate test cases with users

Model Created: TestCase

Fields Stored:

- Title
- Project Name
- Description
- Status
- Uploaded File
- Uploaded By
- Uploaded At

Result:
Test cases are stored in PostgreSQL and linked to the user who uploaded them.

Files Modified:
- testcases/models.py
- testcases/admin.py

---

## Test Case Upload Objective

Allow testers to upload QA test cases and supporting documents.

Upload Form Fields:

- Title
- Project Name
- Description
- Status
- Uploaded File

Workflow:

Tester Login-->Open Upload Test Case Page-->Enter Test Case Details-->Choose File-->Submit Form-->Save Record In Database-->Store File In Media Folder

Result:
Test cases and files are successfully stored in the system.

Files Modified:

- testcases/forms.py
- testcases/views.py
- testcases/templates/testcases/upload_testcase.html

---

## File Upload Management Objective

Allow users to upload and access QA-related documents.

Configuration:
Media files are stored separately from application code.

Features:
- Upload PDF files
- Upload DOCX files
- Store uploaded documents
- Open uploaded files from portal

Result:
Uploaded files are accessible directly from the application.

Files Modified:
- config/settings.py
- config/urls.py

---

## View Test Cases Objective
Display all uploaded test cases in a tabular format.

Information Displayed:

- Title
- Project Name
- Description
- Status
- Uploaded By
- Uploaded At
- Uploaded File

Workflow:

User Opens View Test Case-->Fetch Records From Database-->Display Test Cases In Table

Result:
Users can view all available test cases from a centralized page.

Files Modified:
- testcases/views.py
- testcases/templates/testcases/view_testcases.html

---

## Test Case Status Tracking Objective
Track the execution status of every test case.

Status Values:

- Pending
- In Progress
- Passed
- Failed

Purpose:
- Monitor testing progress
- Identify completed testing
- Identify failed testing
- Improve reporting visibility

Workflow

Tester Uploads Test Case-->Status = Pending-->Tester Executes Test Case-->Tester Updates Status-->Passed / Failed / In Progress

Result:
The current status of every test case is visible from the portal.

Files Modified:
- testcases/models.py
- testcases/views.py
- testcases/templates/testcases/view_testcases.html

---

