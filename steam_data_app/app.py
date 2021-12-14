import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

st.set_page_config(layout="wide")

@st.cache
def load_data():
    # This is the first file stored in the bucket
    df = pd.read_csv('gs://YOUR_BUCKET_NAME/FILENAME')

    start_date = datetime.date(2021, 12, 13)
    today = datetime.date.today()
    days_diff = today - start_date

    # Append new files on the first file.
    for day in range(1, days_diff.days + 1, 1):
        date_str = (start_date + datetime.timedelta(days=day)).strftime('%Y_%m_%d')
        df_new = pd.read_csv('gs://YOUR_BUCKET-NAME/' + date_str + 'FILENAME')
        
        df = pd.concat([df, df_new])    

        print("There is no data on" + date_str)
    
    df.set_index('date', inplace=True)

    return df

def main():
    ### prepare data
    df = load_data()
    columns = df.columns
    
    # Latest max user ranking
    latest_day = df.T.columns[-1]
    ranking = df.T[latest_day].sort_values(ascending=False)[0:100]
    ranks = [i for i in range(1, ranking.shape[0] + 1)]

    
    ### Sidebar
    st.sidebar.markdown("## Settings")
    game_select = st.sidebar.selectbox('Choose a game to see the max user transition', columns)
    

    ### Main view
    st.title('Steam Game Max User Data Dashboard')

    # Ranking table and bar plot
    ranking_container = st.container()
    with ranking_container:
        col1_top, col2_top = st.columns(2)

        # Top 100
        with col1_top:
            ranking_table = go.Figure(data=[go.Table(
                header=dict(values=['Rank', 'Game', 'Max Users'],
                            line_color='darkslategray',
                            fill_color='lightskyblue',
                            align='left'),
                cells=dict(values=[ranks, ranking.keys(), ranking],
                        line_color='darkslategray',
                        fill_color='lightcyan',
                        align='left'))
            ])

            ranking_table.update_layout(height=None, width=500, margin={'l': 20, 'r': 20, 't': 0, 'b': 0})
            ranking_table.update_xaxes(title_text=None)
            ranking_table.update_yaxes(title_text='Max Users')
            st.subheader('Max User Top 100 Games on ' + latest_day)
            st.plotly_chart(ranking_table, use_container_width=True)

        # Top 5
        with col2_top:
            ranking_fig = go.Figure(data=[go.Bar(
                x=ranking[0:5].keys(), y=ranking[0:5],
                text=ranking[0:5],
                textposition='auto',
            )])

            ranking_fig.update_layout(height=300, width=500, margin={'l': 20, 'r': 20, 't': 0, 'b': 0})
            ranking_fig.update_xaxes(title_text=None)
            ranking_fig.update_yaxes(title_text='Max Users')
            st.subheader('Max User Top 5 Games on ' + latest_day)
            st.plotly_chart(ranking_fig, use_container_width=True)



    # Max Users transition per day on each game
    transition_container = st.container()
    with transition_container:
        col1_bottom, col2_bottom = st.columns(2)
        # Show a game transition
        with col1_bottom:
            transition_fig = px.line(df, x=df.index, y=df[game_select], markers=True, labels=dict(x="Date", y="Max Users"))
            transition_fig.update_xaxes(title_text='Date',dtick=df.index, tickformat='%Y_%m_%d',zeroline=False)
            transition_fig.update_yaxes(title_text='Max Users')
            
            st.subheader('Max User Transition: ' + game_select)
            st.plotly_chart(transition_fig, use_container_width=True)
        
        # Show top 5 game transitions
        with col2_bottom:
            transition_top5_fig = px.line(df, x=df.index, y=ranking[0:5].keys(), markers=True, labels=dict(x="Date", y="Max Users", color='Games'))
            transition_top5_fig.update_xaxes(title_text='Date',dtick=df.index, tickformat='%Y_%m_%d',zeroline=False)
            transition_top5_fig.update_yaxes(title_text='Max Users')

            st.subheader('Top 5 Games Max User Transition')
            st.plotly_chart(transition_top5_fig, use_container_width=True)
            

if __name__ == "__main__":
    main()