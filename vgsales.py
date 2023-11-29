import pandas as pd, numpy as np
import streamlit as st
import altair as alt
from urllib.error import URLError

@st.cache_data
def get_data():
    path_ = "datasets/vgsales.csv"
    df = pd.read_csv(path_)
    # Dropping null values from Year and Publisher
    df.dropna(inplace = True)
    df.Year=df.Year.astype('str')
    df.Year=df.Year.str.replace('.0','')
    return df

try:
    df = get_data()
    """ # Video games sales analysis"""
    # The "#" tells streamlit to read the text as a markdown or a title.
    # Another way to do this is to send the text into streamlit .title object as in:
    st.title("A table created by Kolawole.")

    # Total sales metrics
    """ # Sales Metrics"""
    global_sales = np.round(np.sum(df['Global_Sales']), 2)
    eu_sales = np.round(np.sum(df["EU_Sales"]), 2)
    na_sales = np.round(np.sum(df['NA_Sales']), 2)
    jp_sales = np.round(np.sum(df['JP_Sales']), 2)
    othersales = np.round(np.sum(df['Other_Sales']), 2)

    # Create columns
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    # Create card
    col1.metric("Global_Sales Total", global_sales,"USD")
    col2.metric("North America Sales Total", na_sales,"USD")
    col3.metric("European Sales Total", eu_sales,"USD")
    col4.metric("Japan Sales Total", jp_sales,"USD")
    col5.metric("Other Sales Total", othersales,"USD")

    
    st.write("Select a Platform and Genre")

    # Creating filters for Platfrom column
    col6, col7 = st.columns(2)
    platforms = df['Platform'].unique() #To send the unique values in the 'Platform column to variable named "platforms"
    selected_platforms = col6.multiselect(
        "Select from Platform here", platforms, [platforms[0], platforms[1]]
    )

    # Creating filters for Genre column
    genre = df['Genre'].unique()
    selected_genre = col7.multiselect(
        "Select Genre here", genre, [genre[0], genre[1]]
    )

    filtered_data = df[df['Platform'].isin(selected_platforms) & df['Genre'].isin(selected_genre)]

    if not selected_genre and selected_platforms:
        st.write("Please select from filters above to filter table.")
    else:
        # filtered table
        """Filtered result obtained"""

    # The top 10
    """# Top 10 Platforms Chart"""
    bar0 = df.groupby(["Platform"])["Global_Sales"].sum().nlargest(n=10).sort_values(ascending = False)
    st.write(bar0)
    st.bar_chart(bar0, color = '#d4af37')

    # USING FILTERED RESULT TO PLOT A BAR CHART
    st.write(" ## Global Sales per Platform")
    bar1 = filtered_data.groupby(["Platform"])["Global_Sales"].sum().sort_values(ascending = True)
    st.write(bar1)
    st.bar_chart(bar1, color = '#d4af37')

    # USING FILTERED DATA TO PLOT A LINE CHART
    """ ## Global Sales Over Time(Line Chart)"""
    chart = (
        alt.Chart(filtered_data.head())
        .mark_line(opacity = 0.3)
        .encode(
            x = "Year",
            y = alt.Y("Global_Sales", stack=None)
        )
    )

    st.altair_chart(chart, use_container_width=True)


    # USING FILTERED DATA TO PLOT AN AREA CHART
    """ ## Global Sales Over Time (Area Chart)"""
    chart = (
        alt.Chart(filtered_data.head())
        .mark_area(opacity = 0.3)
        .encode(
            x = "Year",
            y = alt.Y("Global_Sales", stack=None)
        )
    )
    st.altair_chart(chart, use_container_width=True)

    # st.write(df)
    # countries = st.multiselect(
    #     "Choose countries", list(df.index), ["China", "United States of America"]
    # )
    # if not countries:
    #     st.error("Please select at least one country.")
    # else:
    #     data = df.loc[countries]
    #     data /= 1000000.0
    #     st.write("### Gross Agricultural Production ($B)", data.sort_index())

    #     data = data.T.reset_index()
    #     data = pd.melt(data, id_vars=["index"]).rename(
    #         columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
    #     )
    #     chart = (
    #         alt.Chart(data)
    #         .mark_area(opacity=0.3)
    #         .encode(
    #             x="year:T",
    #             y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
    #             color="Region:N",
    #         )
    #     )
    #     st.altair_chart(chart, use_container_width=True)
        
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )