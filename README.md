# Dreamclinic Customer Churn

## Business Understanding -

I work at a Dreamclinic Massage in Seattle. Clients come in and use our services for some amount of time and then stop coming. We also have therapists that have been calling out last minute for injury reasons which causes therapists to last minute cancel/reschedule on their clients which hurts the overall moral of both clients and therapists.


## Client Data -

There are ~110,000 entries of client data.
The client data from August 2016 to August 2019 is avialable in the client_df.pkl file in this repo
Date of visit
Who they received massage/acupuncture from
What service they recieved
Length of service
Zip code they live in


## Data Preparation -
I dealt with missing values. I will define a ‘churn instance’ when a client hasn’t had a massage in the last 2 months.
I also aggregated the features I wanted for my modeling which include:

1. How many times they have come in.
2. Which therapist they've seen and how many times they've seen them.
3. Which zipcode they live in.
4. What their average session length is.
5. How many hours they've recieved massage.

## Modeling -
I split the data into training and testing clients to develop a model for predicting churn risk.
I took the last 3 years of Client data and ran it through a Logistic Regression, Random Forest Classifier, and Grandient Boosting.

I have the ROC and Precision-Recall curves to all my CEO to make decisions based on future workflows.

## Evaluation -
I looked at the pression and recall of both of the models to give me CEO more data on how we could be making business decisions to reduce client churn.

## Deployment -
I showed the EDA and final model prediction capabilities to my CEO so that she can make data driven decisions on how to engage with our clientile that is churning or not.

### Presentation Link:
https://docs.google.com/presentation/d/1Ysxvsx8TlXU9UzJRwUkjhwx-4qk8lmAB_9pOEiAmRcM/edit?usp=sharing
