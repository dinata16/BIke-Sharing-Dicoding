# 🚲 Bikesharing Analysis and Dashboard
This is final project from Dicoding Course in the 'Belajar Analisis Data dengan Python' to make analysis and dashboard from bike-sharing dataset (see the detail of data on the [Datasets Bike Sharing](https://www.kaggle.com/competitions/bike-sharing-demand)).

## 1. 📂 Structure Files
```
.
📦Bike-Sharing-Dicoding
 ┣ 📂dashboard
 ┃ ┣ 📜alldata_bikeshare.csv
 ┃ ┗ 📜dashboard_bikeshares.py
 ┣ 📂datasets
 ┃ ┣ 📜alldata_bikeshare.csv
 ┃ ┣ 📜Bike-sharing-datasets.zip
 ┃ ┣ 📜day.csv
 ┃ ┣ 📜hour.csv
 ┃ ┗ 📜Readme.txt
 ┣ 📂image
 ┃ ┣ 📜pngwing.com.png
 ┃ ┗ 📜preview_dashboard.png
 ┣ 📜README.md
 ┣ 📜requirements.txt
 ┗ 📜Submission_Analisis_Data_dengan_Python.ipynb
```

## 2. 📝 Analysis with Notebook

You can see the detail of Visualization on the [Jupyter Notebook](https://github.com/dinata16/Analisi-Data-Python/blob/main/Submission_Analisis_Data_dengan_Python.ipynb)

### 2.1 Project Work on Notebook
1. Data Wrangling
   - Gathering Data
   - Assessing Data
   - Cleaning Data
3. Exploratory Data Analysis
   - Define the attribute based on bussines required
   - Create data exploratory
5. Data Visualization
   - Create data visualization based on data exploratory

### 2.2 Define the question
1. How bike-sharing trends in recent year ?
2. What's the pattern of bike-sharing based on season and  month to effectively provide the bikes ?
3. Does weather affect bike-sharing usage ?
4. Do weekdays or holidays affect bike-sharing usage ?
5. What's the trends of bike-shaing based on hour ?

## 3. 📊 Dashboard on Streamlit
This dashboard  shows the total of bike-sharing across years and seasons. You can check it the details on [streamlit cloud](https://bikesharing-rizkdin.streamlit.app/)


![alt text](https://raw.githubusercontent.com/dinata16/Analisi-Data-Python/main/image/preview_dashboard.png)


### Run Streamlit in the local  
 
#### Install library

To install all required libraries, open your terminal and navigate to this project folder and run with the command:

```bash
pip install -r requirements.txt
```

#### Run Dashboard

```bash
cd dashboard
streamlit run dashboard_bikeshares.py
```

Thank you for visiting this project😊
