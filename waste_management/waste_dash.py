import pandas as pd
import streamlit as st
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

# Set up the Streamlit page
st.set_page_config(page_title='Waste Management Dashboard', page_icon=":recycle:", layout="wide")
st.title(":recycle: Waste Management Dashboard")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

# Load fixed dataset
@st.cache
def load_data():
    return pd.read_csv('indian_state_geodata_waste.csv')

df = load_data()

# Date conversion and filters
df['Date'] = pd.to_datetime(df['Date'])
startdate = df['Date'].min()
enddate = df['Date'].max()

col1, col2 = st.columns(2)
with col1:
    date1 = st.date_input("Start Date", startdate)
with col2:
    date2 = st.date_input("End Date", enddate)

df = df[(df['Date'] >= pd.to_datetime(date1)) & (df['Date'] <= pd.to_datetime(date2))]

# Sidebar filters
st.sidebar.header("Filters")
state = st.sidebar.multiselect("Select State", df["State"].unique(), default=df["State"].unique())
waste_type = st.sidebar.multiselect("Select Waste Type", df["Waste_Type"].unique(), default=df["Waste_Type"].unique())

filtered_df = df[df["State"].isin(state) & df["Waste_Type"].isin(waste_type)]

# Visualization: Waste Volume by State
st.subheader("Waste Volume by State")
fig1 = px.bar(filtered_df, x="State", y="Volume", color="Waste_Type", title="Total Waste Volume by State", template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# Visualization: Waste Type Distribution
st.subheader("Distribution of Waste Types")
fig2 = px.pie(filtered_df, names="Waste_Type", values="Volume", hole=0.4, title="Waste Type Distribution")
fig2.update_traces(textinfo='label+percent')
st.plotly_chart(fig2, use_container_width=True)

# Download filtered data
cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Download Waste Volume Data"):
        csv1 = filtered_df.groupby('State').agg({"Volume": "sum"}).reset_index().to_csv(index=False).encode('utf-8')
        st.download_button("Download Waste Volume Data", data=csv1, file_name="Waste_Volume_Data.csv", mime="text/csv")

with cl2:
    with st.expander("Download Waste Type Data"):
        csv2 = filtered_df.groupby('Waste_Type').agg({"Volume": "sum"}).reset_index().to_csv(index=False).encode('utf-8')
        st.download_button("Download Waste Type Data", data=csv2, file_name="Waste_Type_Data.csv", mime="text/csv")

# Time Series Analysis
st.subheader("Time Series Analysis of Waste Volume")
filtered_df["Month"] = filtered_df["Date"].dt.to_period("M").dt.to_timestamp()
linechart = filtered_df.groupby("Month")["Volume"].sum().reset_index()
fig3 = px.line(linechart, x="Month", y="Volume", title="Monthly Waste Volume", template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)

with st.expander("View Time Series Data"):
    st.write(linechart.style.background_gradient(cmap="Blues"))
    csv3 = linechart.to_csv(index=False).encode('utf-8')
    st.download_button('Download Time Series Data', data=csv3, file_name="Time_Series_Data.csv", mime="text/csv")

# Hierarchical View of Waste Types
st.subheader("Hierarchical View of Waste Types")
fig4 = px.treemap(filtered_df, path=["State", "Waste_Type"], values="Volume", color="Volume", title="Waste Volume Hierarchy", template="plotly_dark")
fig4.update_layout(width=800, height=600)
st.plotly_chart(fig4, use_container_width=True)

# Scatter Plot for Waste Volume vs. Waste Type
st.subheader("Waste Volume vs. Waste Type")
fig5 = px.scatter(filtered_df, x="Volume", y="Waste_Type", size="Volume", color="Waste_Type", hover_name="State", title="Volume vs. Waste Type", template="plotly_dark")
st.plotly_chart(fig5, use_container_width=True)

# Download original dataset
csv_original = df.to_csv(index=False).encode('utf-8')
st.download_button("Download Original Dataset", data=csv_original, file_name="Waste_Data.csv", mime="text/csv")

# Geographical Map of Waste Collection
st.subheader("Geographical Map of Waste Collection")
fig_geo = px.scatter_geo(filtered_df,
                        lat='Latitude',
                        lon='Longitude',
                        hover_name='State',
                        size='Volume',
                        color='Volume',
                        projection='natural earth',
                        title="Geographical Distribution of Waste Collection")
st.plotly_chart(fig_geo, use_container_width=True)
