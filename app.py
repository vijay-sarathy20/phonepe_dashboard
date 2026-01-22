# Now, we have to import the important libraries for creating the interactive dashboard:

import streamlit as st

import numpy as np

import pandas as pd

import plotly.express as px


# we have successfully imported the important libraries used to create dashboard:

# streamlit -> which is used to create or build the web dashboard,

# numpy -> if we need to do any calculations or any functions related to numericals numpy is used. We have imported the numpy just for safety purposes.

# pandas -> It's used to handle the csv files and to handle the data inside the csv files.




# First step -> Now we have to set the configuration for the streamlit web page:


st.set_page_config(
    page_title = "PhonePe Pulse Data Analysis",
    layout = "wide"
)

st.title("📊 PhonePe Pulse Interactive Dashboard")
st.markdown("An interactive analysis of PhonePe transaction, users and growth patterns accross India")


# Now, we have to create sidebar. Sidebar is used to navigate through all the business case studies we have queried using MySQL:

# 5 Business Case Studies -> Transaction Dynamics, Device Dominance, Insurance Growth, Market Expansion, User Engagement.


st.sidebar.title("📌 Navigation")

menu = st.sidebar.radio(
    "Select Analysis",
    [
      "Home",
      "Transaction Dynamics",
      "Device Dominance",
      "Insurance Growth",
      "Market Expansion",
      "User Engagement"
    ]  
)

# from the above the syntax for st.sidebar.radio : st.sidebar.radio(label, options). We have assigned the label as "Select Analysis" and Options as the "Home" and "5 Business Case-studies".


st.write("You have selected the option: ", menu)

# The above code says if we select something in the sidebar, it automatically stored in the menu variable. Once, we call the variable using st.write it returns the "You selected : Menu names in the main page.


# Now, we have to tell the streamlit that if user click any options in the sidebar, just give me this page.


if menu == "Home":
    st.subheader("🏠 Home")
    st.write("Welcome to the PhonePe Pulse Interactive Dashboard")

elif menu == "Transaction Dynamics":
    st.subheader("💳 Transaction Dynamics")
    st.write("Analysis of transaction categories, trend and growth")

elif menu == "Device Dominance":
    st.subheader("📱 Device Dominace")
    st.write("Understanding the device usage and user engagement")

elif menu == "Insurance Growth":
    st.subheader("🛡 Insurance Growth")
    st.write("Insurance penetration and growth trends")

elif menu == "Market Expansion":
    st.subheader("🌍 Market Expansion")
    st.write("Transaction expansion oppurtunities across states")

elif menu == "User Engagement":
    st.subheader("👥 User Engagement")
    st.write("User growth and engagement behavior analysis")



# The sidebar is used to show the 5 business case study options. The above if and elif statement is used to show which type of data we have to show if the user clicks any case studies.


# Now, we have to load the CSV files( Foundation for All Charts):


@st.cache_data

def load_csv(file_name):
    return pd.read_csv(f"data/{file_name}")


# Now, we have to dive into each business case study and code the dashboard for multiple charts in each options:



if menu == "Transaction Dynamics":

    df = load_csv("aggregated_transaction.csv")


# Using the above code we have read the CSV file using the user defined function.


    year_selected = st.selectbox(
        "Select Year",
          sorted(df['year'].unique())
    )

    df_year = df[df['year'] == year_selected]


# from the above we have created the selectbox for year and filtered the year inside the csv file.

    summary = (
        df_year.
        groupby("transaction_category")["transaction_amount"]
        .sum()
        .reset_index()
    )

# from the above using the filtered df_year, we used aggregation function(sum) of transaction_amount for each category and stored it in the summary:
# which shows :  how much money flows through each categories or divisions?


# Now, we fetched the data from the CSV file and done some aggregation function and stored the result.

# From the result, we have to make the visualization using plotly. Plotly's used for data visualization.

    fig = px.bar(
        summary,
        x = "transaction_category",
        y = "transaction_amount",
        title = f"Transaction Amount by Category - {year_selected}",
        labels = {
             "transaction_category" : "Transaction Category",
             "transaction_amount" : "Transaction Amount"
        }
    )

    st.plotly_chart(fig, use_container_width = True)


    top_category = summary.sort_values("transaction_amount", ascending=False).iloc[0]

    st.success(
        f"📌 Insight: In {year_selected}, "
        f"**{top_category['transaction_category']}** dominates transactions "
        f"with a total value of ₹{top_category['transaction_amount']:,.0f}."
    )

# from the above code, we have successfully created the bar chart for case study 1 : Transaction dynamics on PhonePe.

# Now, we have to do another visualization for "Transaction Dynamics": 

# Visualization 2 : Category Trend Over Years (Using Line Chart) :

# which shows “Are transactions growing, stagnating, or declining over time?”

    trend_df = (
        df
        .groupby(['year','transaction_category'])['transaction_amount']
        .sum()
        .reset_index()
    )
    
    fig_trend = px.line(
        trend_df,
        x = 'year',
        y = 'transaction_amount',
        color = 'transaction_category',
        title = 'Transaction Amount Trend by Category',
        markers = True
    )

    st.plotly_chart(fig_trend, use_container_width = True)

    st.info(
        "📈 Insight: Peer-to-Peer payments and Merchant payments show consistent year-on-year growth, "
        "indicating increasing adoption of digital payments among businesses."
    )


# Now, we have to do visualization 3 for "Transaction Dynamics".

#Visualization 3 : Category Share (Using Pie Chart) :

    fig_share = px.pie(
        summary,
        names = 'transaction_category',
        values = 'transaction_amount',
        title = f"Transaction Share by Category - {year_selected}",
        hole = 0.4
    )

    st.plotly_chart(fig_share, use_container_width = True)

# Business Insight:

    top_category = summary.sort_values("transaction_amount", ascending=False).iloc[0]

    st.success(
        f"🏆 Insight: **{top_category['transaction_category']}** contributes the highest "
        f"transaction value of ₹{top_category['transaction_amount']:,.0f}, "
        "making it the backbone of PhonePe’s transaction ecosystem."
    )



# Case Study 2 : Device Dominance and User Engagement Analysis. 

# For this we have fetch the user_device.csv file for data visualization.


elif menu == "Device Dominance":

    df_device = load_csv("user_device.csv")


    year_selected = st.selectbox(
        "Select Year",
        sorted(df_device['year'].unique())
    )

    quarter_selected = st.selectbox(
          "Select Quarter",
          sorted(df_device['quarter'].unique())
    )



# Now, we have to filter the data, because if the user select any year or quarter. The aggregation or any function which has to apply for exactly the selected year. 
# Filtering before will reduce the noise and gives exactly what we want.


    df_filtered = df_device[
        (df_device['year'] == year_selected) &
        (df_device['quarter'] == quarter_selected)
    ]


# Now, we have to do the visualization part:


# 1) Top Device Brands (using bar chart):


    fig_brand = px.bar(
   
        df_filtered.sort_values("count", ascending = False),
        x = 'brand',
        y = 'count',
        title = 'Top Mobile Brands by Registered Users',
        labels = {'count' : 'Registered Users', 'brand' : 'Device Brand'}
    )

    st.plotly_chart(fig_brand, use_container_width = True)


# Now, we have to do Visualization 2:

# 2) Market Share (using pie chart):


    fig_share = px.pie(

        df_filtered,
        names = "brand",
        values = "percentage",
        title = "Device Market Share (%)"
    )

    st.plotly_chart(fig_share, use_container_width = True)


# Business Insights:

    top_brand = df_filtered.sort_values("count", ascending=False).iloc[0]

    st.success(
        f"📌 Insight: In {year_selected} {quarter_selected}, "
        f"**{top_brand['brand']}** leads with "
        f"{top_brand['count']:,} users "
        f"({round(top_brand['percentage']*100, 2)}% market share)."
    )

# Now, we have to do visualization 3:

# Visualization 3: Brand Growth Trend Over Time:

    brand_selected = st.multiselect(
        "Select Brands",
        options = sorted(df_device['brand'].unique()),
        default = sorted(df_device['brand'].unique())[:3]
    )


# The above code let users to compare multiple brands which the checkbox. In streamlit the multiple checkbox is created using st.multiselect().

# Now, we have to aggregation for trend analysis:

    trend_device = (
        df_device[df_device['brand'].isin(brand_selected)]
        .groupby(['year', 'brand'])['count']
        .sum()
        .reset_index()
    )

    
    fig_device_trend = px.line(
        trend_device,
        x = 'year',
        y = 'count',
        color = 'brand',
        markers = True,
        title = "Brand Growth Trend Over Time",
        labels = {
            "year" : "Year",
            "count" : "Registered Users",
            "brand" : "Mobile Brand"
        }
    )

    st.plotly_chart(fig_device_trend, use_container_width = True)


# Business Insights:
 
    st.info(
        "📈 Insight: Consistent upward trends indicate growing brand adoption, "
        "while flat or declining trends may signal market saturation or competition impact."
    )



     
# Now, we have to do 3rd business case study:

# Insurance Growth Analysis:  Which states are showing strong insurance adoption and growth potential?

# The file we're using to solve the above question : map_insurance_state.csv

elif menu == "Insurance Growth":

    df_insurance = load_csv("map_insurance_state.csv")

    year_selected = st.selectbox(
        "Select Year",
        sorted(df_insurance['year'].unique())
    )

    quarter_selected = st.selectbox(
        "Select Quarter",
        sorted(df_insurance["quarter"].unique())
    )

    df_filtered = df_insurance[
        (df_insurance["year"] == year_selected) &
        (df_insurance["quarter"] == quarter_selected)
    ]


    top_states = (
        df_filtered
        .groupby("state")[["count", "amount"]]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )

    # Bar chart – Insurance Amount by State

    fig_amount = px.bar(
        top_states.head(10),
        x="state",
        y="amount",
        title=f"Top 10 States by Insurance Amount – {year_selected}",
        labels={"amount": "Insurance Amount", "state": "State"}
    )

    st.plotly_chart(fig_amount, use_container_width=True)

    # Bar chart – Insurance Transactions by State

    fig_count = px.bar(
        top_states.head(10),
        x="state",
        y="count",
        title=f"Top 10 States by Insurance Transactions Based on Premium – {year_selected}",
        labels={"count": "Transaction Count", "state": "State"}
    )

    st.plotly_chart(fig_count, use_container_width=True)

    # Business Insight:

    top_state = top_states.iloc[0]

    st.success(
        f"📌 Insight: In {year_selected}, **{top_state['state']}** leads insurance adoption "
        f"with ₹{top_state['amount']:,.0f} across {top_state['count']:,} transactions."
    )


# Visualization 2 : Growth Opportunity Scatter Plot

    fig_scatter = px.scatter(
        top_states,
        x="count",
        y="amount",
        size="amount",
        color="state",
        title="Insurance Growth Opportunity: Count vs Amount",
        labels={
            "count": "Transaction Count",
            "amount": "Transaction Amount"
        }
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    top_state = top_states.iloc[0]

    st.success(
        f"📌 Insight: In {year_selected} {quarter_selected}, "
        f"**{top_state['state']}** leads insurance adoption with "
        f"₹{top_state['amount']:,.0f} transaction value."
    )


# Visualization 3 : Insurance Growth Trend:

    
    insurance_growth = (
        df_insurance
        .groupby("year")["amount"]
        .sum()
        .reset_index()
    )

    fig_ins = px.line(
        insurance_growth,
        x="year",
        y="amount",
        title="Insurance Transaction Growth Over Years",
        markers=True
    )

    st.plotly_chart(fig_ins, use_container_width=True)

    
    st.info(
        "📈 Insight: The upward trend highlights insurance as a long-term revenue driver, "
        "making it a strategic vertical for future investments and partnerships."
    )


# Now, we're going to do Business case study - 5:

# Case Study 4: Transaction Analysis for Market Expansion:

# Tables we're using map_transaction_state.csv.
  

elif menu == "Market Expansion":

    df = load_csv("map_transaction_state.csv")


# Visualization 1: Top 10 States by Transaction Amount

# Shows where PhonePe already dominates financially:

    st.subheader("🏆 Top 10 States by Transaction Amount")

    year_selected = st.selectbox(
        "Select Year",
        sorted(df["year"].unique()),
        key="market_year"
    )

    df_year = df[df["year"] == year_selected]

    top_states_amount = (
        df_year
        .groupby("state")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
        .head(10)
    )

    fig1 = px.bar(
        top_states_amount,
        x="state",
        y="amount",
        title=f"Top 10 States by Transaction Amount - {year_selected}",
        labels={"amount": "Transaction Amount"}
    )

    st.plotly_chart(fig1, use_container_width=True)


    top_state = top_states_amount.iloc[0]

    st.success(
        f"💡 Insight: **{top_state['state']}** leads in transaction value with "
        f"₹{top_state['amount']:,.0f}, indicating a mature and highly active market."
    )



# Visualization 2: Low Count but High Amount (Expansion Opportunity)

# These states = fewer users but higher value per transaction which are the perfect targets for market expansion & onboarding



    st.subheader("📈 High Value, Low Volume States (Expansion Opportunities)")

    summary = (
        df_year
        .groupby("state")[["count", "amount"]]
        .sum()
        .reset_index()
    )

    summary["avg_txn_value"] = summary["amount"] / summary["count"]

    opportunity_states = summary.sort_values(
        "avg_txn_value", ascending=False
    ).head(10)


# Scatter Plot -  why here scatter plot, because it's used to view the data multi dimensionally with respect to see the states based on count and amount.

    fig2 = px.scatter(
        opportunity_states,
        x="count",
        y="amount",
        size="avg_txn_value",
        color="state",
        title="Low Volume but High Transaction Value States",
        labels={
            "count": "Transaction Count",
            "amount": "Transaction Amount"
        }
    )

    st.plotly_chart(fig2, use_container_width=True)

# Business Insights:

    st.info(
        "📌 Insight: States with fewer transactions but high value indicate "
        "premium users. Targeted promotions can unlock massive growth potential."
    )


# Visualization 3: India Map – State-wise Transaction Amount:



    st.subheader("🗺️ India Transaction Heatmap")

    fig3 = px.choropleth(
        summary,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="state",
        color="amount",
        color_continuous_scale="Blues",
        title=f"State-wise Transaction Amount - {year_selected}"
    )

    fig3.update_geos(fitbounds="locations", visible=False)

    st.plotly_chart(fig3, use_container_width=True)

# Business Insights:

    st.success(
        "🗺️ Insight: Southern and Western India show strong transaction density, "
        "while emerging northern states present expansion opportunities."
    )




# Business Case Study 5 :


# User Adoption & Engagement Analysis:

# This business case study answers three question -> 1)Where are users growing?
# 2) Which regions are under-penetrated?
# 3) Are users transacting more or just signing up?



# For this case study we're using map_user_state.csv file:


# Visualization 1: Top 10 States by Registered Users:


elif menu == "User Engagement":

    df = load_csv("map_user_state.csv")


    st.subheader("👥 Top 10 States by Registered Users")

    year_selected = st.selectbox(
        "Select Year",
        sorted(df["year"].unique()),
        key="user_year"
    )

    df_year = df[df["year"] == year_selected]

    top_users = (
        df_year
        .groupby("state")["registeredusers"]
        .sum()
        .reset_index()
        .sort_values("registeredusers", ascending=False)
        .head(10)
    )

    fig1 = px.bar(
        top_users,
        x="state",
        y="registeredusers",
        title=f"Top 10 States by Registered Users - {year_selected}",
        labels={"registeredusers": "Registered Users"}
    )

    st.plotly_chart(fig1, use_container_width=True)


# Business insights:

    st.success(
        "📌 Insight: A few large states dominate the user base, "
        "indicating mature markets with strong adoption."
    )

# Visualization 2: Engagement Intensity (App Opens per User):


    st.subheader("📱 User Engagement Intensity by State")

    df_year["engagement_ratio"] = (
        df_year["appopens"] / df_year["registeredusers"]
    )

    top_engagement = (
        df_year
        .groupby("state")["engagement_ratio"]
        .mean()
        .reset_index()
        .sort_values("engagement_ratio", ascending=False)
        .head(10)
    )

    fig2 = px.bar(
        top_engagement,
        x="state",
        y="engagement_ratio",
        title="Top 10 States by Engagement Ratio",
        labels={"engagement_ratio": "App Opens per User"}
    )

    st.plotly_chart(fig2, use_container_width=True)

    top_state = top_engagement.iloc[0]

    st.success(
        f"📌 Insight: **{top_state['state']}** shows the highest engagement intensity, "
        f"with users opening the app on average **{top_state['engagement_ratio']:.2f} times**, "
        "indicating strong user stickiness and frequent usage behavior."
    )




# Visualization 3: User Growth Trend Over Time:


    st.subheader("📊 User Growth Trend Over Time")

    trend_df = (
        df
        .groupby("year")["registeredusers"]
        .sum()
        .reset_index()
    )

    fig3 = px.line(
        trend_df,
        x="year",
        y="registeredusers",
        markers=True,
        title="Year-wise Growth in Registered Users"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.info(
        "📈 Insight: The sustained rise in user registrations reflects strong platform trust "
        "and long-term growth potential."
    )



# Finally Home page map visualization using the entire transaction in india:


elif menu == "Home":

    st.title("🇮🇳 PhonePe Pulse – India Overview")
    st.markdown(
        "An interactive visualization of PhonePe's transaction footprint across India."
    )

    df = load_csv("map_transaction_state.csv")

    year_selected = st.selectbox(
        "Select Year",
        sorted(df["year"].unique()),
        key="home_year"
    )

    df_year = df[df["year"] == year_selected]

    summary = (
        df_year
        .groupby("state")["amount"]
        .sum()
        .reset_index()
    )

    fig = px.choropleth(
        summary,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="state",
        color="amount",
        color_continuous_scale="Viridis",
        title=f"State-wise Transaction Amount ({year_selected})"
    )

    fig.update_geos(fitbounds="locations", visible=False)

    st.plotly_chart(fig, use_container_width=True)

    st.success(
        "📌 Insight: Higher transaction concentration is observed in digitally mature states, "
        "highlighting regional adoption disparities."
    )






























