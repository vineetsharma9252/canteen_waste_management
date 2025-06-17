import pandas as pd
import streamlit as st
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

# Set up the Streamlit page
st.set_page_config(page_title='Canteen Waste Management Dashboard', page_icon=":recycle:", layout="wide")
st.title(":recycle: Canteen Waste Management Dashboard")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

# Load datasets
@st.cache_data
def load_data():
    df_waste = pd.read_csv('day_meal_type_waste.csv')
    df_absent = pd.read_csv('day_meal_type_absent.csv')
    df_hostel = pd.read_csv('hostel_waste.csv')
    return df_waste, df_absent, df_hostel

df_waste, df_absent, df_hostel = load_data()

# Create a date column for filtering (assuming data spans one week, we'll simulate dates)
date_range = pd.date_range(start="2025-06-09", end="2025-06-15")  # One week
days = df_waste['day'].unique()
day_to_date = {day: date for day, date in zip(days, date_range)}
df_waste['Date'] = df_waste['day'].map(day_to_date)
df_absent['Date'] = df_absent['day'].map(day_to_date)

# Date filters
startdate = df_waste['Date'].min()
enddate = df_waste['Date'].max()

col1, col2 = st.columns(2)
with col1:
    date1 = st.date_input("Start Date", startdate)
with col2:
    date2 = st.date_input("End Date", enddate)

df_waste = df_waste[(df_waste['Date'] >= pd.to_datetime(date1)) & (df_waste['Date'] <= pd.to_datetime(date2))]
df_absent = df_absent[(df_absent['Date'] >= pd.to_datetime(date1)) & (df_absent['Date'] <= pd.to_datetime(date2))]

# Sidebar filters
st.sidebar.header("Filters")
day = st.sidebar.multiselect("Select Day", df_waste["day"].unique(), default=df_waste["day"].unique())
meal_type = st.sidebar.multiselect("Select Meal Type", df_waste["meal_type"].unique(), default=df_waste["meal_type"].unique())
hostel = st.sidebar.multiselect("Select Hostel", df_hostel["Hostel"].unique(), default=df_hostel["Hostel"].unique())

# Apply filters
filtered_waste = df_waste[df_waste["day"].isin(day) & df_waste["meal_type"].isin(meal_type)]
filtered_absent = df_absent[df_absent["day"].isin(day) & df_absent["meal_type"].isin(meal_type)]
filtered_hostel = df_hostel[df_hostel["Hostel"].isin(hostel)]

# Visualization: Waste Volume by Day and Meal Type
st.subheader("Waste Volume by Day and Meal Type")
fig1 = px.bar(filtered_waste, x="day", y="waste_in_kg", color="meal_type", 
              title="Total Waste Volume by Day and Meal Type", template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# Visualization: Waste Distribution by Meal Type
st.subheader("Distribution of Waste by Meal Type")
fig2 = px.pie(filtered_waste, names="meal_type", values="waste_in_kg", hole=0.4, 
              title="Waste Distribution by Meal Type")
fig2.update_traces(textinfo='label+percent')
st.plotly_chart(fig2, use_container_width=True)

# Visualization: Student Absence by Day and Meal Type
st.subheader("Student Absence by Day and Meal Type")
fig3 = px.bar(filtered_absent, x="day", y="student_absent_%", color="meal_type", 
              title="Student Absence Percentage by Day and Meal Type", template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)

# Visualization: Waste Volume by Hostel
st.subheader("Waste Volume by Hostel")
fig4 = px.bar(filtered_hostel, x="Hostel", y="waste_in_kg", 
              title="Total Waste Volume by Hostel", template="plotly_dark")
st.plotly_chart(fig4, use_container_width=True)

# Download filtered data
cl1, cl2, cl3 = st.columns(3)
with cl1:
    with st.expander("Download Day-Meal Waste Data"):
        csv1 = filtered_waste.to_csv(index=False).encode('utf-8')
        st.download_button("Download Day-Meal Waste Data", data=csv1, 
                          file_name="Day_Meal_Waste_Data.csv", mime="text/csv")

with cl2:
    with st.expander("Download Student Absence Data"):
        csv2 = filtered_absent.to_csv(index=False).encode('utf-8')
        st.download_button("Download Student Absence Data", data=csv2, 
                          file_name="Student_Absence_Data.csv", mime="text/csv")

with cl3:
    with st.expander("Download Hostel Waste Data"):
        csv3 = filtered_hostel.to_csv(index=False).encode('utf-8')
        st.download_button("Download Hostel Waste Data", data=csv3, 
                          file_name="Hostel_Waste_Data.csv", mime="text/csv")

# Time Series Analysis
st.subheader("Time Series Analysis of Waste Volume")
filtered_waste["Date"] = pd.to_datetime(filtered_waste["Date"])
linechart = filtered_waste.groupby("Date")["waste_in_kg"].sum().reset_index()
fig5 = px.line(linechart, x="Date", y="waste_in_kg", 
               title="Daily Waste Volume", template="plotly_dark")
st.plotly_chart(fig5, use_container_width=True)

with st.expander("View Time Series Data"):
    st.write(linechart.style.background_gradient(cmap="Blues"))
    csv4 = linechart.to_csv(index=False).encode('utf-8')
    st.download_button('Download Time Series Data', data=csv4, 
                      file_name="Time_Series_Waste_Data.csv", mime="text/csv")

# Hierarchical View of Waste
st.subheader("Hierarchical View of Waste")
fig6 = px.treemap(filtered_waste, path=["day", "meal_type"], values="waste_in_kg", 
                  color="waste_in_kg", title="Waste Volume Hierarchy", template="plotly_dark")
fig6.update_layout(width=800, height=600)
st.plotly_chart(fig6, use_container_width=True)

# Scatter Plot for Waste Volume vs. Student Absence
st.subheader("Waste Volume vs. Student Absence")
merged_df = filtered_waste.merge(filtered_absent, on=["day", "meal_type", "Date"], how="inner")
fig7 = px.scatter(merged_df, x="waste_in_kg", y="student_absent_%", 
                  size="waste_in_kg", color="meal_type", hover_name="day", 
                  title="Waste Volume vs. Student Absence", template="plotly_dark")
st.plotly_chart(fig7, use_container_width=True)

# Download original datasets
st.subheader("Download Original Datasets")
col4, col5, col6 = st.columns(3)
with col4:
    csv_waste = df_waste.to_csv(index=False).encode('utf-8')
    st.download_button("Download Original Day-Meal Waste Data", data=csv_waste, 
                      file_name="Original_Day_Meal_Waste.csv", mime="text/csv")
with col5:
    csv_absent = df_absent.to_csv(index=False).encode('utf-8')
    st.download_button("Download Original Student Absence Data", data=csv_absent, 
                      file_name="Original_Student_Absence.csv", mime="text/csv")
with col6:
    csv_hostel = df_hostel.to_csv(index=False).encode('utf-8')
    st.download_button("Download Original Hostel Waste Data", data=csv_hostel, 
                      file_name="Original_Hostel_Waste.csv", mime="text/csv")