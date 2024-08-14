# TKX Upcoming Event Email Generator

This project is a web application that generates HTML email content for TKX events, including upcoming shows and announcements. It allows users to parse event information from a URL or pasted HTML, select events, and generate formatted event cards for email marketing purposes.

## Project Structure

### 1. app.py
This is the main Flask application file. It contains the server-side logic for parsing events, generating cards, and serving the web interface.

Key features:
- Flask routes for the main page, parsing events, and generating cards
- Function to parse event information from HTML
- Error handling for 403 Forbidden and 500 Internal Server errors
- Integration with Streamlit for additional functionality

### 2. templates/index.html
This is the main HTML template for the web interface. It includes the structure, styling, and client-side JavaScript for interacting with the server and manipulating the DOM.

Key features:
- Input fields for URL or HTML content
- Event list display with responsive design
- Event selection and card generation functionality
- Options to generate upcoming show cards, announcement cards, featured event cards, or upcoming announcement cards
- Responsive design for various screen sizes

### 3. templates/upcoming_template.html
This file contains the HTML template for upcoming show cards.

### 4. templates/announcement_template.html
This file contains the HTML template for announcement cards.

### 5. templates/announcement_featured_template.html
This file contains the HTML template for featured event cards.

### 6. templates/upcoming_announcement_template.html
This file contains the HTML template for upcoming announcement cards.

### 7. templates/ticket_analysis.html
This file contains the HTML template for the ticket sales analysis page, which integrates with Streamlit.

### 8. pyproject.toml
This file specifies the project dependencies and configuration for the Poetry package manager.

## How to Run

1. Ensure you have Python 3.12 or later installed.

2. Install Poetry if you haven't already:
   ```
   pip install poetry
   ```

3. Clone the repository and navigate to the project directory.

4. Install the project dependencies:
   ```
   poetry install
   ```

5. Activate the virtual environment:
   ```
   poetry shell
   ```

6. Run the Flask application:
   ```
   python app.py
   ```

7. Open a web browser and navigate to `http://localhost:5001`

## Features

1. Event Parsing:
   - Parse events from a URL or pasted HTML content
   - Extract event details including artist, venue, date, time, and image

2. Card Generation:
   - Generate HTML cards for upcoming shows, announcements, featured events, or upcoming announcements
   - Customizable templates for different card types

3. User Interface:
   - Responsive design for various screen sizes
   - Event selection with options to select all, unselect all, or select top N events
   - Preview generated cards
   - Copy generated HTML to clipboard

4. Streamlit Integration:
   - Additional functionality for event parsing and card generation
   - Ticket sales analysis (work in progress)

## Dependencies

The project uses the following main dependencies:
- Flask
- BeautifulSoup4
- Requests
- Streamlit
- Pandas
- Plotly

For a complete list of dependencies, refer to the `pyproject.toml` file.

## Updating the README

As we continue to develop and enhance the project, we should update this README.md file to reflect new features, dependencies, or usage instructions. This will help maintain clear documentation for the project.

## Next Steps

1. Complete the Streamlit integration for ticket sales analysis
2. Enhance error handling and user feedback
3. Implement unit tests for core functionality
4. Optimize performance for large numbers of events
5. Add user authentication for secure access to sensitive features

Remember to commit your changes frequently and push to the repository to keep track of your progress, Chief!