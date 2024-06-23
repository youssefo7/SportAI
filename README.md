### README

## Project: UEFA Euro 2020

This project sets up a Flask web application that serves an interactive visualiaztions created using Plotly. UEFA Euro 2020 data.

### Prerequisites

Make sure you have the following installed with pyhotn3.8:

- Python 3.x
- Flask
- Plotly
- Pandas
- Openpyxl

You can install the required Python packages using pip:

```bash
pip install Flask plotly pandas openpyxl
```

### Project Structure

```
SportsAI/
   .venv/
   src/
      pages/
         home.py
      services/
         graph.py
         preprocess.py
      static/
         EURO_2020_DATA.xlsx
      app.py
   requirements.txt
```

### How to Run

1. **Clone the repository:**
   ```bash
   git clone [<repository_url>](https://github.com/oussamaelfig/SportAI)
   cd SportsAI
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask app:**
   ```bash
   cd src
   python app.py
   ```

5. **Open your web browser and navigate to:**
   ```
   http://127.0.0.1:5000/
   ```
