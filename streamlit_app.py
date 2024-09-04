import streamlit as st
import pandas as pd
import boto3
from io import BytesIO


# Function to load data from S3
def load_data_from_s3(bucket, key, access_key, secret_key):
    """Load a DataFrame from a CSV file on S3."""
    session = boto3.Session(
        aws_access_key_id=access_key, aws_secret_access_key=secret_key
    )
    s3 = session.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response["Body"].read()
    df = pd.read_csv(BytesIO(content))
    return df


## Set up constants for S3 access
BUCKET_NAME = "electric-vehicle-bucket"
AWS_ACCESS_KEY_ID = st.secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = st.secrets["AWS_SECRET_ACCESS_KEY"]

st.set_page_config(
    page_title="Electric Vehicles Data - WA",
    page_icon=":electric_plug:",
    initial_sidebar_state="auto",
)

st.title("Electric Vehicles Data - Trends in Washington")

## Inject custom CSS to set the width of the sidebar
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 600px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("About This App")
    st.text(
        """
        This application provides simple analysis of trends in 
        electric vehicle usage across various model years and makes
        in Washington. The data is sourced from Data.gov.
        
        Key Features:
        - Yearly trends of electric vehicle counts.
        - Breakdown by make.
        - Interactive selection to filter data by make.

        Technologies Used:
        - CI/CD with GitHub Actions.
        - Analysis with dbt and DuckDB.
        - Data visualizations using Streamlit.
        - Data stored in S3 objects from a dbt pipeline.
        
        Developed by Thiago Bellotto.
    """
    )

## Display a line chart to show trends
st.subheader("Yearly Electric Vehicle Trends")

## Load the data
yearly_trend = load_data_from_s3(
    BUCKET_NAME, "yearly_trend.csv", AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
)

make_trend = load_data_from_s3(
    BUCKET_NAME, "make_trend_by_model.csv", AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
)

st.line_chart(
    yearly_trend.set_index("model_year"),
    use_container_width=True,
    x_label="Year",
    y_label="Number of Electric Vehicles",
)

## Divider
st.markdown("---")

## Dynamic selectbox for filtering by make
make = st.selectbox(
    "Select a make to show yearly count per model:", sorted(make_trend["make"].unique())
)
filtered_data = make_trend[make_trend["make"] == make]
st.dataframe(filtered_data, width=10000, hide_index=True)

footer = """<style>
a:link , a:visited{
color: white;
background-color: transparent;
text-decoration: underline;
}
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; color: white; text-align: center;' href="https://www.linkedin.com/in/thiago-bellotto/" target="_blank">Thiago Bellotto</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

st.markdown(
    """ <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """,
    unsafe_allow_html=True,
)
