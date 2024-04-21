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

## Question Write-ups
### Question 1: Provide a short write-up on ML models: i. linear regression, ii. random forest, or iii. gradient boosting algorithms and select a predictive modeling technique that you would use to reasonably answer "What categories are growing or shrinking with changing customer engagement?".
Linear Regression: a line that best fits the relationship between the input variables and the output variables (y), by finding specific weightings for the input variables coefficients y = B0 + B1 * x. Predict y given the input x

Random Forest: We construct a multitude of decision trees during training, outputting the mode of the classes (classification) or the mean prediction (regression) of the individual trees. It creates a diverse set of decision trees using bootstrapping, and random feature selection. Each tree in the forest is trained on a random subset of the training data and features

Gradient Boosting: This method builds trees sequentially not independently, with each tree attempting to correct the errors of the previous one. Done by optimizing a loss function, with mean squared error for regression, log loss for classification, using gradient descent.

We decided to go with k-nearest neighbors model, as we can search the training set for the K most similar “neighbors” and summarize the output variable for those K instances. For each new data point, the model will search for K most similar instances in training and summarize the output variable (growth or shrinkage) for those K instances.

### Question 5: Which demographic factors (e.g. household size, presence of children, income) appear to affect customer engagement?
This question is answered through the visualizations on the dashboard page, however, we wanted to also provide explicit answers to this question.

We decided to have 4 visualizations:
1)	The first shows the relation between household numbers and the total spend, showing if the newer households have more or less spend. We can see that the older houses have a higher spending habit.
2)	A pie chart shows that food item consumption is the highest.
3)	The bar chart shows that people with one child spend more. Maybe because they need to buy new baby care items? People with 3+ children spend more than people with 2 children. This could be because the older children have grown up and have larger appetites.
4)	Age range 35-44 has the most spending because that is the time when most people start their families. And 55-64 is the age to retire/settle down, hence spending is more. Even after 75+ people spend more on their health.
