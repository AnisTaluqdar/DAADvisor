import pandas as pd
from datetime import datetime
import re


df = pd.read_csv("/Data/daad_data.csv")

df['Scholarships'] = df['C-badge'].apply(lambda x: 'Yes' if isinstance(x, str) and 'Scholarships' in x else 'No')

df['Fully online'] = df['C-badge'].apply(lambda x: 'Yes' if isinstance(x, str) and 'Fully online' in x else 'No')

df['Hybrid'] = df['C-badge'].apply(lambda x: 'Yes' if isinstance(x, str) and 'Hybrid' in x else 'No')

df['Partly online'] = df['C-badge'].apply(lambda x: 'Yes' if isinstance(x, str) and 'Partly online' in x else 'No')

df['Fully on-site'] = df['C-badge'].apply(lambda x: 'No' if isinstance(x, str) and ('Partly online' or 'Hybrid' or  'Fully online')  in x else 'Yes')


def check_presence(x):
    strings_to_check = ['online', 'Hybrid']
    if isinstance(x, str):
        return 'No' if any(string in x for string in strings_to_check) else 'Yes'
    else:
        return 'Yes'

df['Fully on-site'] = df['C-badge'].apply(check_presence)

df = df.rename(columns={'Location': 'City', 'University': 'Institution'})

def costs_to_numbers(costs_str):
    try:
        costs_value = float(costs_str.split()[1].replace(',', ''))
        costs_numbers = costs_value * 121.03
        return costs_numbers
    except:
        return None

df['Costs (Taka)'] = df['Costs'].apply(lambda x: costs_to_numbers(x))


def tuition_to_numbers(tuition_str):
    try:
        tuition_value = float(tuition_str.split()[1].replace(',', ''))
        tuition_numbers = tuition_value * 121.03
        return tuition_numbers
    except:
        return None

df['Tuition fees (Taka per semester)'] = df['Tuition fees per semester'].apply(lambda x: tuition_to_numbers(x))


def semesters_to_numbers(semesters_str):
    try:
        num_semesters = int(semesters_str.split()[0])
        return num_semesters
    except:
        return None

df['Duration (Semesters)'] = df['Duration'].apply(lambda x: semesters_to_numbers(x))


def semesters_to_months(semesters_str, months_per_semester=6):
    try:
        num_semesters = int(semesters_str.split()[0])
        equivalent_months = num_semesters * months_per_semester
        return equivalent_months
    except:
        return None

df['Duration (Months)'] = df['Duration'].apply(lambda x: semesters_to_months(x))


df['Duration (Years)'] = df['Duration (Months)'].apply(lambda x: x/12)



current_year = datetime.now().year

df['Course enroll End Date'] = df['Date(s)'].str.extract(r'(\s\d+\s\w+,\s\d+)')


df['Course enroll Start Date'] = df['Date(s)'].str.extract(r'(\d+\s\w+)') + df['Course enroll End Date'].str.extract(r'(,\s\d+)')


df['Registration Deadline'] = df['Date(s)'].str.extract(r'(Registration Deadline\s\d+\s\w+,\s\d+)')

df['Registration Deadline'] = df['Registration Deadline'].str.extract(r'(\s\d+\s\w+,\s\d+)')




df = df.drop(columns=['Costs'])

df = df.drop(columns=['Duration'])

df = df.drop(columns=['Tuition fees per semester'])

df = df.drop(columns=['C-badge'])

df = df.drop(columns=['Date(s)'])


df["Application deadline"] = df["Application deadline"].fillna("No application deadline")

df["Financial support"] = df["Financial support"].fillna("No")

df["Specific support for int. students and doctoral candidates"] = df["Specific support for int. students and doctoral candidates"].fillna("No")

df["Structured research and supervision"] = df["Structured research and supervision"].fillna("No")



df['Course enroll End Date'] = pd.to_datetime(df['Course enroll End Date'])
df['Course enroll End Date'] = df['Course enroll End Date'].dt.strftime('%d/%m/%Y')
df['Course enroll Start Date'] = pd.to_datetime(df['Course enroll Start Date'])
df['Course enroll Start Date'] = df['Course enroll Start Date'].dt.strftime('%d/%m/%Y')
df['Registration Deadline'] = pd.to_datetime(df['Registration Deadline'])
df['Registration Deadline'] = df['Registration Deadline'].dt.strftime('%d/%m/%Y')


file_path = '/Data/daad_final_data.csv'
df.to_csv(file_path, index=False)