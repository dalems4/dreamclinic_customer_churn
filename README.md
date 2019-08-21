# Dreamclinc Customer Churn - 
# Flatiron Data Science Bootcamp Capstone Project

# Business Understanding -

I work at a Dreamclinic Massage in Seattle. Clients come in and use our services for some amount of time and then stop coming. We also have therapists that have been calling out last minute for injury reasons which causes use to have to last minute cancel/reschedule on their clients which hurts the overall moral of clients and therapists.


# Client Data -
Date of visit
Length of service
Who they received massage/acupuncture from
Zip code they live in
If they were referred or not and by whom
Regence vs other Insurance vs OOP payment

The client data from August 2016 to August 2019 is avialable in the .pkl file in this repo

# Data Preparation -
I dealt with missing values. I will define a ‘churn instance’ when a client hasn’t had a massage in the last 2 months.
I also aggregated the features I wanted for my modeling which includes:


# Modeling -
I split the data into training and testing clients to develop a model for predicting churn risk.
I took the last 3 years of Client data and ran it through a Logistic Regression and a Random Forest Classifier

# Evaluation -
I looked at the pression and recall of both of the models to give me CEO more data on how we could be making business decisions to reduce client churn.

# Deployment -
I showed the EDA and final model prediction capabilities to my CEO so that she can make data driven decisions on how to engage with our clientile that is churning or not.
