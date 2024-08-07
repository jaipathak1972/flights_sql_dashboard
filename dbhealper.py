import plotly.express as px
from db_connection import create_connection_heartattack

def fetch_data(query, params=()):
    connection = create_connection_heartattack()
    if not connection:
        raise Exception("Failed to connect to the database.")
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return []
    
    finally:
        cursor.close()
        connection.close()

def create_bar_graph(table_name):
    query = f"SELECT Age, COUNT(Age) as Freq FROM {table_name} GROUP BY Age ORDER BY Age"
    data = fetch_data(query)
    if not data:
        return None
    age, freq = zip(*data)
    data_dict = {'Age': age, 'Frequency': freq}
    fig = px.bar(data_dict, x='Age', y='Frequency', title='Age vs. Frequency of Heart Attacks', labels={'Age': 'Age', 'Frequency': 'Frequency'}, template='plotly_white')
    fig.update_layout(title_font_size=24)
    return fig

def create_line_graph(table_name):
    query = f"SELECT Age, COUNT(Age) as Freq FROM {table_name} GROUP BY Age ORDER BY Age"
    data = fetch_data(query)
    if not data:
        return None
    age, freq = zip(*data)
    data_dict = {'Age': age, 'Frequency': freq}
    fig = px.line(data_dict, x='Age', y='Frequency', title='Age vs. Frequency of Heart Attacks', labels={'Age': 'Age', 'Frequency': 'Frequency'}, template='plotly_white')
    fig.update_layout(title_font_size=24)
    return fig 

def create_boxplot_graph(table_name):
    query = f"SELECT Cholesterol FROM {table_name}"
    data = fetch_data(query)
    if not data:
        return None
    values = [row[0] for row in data]
    data_dict = {'Cholesterol': values}
    fig = px.box(data_dict, y='Cholesterol', title='Distribution of Cholesterol Levels', template='plotly_white')
    fig.update_layout(title_font_size=24)
    return fig

def create_pie_chart(table_name):
    query = f"SELECT Sex, COUNT(Sex) as Freq FROM {table_name} GROUP BY Sex"
    data = fetch_data(query)
    if not data:
        return None
    sex, freq = zip(*data)
    data_dict = {'Sex': sex, 'Frequency': freq}
    fig = px.pie(data_dict, names='Sex', values='Frequency', title='Sex Distribution of Heart Attacks', template='plotly_white')
    fig.update_layout(title_font_size=24)
    return fig