from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import pandas as pd # importa a principal biblioteca de manipulação de dados no Python
import numpy as np # importa biblioteca que permite trabalhar com arranjos, vetores e matrizes
import matplotlib.pyplot as plt # importa biblioteca para gráficos]
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(
    'C:/Users/User/PycharmProjects/pythonProject/client_secrets.json',
    scopes=['https://www.googleapis.com/auth/analytics.readonly'])

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'C:/Users/User/PycharmProjects/pythonProject/client_secrets.json'
VIEW_ID = '0000000'
data_inicio = '2021-08-01'
data_fim = '2021-08-31'


def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
  analytics = build('analyticsreporting', 'v4', credentials=credentials)
  return analytics

def get_report_visao_geral(analytics):
    return analytics.reports().batchGet(body={'reportRequests': [{
      'viewId': VIEW_ID,
      'dateRanges': [{'startDate': data_inicio, 'endDate': data_fim}],
      'dimensions': [
        {'name': 'ga:date'}
      ],
      'metrics': [
        {'expression': 'ga:users'},
        {'expression': 'ga:sessions'},
        {'expression': 'ga:transactions'},
        {'expression': 'ga:transactionsPerSession'},
        {'expression': 'ga:revenuePerTransaction'},
        {'expression': 'ga:transactionRevenue'},
        {'expression': 'ga:totalValue'},
      ]
    }]}).execute()

def response(response):
    report = response.get('reports', [])[0]  # expected just one report
    # headers
    header_dimensions = report.get('columnHeader', {}).get('dimensions', [])
    header_metrics = [value['name'] for value in
                      report.get('columnHeader', {}).get('metricHeader', {}).get('metricHeaderEntries', [])]
    headers = header_dimensions + header_metrics
    headers = list(map((lambda x: x.split(':', 1)[-1]), headers))  # removes "ga:" from each column
    # values
    values = []
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
      values_dimensions = row.get('dimensions', [])
      values_metrics = row.get('metrics', [])[0].get('values', [])
      values.append(values_dimensions + values_metrics)
    # to dataframe
    df = pd.DataFrame(columns=headers, data=values)
    return df

analytics = initialize_analyticsreporting()
response_visao_geral = get_report_visao_geral(analytics)
df = response(response_visao_geral)

df.head()
