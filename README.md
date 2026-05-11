# AI-Powered Vehicle Data Analysis Assistant 🚗🤖

This project is a Python-based vehicle data analysis assistant that processes automotive datasets and generates AI-supported technical reports.

The system performs data cleaning, statistical analysis, vehicle health scoring, and produces maintenance insights using a locally running Large Language Model (LLM).

## Features

- Vehicle dataset loading and preprocessing
- Automatic missing data handling
- Statistical analysis of vehicle performance data
- Vehicle health score calculation
- AI-generated technical analysis reports
- Local LLM integration using Ollama
- Modular Python project structure

## Technologies Used

- Python
- Pandas
- NumPy
- Data Analysis & Preprocessing
- Local LLM integration (Ollama)
- Git & GitHub

## Project Structure

ai-data-analysis-assistant/

├── main.py              # Main execution file  
├── cleaner.py           # Data cleaning module  
├── analyzer.py          # Data analysis module  
├── health.py            # Vehicle health scoring  
├── llm_report.py        # AI report generation  
├── data.csv             # Sample dataset  
└── README.md  

## Example Workflow

1. Load vehicle dataset
2. Clean and preprocess data
3. Perform statistical analysis
4. Calculate vehicle health score
5. Generate AI-based maintenance report

## Example Output

Vehicle Health Scores:

vehicle_id | health_score  
-----------|-------------  
1          | 100  
4          | 40  
6          | 70  

The system then generates an AI-based technical evaluation and maintenance suggestions for vehicle monitoring.

## Quick Start (Streamlit App)

To run the new Streamlit-based web application with the SQLite database, follow these steps:

1. Install the required dependencies:
```bash
pip install streamlit pandas matplotlib
```

2. Run the application:
```bash
streamlit run app.py
```

3. The web interface will open in your browser, where you can upload CSV files, run analyses, view charts, and check the database records.

## Future Improvements

- Real-time vehicle data integration
- Predictive maintenance modeling
- Fleet monitoring system

## Author

Developed as an automotive-oriented data analysis and AI integration project.
