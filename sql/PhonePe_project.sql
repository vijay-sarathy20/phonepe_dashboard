# Now, we have to create database to write the case queries based on the business insights for PhonePe project:

CREATE DATABASE phonepe_db;
USE phonepe_db;

# Now, we have to create the 16 tables for different insights based on aggregated, map, top within the transaction, user and insurance:

CREATE TABLE aggregated_transaction(
   year INT,
   quarter varchar(2),
   transaction_category varchar(50),
   transaction_count bigint,
   transaction_amount double
);

CREATE TABLE aggregated_user(
    year int,
    quarter varchar(2),
    registeredusers bigint,
    appopens bigint
);

CREATE TABLE aggregated_insurance(
     year int,
     quarter varchar(2),
     category varchar(50),
     count bigint,
     amount double
);

USE phonepe_db;


CREATE TABLE user_device(
     year int,
     quarter varchar(2),
     brand varchar(50),
     count bigint,
     percentage float
);

# From the above we have created the tables for aggregated portion.alter

# Now, we have to create the tables for map portion and the map portion contains state and district level dataframes:


CREATE TABLE map_transaction_state(
     year int,
     quarter varchar(2),
     state varchar(50),
     count bigint,
     amount double
);

CREATE TABLE map_transaction_district(
	 year int,
     quarter varchar(2),
     state varchar(50),
     district varchar(60),
     count bigint,
     amount double
);


CREATE TABLE map_user_state(
     year int,
     quarter varchar(2),
     state varchar(50),
     registeredusers bigint,
     appopens bigint
);


CREATE TABLE map_user_district (
    year INT,
    quarter VARCHAR(2),
    state VARCHAR(50),
    district VARCHAR(60),
    registeredusers BIGINT,
    appopens BIGINT
);

CREATE TABLE map_insurance_state(
	 year int,
     quarter varchar(2),
     state varchar(50),
     count bigint,
     amount double
);

CREATE TABLE map_insurance_district(
     year int,
     quarter varchar(2),
     state varchar(50),
     district varchar(70),
     count bigint,
     amount double
);

# we have successfully created tables for map portion for state and district level drill down.alter

# Now, we have to create table for top portion like wise in map with state and district level tables for transaction, user and insurance:

CREATE TABLE top_transaction_state(
      year int,
      quarter varchar(2),
      state varchar(50),
      count bigint,
      amount double
);

CREATE TABLE top_transaction_district(
	  year int,
      quarter varchar(2),
      state varchar(50),
      district varchar(70),
      count bigint,
      amount double
);

CREATE TABLE top_user_state(
      year int,
      quarter varchar(2),
      state varchar(50),
      registeredusers bigint
);


CREATE TABLE top_user_district(
      year int,
      quarter varchar(2),
      state varchar(50),
      district varchar(70),
      registeredusers bigint
);

CREATE TABLE top_insurance_state(
      year int,
      quarter varchar(2),
      state varchar(50),
      count bigint,
      amount double
);

CREATE TABLE top_insurance_district(
	 year int,
     quarter varchar(2),
     state varchar(50),
     district varchar(50),
     count bigint,
     amount double
);

# From the above we have successfully created the 16 tables based on aggregated,top and map for transaction,user and insurance within the phonepe_db.


USE phonepe_db;


select count(*) from aggregated_transaction;
select* from aggregated_transaction limit 5;

select* from top_transaction_district limit 5;

# The above 3 queries are used to check whether the tables have been imported successfully without any issues and the result shows it has been imported successfully.

# Now, we're going to query for 5 business insights to develop the streamlit business problems:

# First we choosed Decoding Transaction Dynamics on PhonePe:

# PhonePe wants to understand how transactions behave across time and categories:

# 1) Which transaction categories dominate?

# 2) How do transactions change quarter-wise and year-wise?

# 3) Are users spending more money or just making more transactions?


# For the above questions, we're going to take aggregated_transaction tables which contains transaction_categories, transaction_count and amount, year and quarter wise columns.

# Q1. Which transaction categories generate the highest total amount?

select 
    transaction_category,
    sum(transaction_amount) as category_total_amount
from aggregated_transaction
group by transaction_category
order by category_total_amount desc;

# Q2. How does transaction amount grow year-wise?

select 
    year,
    sum(transaction_amount) as year_wise_total_amount
from aggregated_transaction
group by year
order by year;

# Q3. Quarter-wise transaction trend

select 
    quarter,
    sum(transaction_amount) as quarter_wise_total_amount
from aggregated_transaction
group by quarter
order by quarter;

# Q4. Average transaction value per category:

# which means, Are users spending more per transaction?

select 
    transaction_category,
    sum(transaction_amount)/sum(transaction_count) as avg_transaction_value,
    sum(transaction_count) as category_transaction_count
from aggregated_transaction
group by transaction_category
order by avg_transaction_value desc;

 

# Q5. Top transaction categories per year

select 
    year,
    transaction_category,
    sum(transaction_amount) as total_amount
from aggregated_transaction
group by year, transaction_category
order by year, total_amount desc;


# From the above queries we have successfully solved few questions about the phonepe transaction dynamics.

# Now, we're going to query the second phonepe business case-study:

# Business Objective 

# The second business case-study is Device Dominance & User Engagement Analysis:

# Now, we're going to divide the second business case-study into two parts:

# PART 1: Device Dominance Analysis (user_device) -> In part one, we analyze the device dominace using the user_device table:

# PART 2: User Engagement Analysis (aggregated_user) -> In part two, we analyze user_engagement with the phonepe app using aggregated_user:



# Now, we start with PART 1: Device Dominance Analysis (user_device):

# Question 1

# Which device brands have the highest user count?

SELECT
    brand,
    sum(count) as user_count
from user_device
group by brand
order by user_count desc;

# Question 2

# How device preference changes over time?

select
    year,
    brand,
    sum(count) as user_count
from user_device
group by year, brand
order by year, user_count desc;


# Question 3

# Device distribution by quarter?

SELECT
    year,
    quarter,
    brand,
    SUM(percentage) AS brand_share
FROM user_device
GROUP BY year, quarter, brand
ORDER BY year, quarter, brand_share DESC;


# PART 2: User Engagement Analysis (aggregated_user)

# Question 4

# How does user engagement grow over time?

SELECT
    year,
    SUM(registeredusers) AS total_registeredusers,
    SUM(appopens) AS total_app_opens,
    ROUND(sum(appopens) / sum(registeredusers), 2) AS engagement_ratio
FROM aggregated_user
GROUP BY year
ORDER BY year;

# Question 5

# Quarter-wise engagement pattern?

SELECT
    year,
    quarter,
    SUM(appopens) AS total_app_opens
FROM aggregated_user
GROUP BY year, quarter
ORDER BY year, quarter;


# We have defined the business case studies for Device dominance and user engagement analysis:

# Now, we're going to query third business case-study:

# Insurance Penetration & Growth Potential Analysis

# PhonePe wants to:

# 1) Understand how insurance usage is growing

# 2)Identify top-performing states

# 3)Find states with low penetration but high growth potential


# The tables are : aggregated_insurance and map_insurance_state

# Question 1:

# Is insurance usage growing year by year?

select
    year,
    sum(count) as total_policies,
    sum(amount) as total_policy_amount
from aggregated_insurance
group by year
order by year;

# Question 2:

# Which states are leading in insurance usage?

select
    state,
    sum(count) as statelevel_total_policies,
    sum(amount) as total_policy_amount_state
from map_insurance_state
group by state
order by statelevel_total_policies desc
limit 10;



# Question 3:

# Which states have low current usage but high potential? -> which means high growth potential - hidden oppurtunity states:

select
    state,
    sum(count) as statelevel_total_policies,
    round(sum(amount) / sum(count), 2) as avg_premium_amount
from map_insurance_state
group by state
having statelevel_total_policies < 1000000
order by avg_premium_amount desc
limit 10;


# Question 4:

# Do insurance purchases increase in specific quarters?

select
    year,
    quarter,
    sum(count) as total_policies
from aggregated_insurance
group by year, quarter
order by year, quarter;


# We have queried the important problems for Insurance Penetration & Growth Potential Analysis:

# Now, we have to query the fourth business case-study:

# Transaction Analysis for Market Expansion

# The table that we're going to use -> map_transaction_state

# why map_transaction_state? -> because the market expansion has been discussed in state-wise. The district will cause lots of noise in this scenario.


# Business Question 1:

# Which states contribute the highest transaction value overall?

select 
	state,
    sum(amount) as total_transaction_amount
from map_transaction_state
group by state
order by total_transaction_amount desc
limit 10;

# Business Question 2:

# Which states have the highest number of transactions?

select
    state,
    sum(count) as total_transaction_count
from map_transaction_state
group by state
order by total_transaction_count desc
limit 10;


# Business Question 3

# How is transaction growth evolving year by year across states?

select 
	year,
    state,
    sum(amount) as total_transaction_amount
from map_transaction_state
group by year, state
order by year, total_transaction_amount desc;


# Business Question 4

# Which states have high transaction count but relatively low transaction value?


select 
    state,
    sum(count) as total_transaction_count,
    sum(amount) as total_transaction_amount,
    round(sum(amount) / sum(count), 2) as avg_transaction_value
from map_transaction_state
group by state
order by avg_transaction_value asc;


# we have successfully  queried the case-study 4 business questions:

# Now, we have to query the fifth case-study:

# User Engagement & Growth Strategy -> Understand how users engage with PhonePe across: States, Districts and Time (year / quarter):

# The tables we're going to use: 
# State - level -> map_user_state, District - level : map_user_district, Overall growth strategt analysis -> aggregated_user


# Business Question: 

# Which states have the highest user engagement?

# Engagement = App Opens per Registered User

select
    state,
    sum(registeredusers) as total_registeredusers,
    sum(appopens) as total_appopens,
    round(sum(appopens) / sum(registeredusers), 2) as engagement_ratio
from map_user_state
group by state
order by engagement_ratio desc;



# Business Question:

# Which districts show low engagement despite high registrations?

select
    state,
    district,
    sum(registeredusers) as total_registeredusers,
    sum(appopens) as total_appopens,
    ROUND(sum(appopens) / sum(registeredusers), 2) AS engagement_ratio
from map_user_district
group by state,district
having sum(registeredusers) > 500000
order by engagement_ratio asc;


# Business Question:

# How has user engagement evolved over time?

select
    year,
    sum(registeredusers) as total_registeredusers,
    sum(appopens) as total_appopens
from aggregated_user
group by year
order by year;


# The 5 business case study and the business questions has been queried successfully!!!





    






















