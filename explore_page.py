import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import pydeck as pdk
import matplotlib as mpl



def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2020
    """
    )

    data = df["Country"].value_counts()
    
    fig1, ax1 = plt.subplots()
    
    ax1.pie(data, labels=data.index, shadow=False, startangle=90,radius=0.1, textprops={'fontsize': 6})
    
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1,shadow=False, height=600.9, width=80.5)
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data, height=600.9, width=80.5)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data, height=600.9, width=80.5)
    
    st.title("Explore Developers Salaries across Europe")

    st.write("""
    ### Median Salaries by Country
    """)
    data1 = df.groupby(["Country"])["Salary"].median().sort_values(ascending=True)
    st.bar_chart(data1, height=700.9, width=90.5)
    
    st.write(""" ### Median Salary Based on Experience""")
    data= df.groupby(["YearsCodePro"])["Salary"].median().sort_values(ascending=True)
    st.line_chart(data, height=600.9, width=80.5)

    st.write(""" ### Median Salary Based on Education""")
    data4 = df.groupby(["EdLevel"])["Salary"].median().sort_values (ascending = True)
    st.bar_chart(data4, height=600.9, width=80.5)
    
    st.write(""" ### State wise job postings on handshake during 2020-21""")
    data5 = {'state': ['New York','California', 'District of Columbia', 'New Jersey', 'Massachusetts', 'Texas',
                  'Washington', 'Virginia', 'Maryland', 'Illinois', 'North Carolina',
                  'Georgia', 'Connecticut', 'Florida', 'Pennsylvania', 'Ohio', 
                  'Rhode Island', 'Colorado', 'Wisconsin', 'Minnesota', 'Utah', 
                  'Maine', 'Michigan', 'West Virginia', 'Vermont', 'Oregon', 'Arizona', 
                  'Indiana', 'Nebraska', 'Iowa', 'New Hampshire', 'Tennessee', 
                  'Kentucky', 'South Dakota', 'Idaho', 'Mississippi', 'Alabama', 
                  'Nevada'],
        'count': [140,59, 52, 41, 34, 24, 23, 19, 19, 18, 17, 14, 12, 12, 11, 8, 7, 
                  7, 7, 6, 5, 5, 5, 4, 4, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1]
        }


    df5 = pd.DataFrame(data5)
    st.bar_chart(df5.set_index('state'))
    
    

    df6 = pd.read_csv("test.csv")
    
    
    

