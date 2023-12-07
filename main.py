import pandas as pd

names = [
    'avg_pr_housing_price',
    'avg_sec_housing_price',
    'inflation_total',
    'inflation_utility',
    'income_prc',
    'avg_income',
    'company_wage',
    'built_houses',
    'mortgage_prc',
    'unemployment_rate',
    'num_people',
    'urbanization',
    'pop_growth',
    'grp_prc',
    'grp_total',
    'grp_per_capita',
    'real_income',
    'working_age_prc',
    'apartment_per_1000',
    'bank_deposits',
    'debt_on_housing_loans',
    'debt_on_mortgage',
]

months = {'январь': 1, 'февраль': 2, 'март': 3, 'апрель': 4,
          'май': 5, 'июнь': 6, 'июль': 7, 'август': 8, 'сентябрь': 9,
          'октябрь': 10, 'ноябрь': 11, 'декабрь': 12, 'авуст': 8}

quarters = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'год': 'FULL'}

num_variables = 22

df_fin = None

for i in range(num_variables):
    df = pd.read_excel(f'Показатели/excel ({i}).xlsx')
    df = df.rename(columns={'Unnamed: 0': 'region'})

    if all(df.columns[1:].str.isnumeric()):
        cols = {x: f'{names[i]}_year_{x}' for x in df.columns[1:]}
        df = df.rename(columns=cols)

    elif any(df.columns[1:].str.contains('квартал')):
        cols = {x: f'{names[i]}_quarter_{quarters[x.split()[1]]}_{x.split()[0].strip(",")}' for x in df.columns[1:]}
        df = df.rename(columns=cols)

    elif not any(df.columns[1:].str.contains('-')):
        cols = {x: f'{names[i]}_month_{months[x.split()[1]]}_{x.split()[0]}' for x in df.columns[1:]}
        df = df.rename(columns=cols)

    else:
        cols = {x: f'{names[i]}_month_{months[x.split()[-1]]}_{x.split()[0].strip(",")}' for x in df.columns[1:]}
        df = df.rename(columns=cols)

    if i == 0:
        df_fin = df
    else:
        df_fin = df_fin.merge(df, on='region', how='outer')

df_fin.to_excel('initial_data.xlsx')
print(df_fin.shape)
