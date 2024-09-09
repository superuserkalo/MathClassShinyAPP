import shiny
from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt

app_ui = ui.page_sidebar(
    ui.sidebar(
    ui.input_file("file1", "Choose CSV File", accept=[".csv"]),
    ),
    ui.output_plot("bar_plot")
)

def server(input, output, session):
    @render.plot
    def bar_plot():

        file_dict = input.file1()
        if isinstance(file_dict, list):
            file_dict = file_dict[0]

        df = pd.read_csv(file_dict['datapath'])

        if 'Topic' not in df.columns or 'Rating' not in df.columns:
            return "The CSV file must contain 'Topic' and 'Rating' columns."
        
        negative_ratings = df[df['Rating'] == '-']
        topic_counts = negative_ratings['Topic'].value_counts().sort_values()

        # Plot the bar chart
        plt.figure(figsize=(10, 6))
        topic_counts.plot(kind='bar', color=['skyblue'])
        plt.title('Topic Ratings')
        plt.xlabel('')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        
        # Return the plot
        return plt.gcf()



if __name__ == "__main__":
    app = App(app_ui, server)
    app.run()