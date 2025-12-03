# Automated Quotes Email Delivery Service using ZenQuotes API

## Data Engineering Community LaunchPad Mentorship Python task project

## Project Objective
Task is to build an automated quote email delivery platform using ZenQuotes API. Get quotes from the API and automate daily sending to subscribers’ email.

![pic](https://github.com/user-attachments/assets/f43e0031-ebd5-4eec-8f4f-f4fc22ac893d)

## Project Overview
The project is for MindFuel Company, a mental wellness startup.
They want to send motivational quotes to subscribed users every morning at 7 AM.

Task is to build a production-grade backend service that:
- Pulls a new quote daily from ZenQuotes API
- Personalizes and sends it to subscribed users via email
- Logs activity and handles failures
- Can scale to hundreds or thousands of users

## Deliverables
### 1. ZenQuotes API
- Fetch quote from the API: https://zenquotes.io/
  - Handle edge cases:
  - No response
  - Malformed response
    
### 2. User Subscription Management
- Create a users table in any database management system of your choice (e.g., Postgres, MySQL, SQL Server).
- Each user should have:
  - Email address
  - Name
  - Subscription status (active/inactive)
  - Email frequency preference (daily/weekly)
    
### 3. Email Module
- Send personalized quotes
- Handle failures and with retries
- Log email delivery status per user
  
### 4. Logging & Monitoring
- Log events to files
- Quote fetched
- Email sent (to which user, when)
- Failures and retry attempts
- Send email summary logs to admin (e.g., daily email with stats)

### 5. Requirements for project:
Clone Project directory
```
git clone https://github.com/kabiromohd/email_services.git

cd email_services

pip install -r requirements.txt
```
Rename ```.env_test``` to ```.env``` and populate the relevant parameters with your own details
  
### 6. Create the users database
Open ```database_setup.py``` and populate valid users details, names and save.
Run below command to setup a duckdb database:

```
python database_setup.py
```

### 7. Email service launches via cron or manual
- setup a cron job as in below screenshot

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/abb36f76-1fec-4823-8f1a-9d1a2bd6a286" />

- The App can be manually run via this command:
  
```
python main.py

```

