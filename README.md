# Online Voting System

The Online Voting System is a graphical user interface (GUI) application built using Tkinter in Python. It facilitates the process of voting by extracting user details from Aadhaar and voter ID cards, authenticating the elector against a dummy government database, and sending a one-time password (OTP) to the elector's mobile phone for verification. The system also includes an admin panel to check the voting results, and the admin's identity is verified using the Simple Mail Transfer Protocol (SMTP).

## Features

- **GUI Interface**: The system provides an intuitive graphical user interface built using Tkinter, which allows users to easily navigate and interact with the application.

- **Data Extraction**: EasyOCR is used to extract user details from Aadhaar and voter ID cards. The extracted data & entered user details are compared with a dummy government database to authenticate the elector's identity.

- **Mobile OTP Verification**: Twilio API is integrated to send a one-time password (OTP) to the elector's mobile phone. This adds an extra layer of security to ensure that only legitimate voters can participate in the voting process.

- **Database Management**: The system utilizes MySQL for backend database management. It stores the electors who have cast their votes in a separate database for tracking and auditing purposes.

- **Admin Panel**: An admin panel is provided to view the voting results. To access the admin panel, the administrator needs to be verified using the Simple Mail Transfer Protocol (SMTP) library in Python.

## Requirements

- Python 3.x
- Tkinter
- EasyOCR
- MySQL
- Twilio API
- SMTP

## Installation

1. Clone this repository:

```
git clone https://github.com/akshitbtw/GUI-Based-Online-Voting-System.git
```

2. Install the required dependencies. You can use pip to install them:

```
pip install tkinter
pip install easyocr
pip install mysql-connector-python
pip install twilio
```

3. Set up the MySQL database:
   - Install MySQL if you haven't already.
   - Create 2 new databases, 1 which acts as government database & 1 to store electors that have voted.
   - Update the database connection settings in the application code.

4. Configure the Twilio API:
   - Sign up for a Twilio account and obtain your API credentials.
   - Update the Twilio API settings in the application code.

5. Configure the SMTP settings:
   - Update the SMTP server settings and email credentials in the application code.

## Usage

1. Run the application:

```
python main.py
```

2. The GUI interface will be displayed. Users can enter their details.

3. The system will authenticate the elector against the dummy government database and send an OTP to their mobile phone for verification.

4. Once the OTP is verified, the elector will be able to cast his/her vote, and the elector will be stored in the voted electors database.

5. The admin can access the admin panel by logging in using the provided credentials.

6. In the admin panel, the voting results can be checked and analyzed.

## Screenshots


