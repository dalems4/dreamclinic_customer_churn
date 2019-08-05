# Dreamclinc Customer Churn - 
# Flatiron Data Science Bootcamp Capstone Project

Business Understanding
I work at a Dreamclinic Massage in Seattle. Clients come in and use our services for some amount of time and then stop coming. We also have therapists that have been calling out last minute for injury reasons which causes use to have to last minute cancel/reschedule on their clients which hurts the overall moral of clients and therapists.


Data Understanding
The massage clinic has data on clients and therapists:
Client Data: 
Date of visit
Length of service
Who they received massage or acupuncture from
Address
Age
If they were referred or not and by whom
Regence vs other Insurance vs OOP payment


Therapist Data:
When they work
Who they work on
Which clients request to work with them
How much they make per massage hour
How long they have been working at the company
How many times they have called out


All of the data is currently stored in a FileMaker database to be requested in excel format for Pandas manipulations and modeling.

Data Preparation
My goal is to take the last 2 years of Client data and prepare it to model churn. I will prepare the data by dealing with missing values and creating a “distance from clinic” feature based on client’s address using Folium and geopy to calculate. I will define a ‘churn instance’ when a client hasn’t been in for 2 months.

I will take the therapist data and put it into a postgresql database for easier manipulation


Modeling
I will split the data into training and testing clients to develop a model for predicting churn risk.
I will start by using linear regression


Evaluation
I will report both the accuracy score and cross entropy loss, on training and test data.


Deployment
The model will be deployed as a dashboard that updates with real time data each week that my CEO can use to make real time business decisions/policies to increase customer retention and also to reduce therapist callout rates.
