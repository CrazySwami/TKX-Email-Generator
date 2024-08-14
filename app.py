from flask import Flask, render_template, request, jsonify, abort, Response
import logging
from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime
import streamlit as st
import sys
from io import StringIO

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Keep all your existing Flask routes and functions here
@app.errorhandler(403)
def forbidden(e):
    app.logger.error('403 error: %s', str(e))
    return jsonify(error=str(e)), 403

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error('500 error: %s', str(e))
    return jsonify(error="Internal Server Error"), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse_events', methods=['POST'])
def parse_events():
    try:
        url = request.form.get('url')
        html_content = request.form.get('html_content')
        
        if url:
            response = requests.get(url)
            html_content = response.text
        
        events = parse_events_from_html(html_content)
        return jsonify(events=events)
    except Exception as e:
        app.logger.error(f"Error in parse_events: {str(e)}")
        return jsonify(error=str(e)), 500

@app.route('/generate_cards', methods=['POST'])
def generate_cards():
    try:
        events = request.json.get('events', [])
        template_type = request.json.get('templateType', 'upcoming')
        
        if template_type == 'upcoming':
            template_file = 'upcoming_template.html'
        elif template_type == 'announcement':
            template_file = 'announcement_template.html'
        elif template_type == 'featured':
            template_file = 'announcement_featured_template.html'
        else:  # upcoming_announcement
            template_file = 'upcoming_announcement_template.html'
        
        with open(f'templates/{template_file}', 'r') as file:
            template = file.read()
        
        if template_type in ['upcoming', 'announcement']:
            generated_html = "<div style='display: flex; flex-wrap: wrap; justify-content: space-between;'>"
            for i, event in enumerate(events):
                event_html = template
                for key, value in event.items():
                    event_html = event_html.replace(f'{{{key.upper()}}}', str(value))
                generated_html += event_html
                
                if (i + 1) % 2 == 0 and i != len(events) - 1:
                    generated_html += "</div><div style='display: flex; flex-wrap: wrap; justify-content: space-between;'>"
            generated_html += "</div>"
        elif template_type == 'featured':
            if events:
                event = events[0]
                event_html = template
                for key, value in event.items():
                    event_html = event_html.replace(f'{{{key.upper()}}}', str(value))
                generated_html = event_html
            else:
                generated_html = "<p>No events available for featured template.</p>"
        else:  # upcoming_announcement
            generated_html = ""
            for event in events:
                event_html = template
                for key, value in event.items():
                    event_html = event_html.replace(f'{{{key.upper()}}}', str(value))
                generated_html += event_html
        
        return jsonify({'html': generated_html})
    except Exception as e:
        app.logger.error(f"Error in generate_cards: {str(e)}")
        return jsonify(error=str(e)), 500

def parse_events_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    events = []
    current_year = datetime.now().year
    for event_div in soup.find_all('div', class_='event-tile'):
        event = {}
        event['artist'] = event_div.find('div', class_='artist').text.strip()
        event['venue'] = event_div.find('div', class_='categories').text.split('|')[0].strip()
        date_div = event_div.find('div', class_='date')
        event['month'] = date_div.find('div', class_='month').text.strip()
        event['day'] = date_div.find('div', class_='day').text.strip()
        event['time'] = event_div.find('div', class_='categories').text.split('|')[-1].strip()
        event['image_url'] = re.search(r'background-image:url\((.*?)\)', event_div['style']).group(1)
        event['link'] = event_div.find('a', class_='event-tile-link')['href']
        
        year_match = re.search(r'/(\d{4})/', event['link'])
        event['year'] = int(year_match.group(1)) if year_match else current_year
        
        event_date = datetime(event['year'], 
                              datetime.strptime(event['month'], '%b').month, 
                              int(event['day']))
        
        event['dayofweek'] = event_date.strftime('%A')
        
        if event_date < datetime.now():
            event['year'] += 1
        
        events.append(event)
    return events

# New route for Streamlit app
@app.route('/streamlit/')
def streamlit_app():
    output = StringIO()
    old_stdout = sys.stdout
    sys.stdout = output

    st.title('Event Parser and Card Generator')

    url = st.text_input('Enter URL')
    html_content = st.text_area('Or paste HTML content here')

    if st.button('Parse Events'):
        if url or html_content:
            if url:
                response = requests.get(url)
                html_content = response.text
            events = parse_events_from_html(html_content)
            st.write('Parsed Events:', events)

            template_type = st.selectbox('Select template type', ['upcoming', 'announcement', 'featured', 'upcoming_announcement'])

            if st.button('Generate Cards'):
                generated_html = generate_cards_streamlit(events, template_type)
                st.write('Generated HTML:')
                st.code(generated_html, language='html')
        else:
            st.error('Please provide either a URL or HTML content')

    sys.stdout = old_stdout
    streamlit_html = output.getvalue()

    return Response(streamlit_html, mimetype='text/html')

def generate_cards_streamlit(events, template_type):
    # This function should mirror your existing generate_cards logic
    # but return the generated HTML directly instead of jsonify-ing it
    # Implement the logic here based on your existing generate_cards function
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5001)