import streamlit as st
import pandas as pd

st.title('Startup Dashboard')
st.header('Team Phoenix Racing')
st.subheader('President & CEO Mr.Rajesh Khangar')
st.write('This is the most sucessful automobile compony till the date')
st.markdown("""
### Sectors working in
- Autonomous Vehicle
- Offroad
- F1 team
""")

st.code("""
def km_to_mph(speed)
  return speed/1.5
""")
st.latex('x^2+y^2=0')
st.metric('Revenue','Rs 400 cr','+90 %')
df=pd.DataFrame({'Investor':['FDC','Saguna Baugh','Mopar'],'Invested amt':[5000000,2000000,10000000]})
st.dataframe(df)
st.json({'Investor':['FDC','Saguna Baugh','Mopar'],'Invested amt':[5000000,2000000,10000000]})
st.sidebar.title('History of Team Phoenix Racing')
col1,col2,col3=st.columns(3)
with col1:
    st.image('nikhil-mishra-sshi-ram-ji-4k-1-1a-wm.jpg')
with col2:
    st.header('Jai Shree Ram')
with col3:
    st.header('Jai Shree Hari')
st.error('login failed')
st.success('login sucessful')
import time


email=st.text_input('Enter Email Id')
number=st.number_input('age')
password=st.text_input('enter password')
btn=st.button('login')
if btn:
    if email=='rkhangar1998@gmail.com' and password=='1234':
        st.success('successful')
        st.balloons()
    else:
        st.error('something is wrong')

st.sidebar.selectbox('Founders',['Rajesh','Rupesh'])

file=st.file_uploader('upload a csv document')
if file is not None:
    df=pd.read_csv(file)
    st.dataframe(df.describe())
