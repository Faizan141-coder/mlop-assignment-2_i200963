# News Article Extraction and Version-Controlled Storage Pipeline

## Overview

This project implements an automated pipeline to extract news articles from two major news sources – Dawn (`dawn.com`) and BBC (`bbc.com`). The pipeline performs the following key steps:

1. **Extraction:** Extracts article links, titles, and descriptions from the homepages of the news sources.
2. **Transformation:** Cleans and preprocesses the extracted text data.
3. **Loading:** Stores the processed data in JSON format on Google Drive.
4. **Version Control:** Uses DVC (Data Version Control) to track changes and versions of the data.

## Workflow

The pipeline is orchestrated using Apache Airflow, a powerful workflow management tool. Here's how the Airflow DAG (Directed Acyclic Graph) executes the pipeline tasks:

1. **Task 1 (Extract):** Scrapes the news websites using `requests` and `BeautifulSoup`, extracting relevant information.
2. **Task 2 (Transform):** Applies data cleaning and preprocessing steps (e.g., removing special characters).
3. **Task 3 (Load):** Saves the processed data as JSON to a specified Google Drive folder.
4. **Version Control:**  The `dvc add` command tracks the new data version, and `git` commands commit and push the changes to a remote repository.

## DVC Setup

1. **Apache Airflow:**
   - Install Apache Airflow and configure it according to your environment.
   - Ensure Airflow's Python environment has the required libraries (`requests`, `BeautifulSoup4`, `dvc`).

2. **Google Drive:**
   - Create a folder in your Google Drive where the data will be stored.
   - Update the `google_drive_path` variable in the `load` function with the correct path to your folder.

3. **DVC (Data Version Control):**
   - Install DVC (`pip install dvc`).
   - Initialize a DVC repository in your project directory (`dvc init`).
   - Set up a remote DVC storage (e.g., on a cloud platform like AWS S3) to store your data versions. Update the DVC configuration accordingly.

4. **Git:**
   - Ensure you have a Git repository for versioning your code and DVC metadata.

## Usage

1. **Schedule DAG:** Set up the Airflow DAG to run daily (or adjust the `schedule` parameter in the DAG definition to your preferred frequency).
2. **Monitor:** Monitor the Airflow UI for successful DAG runs and potential errors.
3. **Version History:** Use DVC commands (`dvc list`, `dvc checkout`) to access and manage different versions of your data.

## Important Considerations

- **Web Scraping Policies:** Be mindful of the websites' terms of service and robots.txt files to avoid violating their policies. 
- **Error Handling:** Consider adding error handling mechanisms to the pipeline to handle cases like website unavailability or network issues gracefully.
- **Transformation Logic:** Currently, the transformation step is a placeholder. Implement specific transformations based on your data requirements.

## Future Enhancements

- **Data Validation:** Incorporate data validation steps to ensure the quality and consistency of the extracted data.
- **Monitoring and Alerting:** Set up alerts in Airflow to notify you of any pipeline failures or issues.
- **Scalability:** If you expect large volumes of data, consider optimizing for scalability by using distributed task execution frameworks (e.g., Celery) in conjunction with Airflow.
