import requests
from bs4 import BeautifulSoup
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import json
import re
from datetime import datetime, timedelta

# Define the start date for the DAG
start_date = datetime(2022, 1, 1)

sources = ['https://www.dawn.com/', 'https://www.bbc.com/']

def extract():
    extracted_data = {}
    for source in sources:
        reqs = requests.get(source)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        articles = soup.find_all('article')

        articles_data = []
        for article in articles:
            title = article.find('h3')
            description = article.find('p')
            if title and description:
                articles_data.append({
                    'title': clean_text(title.text.strip()),
                    'description': clean_text(description.text.strip())
                })

        extracted_data[source] = {
            'links': links,
            'articles': articles_data
        }

    return extracted_data

def clean_text(text):
    # Remove special characters and extra whitespaces
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text

def transform(extracted_data):
    # Placeholder for transformation logic
    transformed_data = extracted_data
    return transformed_data

def load(data):
    # Storing the data on Google Drive
    google_drive_path = "https://drive.google.com/drive/u/0/folders/18TtpB7KOpIx5lYGbobfr9TJdRmQJhsR4"
    file_name = "processed_data.json"

    with open(os.path.join(google_drive_path, file_name), 'w') as f:
        json.dump(data, f)

    # Implementing Data Version Control (DVC)
    os.system("dvc add {} -f".format(os.path.join(google_drive_path, file_name)))
    os.system("git add . && git commit -m 'Added new data version' && git push origin master")

default_args = {
    'owner': 'airflow-demo',
    'start_date': start_date
}

dag = DAG(
    'mlops-dag',
    default_args=default_args,
    description='A simple ',
    schedule=timedelta(days=1)
)

task1 = PythonOperator(
    task_id="Task_1",
    python_callable=extract,
    dag=dag
)

task2 = PythonOperator(
    task_id="Task_2",
    python_callable=transform,
    dag=dag
)

task3 = PythonOperator(
    task_id="Task_3",
    python_callable=load,
    dag=dag
)

task1 >> task2 >> task3
