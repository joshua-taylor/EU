import streamlit as st
from streamlit_observable import observable
import pandas as pd 
import json
#st.set_page_config(layout="wide")
#col1, col2 = st.beta_columns((2,1))

@st.cache
def data_load():
	df = pd.read_pickle('Data/data.pkl')
	df['idx'] = df.index
	df['y1'] = df['idx']/df.shape[0]*5
	return df
st.title('EU, UK & NI deal')
st.subheader('AI exploration of the EU, UK and Northern Island agreement')
df = data_load()

with st.beta_expander("What is this chart showing?"):
     st.write("""
         The chart below shows all of the paragraphs of text contained within the
         UK and EU deal agreed on the 24th December 2020.
         Colours in the chart represent the different sections of the deal (see below).
         Viewing the information by 'order of agreement', will show the document from start to end
         (top-to-bottom) with items arranged in the horizontal axis by topics.
         Viewing the information by 'subject clusters' will cluster the paragraphs in the document
         by how similar they are.
         You can pan an zoom into the chart. Hovering over a paragraph will display the text. 

     """)
     st.image('legend.png')





render = st.radio('Select view',['Render by order of agreement','Render by subject clusters'])

if render == 'Render by subject clusters':
	df_output = df[['x','y','idx','Titles','Words']]
else:
	df_output = df[['z','y1','idx','Titles','Words']]


df_output.columns = ['x','y','idx','Titles','Words']

result = df_output.to_json(orient="records")
parsed = json.loads(result)
data = list(parsed)


observers = observable("", 
    notebook="@jtaylor/animated-scatter", 
    targets=["draw", "chart",], 
    redefine={
        "currentData": data
    },
    observe=["selection"],
    hide=["draw"]
)

try:
	output = int(observers.get("selection"))
	output = df.iloc[output][['Parts','Titles','Text']]
	st.sidebar.header("Selection:")
	st.sidebar.write(output.Parts)
	st.sidebar.write(output.Titles)
	st.sidebar.write(output.Text)
	st.header("Selection:")
	st.write(output.Parts)
	st.write(output.Titles)
	st.write(output.Text)
except:
	st.subheader('First 10 paragraphs:')
	for i in df[['Articles','Text']].head().values:
		st.write(i[0])
		st.write(i[1])
	pass

st.sidebar.header("Filters:")
Search = st.sidebar.text_input('Search for keywords')
if len(Search)>0:
	Search = Search.lower()
	df = df.loc[df['Text'].str.lower().str.contains(Search)]
Parts = st.sidebar.multiselect('Select an area of the agreement', df.Parts.unique())
if len(Parts)>0:
	df = df.loc[df['Parts'].isin(Parts)]
Titles = st.sidebar.multiselect('Select a chapter of the agreement', df.Titles.unique())
if len(Titles)>0:
	df = df.loc[df['Titles'].isin(Titles)]
# Articles = st.sidebar.multiselect('Select an article of the agreement', df.Articles.unique())
# if len(Articles)>0:
# 	mask = df['Parts'].isin(Articles)
# 	df = df[mask]
