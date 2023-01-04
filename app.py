import streamlit as st
import pandas as pd

st.set_page_config(layout='wide',page_title='Startup Analysis')
#Importing Dataset
df=pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'])

# More cleaning
df['investors']=df['investors'].apply(lambda x:'undisclosed' if x=='' else x)
df['vertical']=df['vertical'].str.replace('E-Commerce','ECommerce')
df['vertical']=df['vertical'].str.replace('eCommerce','ECommerce')
df['vertical']=df['vertical'].str.replace('E-commerce','ECommerce')

df['round']=df['round'].str.replace('Seed/ Angel Funding','Seed Funding')
df['round']=df['round'].str.replace('Seed / Angel Funding','Seed Funding')
df['round']=df['round'].str.replace('Seed/Angel Funding','Seed Funding')

df['city']=df['city'].str.replace('Bengaluru','Bangalore')

#Function for overall analysis----------------------------------------------------------------------------------------
def load_startup_analysis(startup):
    st.title(startup)
    investment=round(df[df['startup']==startup]['amount'].sum(),2)
    string='Undisclosed' if investment==0.00 else str(investment)+ " " + "Cr"   #replacing i=0.00investment with undixclosed string
    st.metric('Total investment', string)   #Metric
    #verical
    st.subheader("Industry Working In:")
    st.write(','.join(df[df['startup']==startup]['vertical'].unique()))
    #dont use sub industry now as it has so many missing values
    #st.subheader('Subindustry:')
    #st.text(','.join(df[df['startup']==startup]['subvertical'].values))
    #Lovcation
    st.subheader('Location:')
    st.write(','.join(df[df['startup'] == startup]['city'].unique()))
    #Funding Round Details
    st.subheader('Funding Rounds')
    df['date']=df['date'].dt.date
    st.dataframe(df[df['startup']==startup][['date','investors','round','amount']].sort_values('date'))
    #simillar startup details
    st.subheader('Simillar Startups')
    df1=df[df['vertical'].isin(df[df['startup']==startup]['vertical'].values)]
    #df1 = df1[df1['subvertical'].isin(df[df['startup'] == startup]['subvertical'].values)] (so many values are nan so dont use it now)
    simillar=sorted(df1[df1['startup']!=startup]['startup'].unique())
    st.dataframe(simillar)

#Function for overall analysis-----------------------------------------------------------------------------------------------------------------------
def load_overall_analysis():
   #Matrics
    col0,col1, col2, col3 = st.columns(4)
    with col0:
        total_amt_invested=round(df['amount'].sum(),2)
        st.metric('Total',str(total_amt_invested)+" "+"Cr")
    with col1:
        max_amt=df.groupby('startup')['amount'].max().sort_values(ascending=False).values[0]
        st.metric('max_amt',str(max_amt)+" "+"Cr")
    with col2:
        avg_amt=df.groupby('startup')['amount'].sum().mean()
        st.metric('avg_amt',str(round(avg_amt,2))+" "+"Cr")
    with col3:
        funded_startups=df['startup'].nunique()
        st.metric('funded_startups',str(funded_startups))

   #Total deals
    st.subheader('Total Deals')
    st.write('''
        Usage of internet has been incresed in India.This is because many things are going online such as 
        online Education, ECommerce, Online Banking etc.That is a reson investment deal for consumer internet
        is the most. 
        ''')
    col1,col2=st.columns(2)
    with col1:
        vert_count=df['vertical'].value_counts().head(5)
        fig1, ax1 = plt.subplots()
        ax1.pie(vert_count, labels=vert_count.index, autopct='%0.01f%%')
        st.pyplot(fig1)

    #Total Funding
    st.subheader('Total Funding')
    st.write('''
        In the sapn of 2015-2020 ECommerce based startup has got highest total funding of 65,640.5cr 
        ''')
    col1,col2=st.columns(2)
    with col1:
        vert_amt=round(df.groupby('vertical')['amount'].sum().sort_values(ascending=False), 2).head(5)
        vert_amt=vert_amt.reset_index().sort_values('amount')
        fig1, ax1 = plt.subplots()
        ax1.barh(vert_amt['vertical'],vert_amt['amount'],color='green')
        st.pyplot(fig1)
        #st.dataframe(vert_amt)

    #Type of investment
    col1, col2=st.columns(2)
    with col1:
        st.subheader('Type of Investment')
        rounds_series=df['round'].value_counts().reset_index().rename(columns={'index':'Investment Type','round':'Total Count'}).head(3)
        st.dataframe(rounds_series)
        fig1, ax1 = plt.subplots()
        ax1.pie(rounds_series['Total Count'], labels=rounds_series['Investment Type'], autopct='%0.01f%%')
        my_circle = plt.Circle((0, 0), 0.7, color='white')
        p = plt.gcf()
        p.gca().add_artist(my_circle)
        st.pyplot(fig1)

    #Geography
    st.subheader('Geography')
    st.write('''
    startups that come from Bangalore have a higher probability of upgrading to a Unicorn because of
    Amazing tech brains, innovative ideas and Goverment support.
    ''')
    st.write('''
    That is reason Banglore has become a startup hub in india and almost 832 startups have got 
    total investment of 152,118.92 Cr which is highest as compare other cities''')
    city_df = df.groupby(['city']).agg({'startup': 'count', 'amount': 'sum'})
    city_df = city_df.sort_values('startup', ascending=False).head(10).reset_index()
    city_df = city_df.rename(columns={'startup': 'No of Investment'})
    city_df['amount'] = city_df['amount'].apply(lambda x: round(x, 2))
    #st.dataframe(city_df)
    city_df=city_df.sort_values('No of Investment')
    col1,col2=st.columns(2)
    with col1:
        st.subheader('Deals')
        fig1, ax1 = plt.subplots()
        ax1.barh(city_df['city'], city_df['No of Investment'], color='blue')
        st.pyplot(fig1)
    with col2:
        st.subheader('Total Fundings')
        fig1, ax1 = plt.subplots()
        ax1.barh(city_df['city'], city_df['amount'], color='skyblue')
        st.pyplot(fig1)

    #Top Startups
    st.subheader("Top Startups")
    st.write('We can see here most of the top startups are based on online services')
    col1,col2=st.columns(2)
    with col1:
        df['startup'] = df['startup'].str.replace('Flipkart.com', 'Flipkart')
        top_startup=df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        top_startup=top_startup.reset_index()
        fig1, ax1 = plt.subplots()
        ax1.bar(top_startup['startup'],top_startup['amount'],color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig1)

   #Year Wise Top Startups
    col1,col2=st.columns(2)
    with col1:
        st.subheader('Year Wise Top Startups')
        df['year']=df['date'].dt.year
        year_wise = df.groupby(['year', 'startup'])['amount'].sum().reset_index().sort_values('amount',ascending=False).drop_duplicates('year')
        year_wise=year_wise.sort_index()
        year_wise['index']=year_wise['year'].apply(lambda x:str(x)) + '-' + year_wise['startup']
        #st.dataframe(year_wise[['index','amount']])
        fig1, ax1 = plt.subplots()
        ax1.bar(year_wise['index'], year_wise['amount'],color='grey')
        plt.xticks(rotation='vertical')
        st.pyplot(fig1)

    #Top Investors
    st.subheader('Top Investors')
    st.write("Westbridge Capital has invested highest amount of 32175Cr in Rapido Bike Taxi")
    top_investors=df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(10)
    top_investors=top_investors.reset_index().set_index('investors')
    #st.dataframe(top_investors)
    st.bar_chart(top_investors)

#Function for investors analysis
def load_investors_details(investor):
    st.subheader(investor)
    st.write('Recent Investment')
    recent_df=df[df['investors'].str.contains(investor)].head()[['startup', 'vertical', 'round', 'amount']] #recent investment
    st.dataframe(recent_df.sort_values('amount',ascending=False))
    #grouping all startups invested by investor
    big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)

    #Biggest Investment
    col1,col2=st.columns(2)
    with col1:
        st.subheader('Biggest Investment')
        fig,ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        vertical_df=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending=False).head()
        st.subheader("Sectors Invested In")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_df,labels=vertical_df.index,autopct='%0.01f%%')
        st.pyplot(fig1)

    #YOY investment
    col3,col4=st.columns(2)
    with col3:
        df['year'] = df['date'].dt.year
        year_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum().head(5)
        st.subheader("YOY investment")
        fig2, ax2 = plt.subplots()
        sizes = year_series.values
        ax2.scatter(year_series.index, year_series.values, s=sizes, alpha=0.5)
        plt.xticks(rotation='vertical')
        st.pyplot(fig2)
    #Funding stage
    with col4:
        stage_df = df[df['investors'].str.contains(investor)]
        stage_df=stage_df.groupby('round')['startup'].count()
        st.subheader("Funding Stage")
        fig3, ax3 = plt.subplots()
        ax3.pie(stage_df,labels=stage_df.index, autopct='%0.01f%%')
        st.pyplot(fig3)

    #Cities Startup Belongs to
    col5,col6=st.columns(2)
    with col5:
        city_df = df[df['investors'].str.contains(investor)]
        city_series=city_df.groupby(['city'])['startup'].count().sort_values(ascending=False)
        st.subheader("Cities Startup Belongs to")
        fig5, ax5 = plt.subplots()
        ax5.pie(city_series, labels=city_series.index, autopct='%0.01f%%')
        st.pyplot(fig5)

    #similar investores
    st.subheader('Simillar Investores')
    vertical_of_inv = df[df['investors'].str.contains(investor)]['vertical'].unique()
    df1 = df
    df1=df1[df1['vertical'].isin(list(vertical_of_inv))]
    df1=df1[df1['investors']!=investor]
    investores_series=pd.Series(sorted(df1['investors'].unique())).reset_index()
    st.dataframe(investores_series.rename(columns={0:'investores'}))
#-----------------------------------------------------------------
#side bar
st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select one',['Overall Analysis','Startup','Investor'])
#overall analysis
if option=='Overall Analysis':
    btn0=st.sidebar.button('Show Analysis')
    st.title('Overall Analysis 2015-20')
    if btn0:
        load_overall_analysis()
#startup analysis
elif option=='Startup':
    selected_startup=st.sidebar.selectbox('Startup Name',sorted(df['startup'].unique()))
    st.title('Startup Analysis 2015-20')
    btn1=st.sidebar.button('Find Startup Detail')
    load_startup_analysis(selected_startup)
#Investors Analysis
else:
    selected_investor=st.sidebar.selectbox("Investor's Name",sorted(df['investors'].astype(str).str.split(',').sum())[60:])
    st.title('Investor Analysis 2015-20')
    btn2 = st.sidebar.button("Find Investor's Detail")
    if btn2:
        load_investors_details(selected_investor)



