import datetime

import streamlit as st
import requests
from ics import Calendar
import pandas as pd


def main():
    st.sidebar.title('iCal Display')

    url = st.sidebar.text_input('Enter your iCal feed URL:')

    if st.sidebar.button('Load Calendar'):
        if url:
            try:
                # Fetch the content of the url
                c = Calendar(requests.get(url).text)

                # Create lists to hold the event data
                event_name = [e.name for e in c.events]
                event_start = [e.begin.date() for e in c.events]
                event_end = [e.end.date() for e in c.events]

                # Assemble the data into a pandas DataFrame and display
                df = pd.DataFrame({'Event': event_name, 'Start': event_start, 'End': event_end})
                df = df.sort_values('Start')

                # Remove rows where today's date is greater than the end date
                df = df[df['End'] >= datetime.date.today()]

                # Convert the DataFrame to Markdown and display
                st.markdown(df.to_markdown())

                # # Generate CSS to highlight rows where today's date is between start and end date
                # df['Highlight'] = (df['Start'] <= datetime.date.today()) & (df['End'] >= datetime.date.today())
                # df.loc[df['Highlight'], 'Highlight'] = 'background-color: yellow'
                # df.loc[~(df['Start'] <= datetime.date.today()) & (df['End'] >= datetime.date.today()), 'Highlight'] = ''
                #
                # # Reset the 'Highlight' column to be the DataFrame's index
                # df = df.set_index('Highlight')
                #
                # # Convert the DataFrame to an HTML table and display
                # st.write(df.to_html(escape=False), unsafe_allow_html=True)

            except Exception as e:
                st.write('An error occurred:')
                st.write(e)

        else:
            st.write('Please enter an iCal feed URL.')


if __name__ == '__main__':
    main()