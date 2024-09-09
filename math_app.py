import shiny
from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt

app_ui = ui.page_fluid(
    ui.panel_title("Math Class Topic Rating"),
    ui.page_sidebar(
        ui.sidebar(
            ui.input_file("file1", "Choose CSV File", accept=[".csv"]),
            ui.output_text_verbatim("file_info")
        ),
        ui.ma(
            ui.output_plot("bar_plot")
        )
    )
)

def server(input, output, session):
    @output
    @render.text
    def file_info():
        if input.file1() is None:
            return "No file selected."
        return f"File: {input.file1()['name']}"

    @output
    @render.plot
    def bar_plot():
        if input.file1() is None:
            return None
        
        # Read the uploaded CSV file
        df = pd.read_csv(input.file1()['datapath'])
        
        # Assuming the CSV has columns 'Topic', 'Rating'
        rating_counts = df['Rating'].value_counts()
        
        # Plot the bar chart
        plt.figure(figsize=(10, 6))
        rating_counts.plot(kind='bar', color=['green', 'red', 'blue'])
        plt.title('Topic Ratings')
        plt.xlabel('Rating')
        plt.ylabel('Count')
        plt.xticks(rotation=0)
        return plt


if __name__ == "__main__":
    app = App(app_ui, server)
    app.run()
