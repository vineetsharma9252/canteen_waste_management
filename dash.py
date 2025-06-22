import pandas as pd
import streamlit as st
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title='Waste Management Dashboard', page_icon=":recycle:", layout="wide")
st.title(":recycle: Waste Management Dashboard")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

def load_data():
    return pd.read_csv('indian_state_geodata_waste.csv')

df = load_data()

df['Date'] = pd.to_datetime(df['Date'])
startdate = df['Date'].min()
enddate = df['Date'].max()

col1, col2 = st.columns(2)
with col1:
    date1 = st.date_input("Start Date", startdate)
with col2:
    date2 = st.date_input("End Date", enddate)

df = df[(df['Date'] >= pd.to_datetime(date1)) & (df['Date'] <= pd.to_datetime(date2))]

st.sidebar.header("Filters")
state = st.sidebar.multiselect("Select State", df["State"].unique(), default=df["State"].unique())
meal_type = st.sidebar.multiselect("Select Meal Type", ["Breakfast", "Lunch", "Dinner"], default=["Breakfast", "Lunch", "Dinner"])

filtered_df = df[df["State"].isin(state) & df["Meal_Type"].isin(meal_type)]

st.subheader("Waste Volume by State")
fig1 = px.bar(filtered_df, x="State", y="Volume", color="Meal_Type", title="Total Waste Volume by State", template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Distribution of Meal Types")
fig2 = px.pie(filtered_df, names="Meal_Type", values="Volume", hole=0.4, title="Meal Type Distribution")
fig2.update_traces(textinfo='label+percent')
st.plotly_chart(fig2, use_container_width=True)

cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Download Waste Volume Data"):
        csv1 = filtered_df.groupby('State').agg({"Volume": "sum"}).reset_index().to_csv(index=False).encode('utf-8')
        st.download_button("Download Waste Volume Data", data=csv1, file_name="Waste_Volume_Data.csv", mime="text/csv")

with cl2:
    with st.expander("Download Meal Type Data"):
        csv2 = filtered_df.groupby('Meal_Type').agg({"Volume": "sum"}).reset_index().to_csv(index=False).encode('utf-8')
        st.download_button("Download Meal Type Data", data=csv2, file_name="Meal_Type_Data.csv", mime="text/csv")

st.subheader("Time Series Analysis of Waste Volume")
filtered_df["Month"] = filtered_df["Date"].dt.to_period("M").dt.to_timestamp()
linechart = filtered_df.groupby("Month")["Volume"].sum().reset_index()
fig3 = px.line(linechart, x="Month", y="Volume", title="Monthly Waste Volume", template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)

with st.expander("View Time Series Data"):
    st.write(linechart.style.background_gradient(cmap="Blues"))
    csv3 = linechart.to_csv(index=False).encode('utf-8')
    st.download_button('Download Time Series Data', data=csv3, file_name="Time_Series_Data.csv", mime="text/csv")

st.subheader("Hierarchical View of Meal Types")
fig4 = px.treemap(filtered_df, path=["State", "Meal_Type"], values="Volume", color="Volume", title="Waste Volume Hierarchy", template="plotly_dark")
fig4.update_layout(width=800, height=600)
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Waste Volume vs. Meal Type")
fig5 = px.scatter(filtered_df, x="Volume", y="Meal_Type", size="Volume", color="Meal_Type", hover_name="State", title="Volume vs. Meal Type", template="plotly_dark")
st.plotly_chart(fig5, use_container_width=True)

# Load new datasets
df_waste = pd.read_csv('day_meal_type_waste.csv')
df_absent = pd.read_csv('day_meal_type_absent.csv')
df_hostel = pd.read_csv('hostel_waste.csv')

# Simulate Date column for day_meal_type datasets
date_range = pd.date_range(start="2025-06-09", end="2025-06-15")  # One week
days = df_waste['day'].unique()
day_to_date = {day: date for day, date in zip(days, date_range)}
df_waste['Date'] = df_waste['day'].map(day_to_date)
df_absent['Date'] = df_absent['day'].map(day_to_date)

# Visualization: Waste Volume by Day and Meal Type
st.subheader("Canteen Waste by Day and Meal Type")
fig6 = px.bar(df_waste, x="day", y="waste_in_kg", color="meal_type", 
              title="Total Canteen Waste by Day and Meal Type", template="plotly_dark")
st.plotly_chart(fig6, use_container_width=True)

# Visualization: Student Absence by Day and Meal Type
st.subheader("Student Absence by Day and Meal Type")
fig7 = px.bar(df_absent, x="day", y="student_absent_%", color="meal_type", 
              title="Student Absence Percentage by Day and Meal Type", template="plotly_dark")
st.plotly_chart(fig7, use_container_width=True)

# Visualization: Waste Volume by Hostel
st.subheader("Waste Volume by Hostel")
fig8 = px.bar(df_hostel, x="Hostel", y="waste_in_kg", 
              title="Total Waste Volume by Hostel", template="plotly_dark")
st.plotly_chart(fig8, use_container_width=True)

# Visualization: Waste Volume vs. Student Absence
st.subheader("Canteen Waste vs. Student Absence")
merged_df = df_waste.merge(df_absent, on=["day", "meal_type", "Date"], how="inner")
fig9 = px.scatter(merged_df, x="waste_in_kg", y="student_absent_%", 
                  size="waste_in_kg", color="meal_type", hover_name="day", 
                  title="Canteen Waste vs. Student Absence", template="plotly_dark")
st.plotly_chart(fig9, use_container_width=True)

csv_original = df.to_csv(index=False).encode('utf-8')
st.download_button("Download Original Dataset", data=csv_original, file_name="Waste_Data.csv", mime="text/csv")

st.subheader("Geographical Map of Waste Collection")
fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    hover_name="State",
    hover_data=["Meal_Type", "Volume", "Date"],
    color="Meal_Type",
    size="Volume",
    zoom=16,
    height=600,
    title="<b>Waste Collection by Hostel</b>"
)

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox=dict(
        center=dict(lat=26.1885, lon=91.6916),  
        zoom=16 
    ),
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    hovermode='closest'
)

fig.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "Meal Type: %{customdata[0]}<br>"
        "Volume: %{customdata[1]} kg<br>"
        "Date: %{customdata[2]}<extra></extra>"
    )
)
st.plotly_chart(fig, use_container_width=True)