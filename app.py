import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go


# Reading the data from excel file

df = pd.read_excel('Adidas.xlsx')

st.set_page_config(layout='wide')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

image = Image.open('adidas-logo.jpg')


col1, col2 = st.columns([0.1,0.9])

with col1:
    st.image(image, use_column_width=True)
    
    
html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class='title-test'>Adidas Interactive Sales Dashboard</h1></center>"""
    
with col2:
    st.markdown(html_title, unsafe_allow_html=True)
    
    
col3,col4,col5 = st.columns([0.1,0.45,0.45])

with col3:
    box_date = str(datetime.datetime.now().strftime("%d-%B-%Y"))
    st.markdown(f'<center>Last updated:<br>{box_date}</center>', unsafe_allow_html=True)
    #st.write(f'Last updated: \n {box_date}')
    
with col4:
    fig = px.bar(df, x="Retailer", y="TotalSales", labels={'TotalSales':'Total Sales {$}'},
                 title='Total Sales by Retailer',hover_data=['TotalSales'],
                 template='gridon',height=500)
    
    st.plotly_chart(fig, use_container_width=True)
    
_,view1,dwn1,view2,dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])

with view1:
    expander = st.expander("Retailer wise Sales")
    data = df[["Retailer","TotalSales"]].groupby(by='Retailer')['TotalSales'].sum()
    expander.write(data)
    
with dwn1:
    st.download_button(
        label="Download",
        data=data.to_csv(),
        file_name="RetailerWiseSales.csv",
        mime="text/csv",
    )
    
df['Month_Year'] = df['InvoiceDate'].dt.strftime("%b-%Y")
result = df.groupby(by=df['Month_Year'])['TotalSales'].sum().reset_index()
      
with col5:
    fig1 = px.line(result, x="Month_Year", y="TotalSales", labels={'TotalSales':'Total Sales {$}'},
                 title='Total Sales over Time',
                 template='gridon',height=500)
    
    st.plotly_chart(fig1, use_container_width=True)
    
with view2:
    expander = st.expander('Monthly Sales')
    expander.write(result)
    
with dwn2:
    st.download_button(
        label="Download",
        data=result.to_csv(),
        file_name="Monthly Sales.csv",
        mime="text/csv",
    )
    
st.divider()


result1 = df.groupby(by='State')[['TotalSales','UnitsSold']].sum().reset_index()

# Add the units sold as line chart on a secondary y-axis

fig2 = go.Figure()

fig2.add_trace(go.Bar(x=result1['State'], y=result1['TotalSales'], name = 'Total Sales'))
fig2.add_trace(go.Scatter(x=result1['State'], y=result1['UnitsSold'], name ='Units Sold', mode='lines', yaxis='y2'))

fig2.update_layout(
    
    title ='Total Sales & Units Sold by State',
    xaxis=dict(title='State'),
    yaxis=dict(title='Total Sales',showgrid=False),
    yaxis2=dict(title='Units Sold',overlaying='y',side='right'),
    template ='gridon',
    legend=dict(x=1,y=1))

_, col6 = st.columns([0.1,1])

with col6:
    st.plotly_chart(fig2, use_container_width=True)
    
_, view3, dwn3 = st.columns([0.5,0.45,0.45])

with view3:
    expander = st.expander("Sales & Units Sold by State")
    expander.write(result1)
    
with dwn3:
    st.download_button(
        label="Download",
        data=result1.to_csv().encode('utf-8'),
        file_name="Sales & Units Sold by State.csv",
        mime="text/csv",
    )
    
st.divider()

_, col7 = st.columns([0.1,1.1])

treemap = df[['Region','City','TotalSales']].groupby(by=['Region','City'])['TotalSales'].sum().reset_index()

def format_sales(value):
    if value>=0:
        return '{:.2f} Lakh'.format(value/1_000_00)
    
treemap['TotalSales (Formatted)'] = treemap['TotalSales'].apply(format_sales)

fig3 = px.treemap(treemap, path=['Region','City'], values='TotalSales', color='City',
                   color_continuous_scale=px.colors.cyclical.IceFire,
                   hover_data=['Region','City','TotalSales (Formatted)'],
                   labels={'TotalSales':'Total Sales {$}'},height=700,width=600)

fig3.update_traces(textinfo='label+value')

with col7:
    st.subheader(':point_right: Total Sales by Region & City in Treemap')
    st.plotly_chart(fig3, use_container_width=True)
    
_, view4, dwn4 = st.columns([0.5,0.45,0.45])

with view4:
    expander = st.expander("Total Sales by Region & City")
    expander.write(treemap)
    
with dwn4:
    st.download_button(label="Download", data=treemap.to_csv().encode('utf-8'),
                       file_name='Total Sales by Region & City.csv',
                       mime='text/csv')


st.divider()

_, view5, dwn5 = st.columns([0.5,0.45,0.45])

with view5:
    expander = st.expander('View Sales Raw Data')
    expander.write(df)
    
with dwn5:
    st.download_button(label="Download Raw Data", data=df.to_csv().encode('utf-8'),
                       file_name='Sales Raw Data.csv',
                       mime='text/csv')