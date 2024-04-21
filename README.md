# Cloud Computing Final Project
Created by Saumick Pradhan, Carson McCarthy, and Emma Gardner, this web application uses Microsoft Azure and Databricks to visualize, search, and upload anonymized transaction, household, and product data from 84.51°/Kroger.

## Availability and Use
This application is running at http://20.121.58.13. First, you must log in or create an account. Then, you will be taken to a menu page. You can press one of the buttons (search for data, upload data, or view the dashboard), or log out.

**NOTE:** We are aware of an issue occurring on the SQL server. It is unclear why, but the connection is sometimes refused after it hasn't received any queries for a while. If you receive an error, please reload the page, and it should be resolved. We apologize for any inconvenience!

### Dashboard
This page contains visualizations of the retail data, which were created using Databricks. The notebook is the DashboardTemp.ipynb file within this repository.
![image](https://github.com/SaumickPradhan/Retail-Customer-Trends/assets/56894514/c85b4f81-98e3-4783-879e-1d44c6506488)


### Search for Data
This page allows users to search for retail data (households, transactions, and products joined on the product IDs and household IDs). Simply enter a household ID number and press the search button to populate a table with the related data.

#### Initial page (displaying data for household number 10)
![image](https://github.com/SaumickPradhan/Retail-Customer-Trends/assets/56894514/1d5ab030-767f-439d-a8e3-233609d2bb5b)
#### Page after searching for household number 577
![image](https://github.com/SaumickPradhan/Retail-Customer-Trends/assets/56894514/4df48ba0-679f-4b84-969b-8a42d288ea6c)

### Upload Data
This page allows users to upload data in a CSV file so that it is added to the corresponding database table. Simply select within the dropdown the type of data you want to upload (transaction, household, or product). Then, click the Choose File button to select the CSV file containing the data you wish to upload. After pressing the Upload button, the data will be inserted into the appropriate database table and appear when searched for within the "Search for Data" page.
