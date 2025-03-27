import streamlit as st
import pandas as pd

# Load classified emails & summaries
df_emails = pd.read_csv("classified_emails.csv")
df_summaries = pd.read_csv("email_summaries.csv")

st.title("📩 AI-Powered Email Dashboard")

# Select category
category = st.selectbox("📂 Select Email Category:", df_emails["Category"].unique())

# Filter emails by category
filtered_emails = df_emails[df_emails["Category"] == category]

# Select cluster within category
cluster = st.selectbox("🔍 Select Cluster:", filtered_emails["Cluster"].unique())

# Display emails in the selected cluster
st.subheader("📬 Emails in Cluster:")
st.write(filtered_emails[filtered_emails["Cluster"] == cluster][["Subject", "Body"]])

# Show summary for the selected cluster
summary = df_summaries[df_summaries["Cluster"] == cluster]["Summary"].values
if len(summary) > 0:
    st.subheader("📜 Email Summary:")
    st.write(summary[0])
else:
    st.write("No summary available.")
