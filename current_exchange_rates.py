#a parser that automatically pulls historical exchange rates from the Internet and converts national currencies into USD.
import pandas as pd
import datetime
from datetime import timedelta, date
#import ipywidgets as widgets for jupyter
import time

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

'''for jupyter
start_date_w = widgets.DatePicker(
    description='Pick a Date',
    disabled=False
)
print('Please, select start date:')
start_date_w

end_date_w = widgets.DatePicker(
    description='Pick a Date',
    disabled=False
)
print('Please, select end date:')
end_date_w

start_date=start_date_w.value
end_date=end_date_w.value+datetime.timedelta(days=1)
print(f'Selected period: from {start_date} to {end_date}')
'''
year1 = int(input('Enter a year: '))
month1 = int(input('Enter a month: '))
day1 = int(input('Enter a day: '))

start_date = date(year1, month1, day1)
print('start: ',start_date)

year2 = int(input('Enter a year: '))
month2 = int(input('Enter a month: '))
day2 = int(input('Enter a day: '))

end_date = date(year2, month2, day2)
print('end: ', end_date)

print(f'Selected period: from {start_date} to {end_date}')

#--------------------------------------------------------------------------------------------For single country
df = pd.DataFrame()
print("Please input code of national currency (for example, UAH):")
from_val=str(input())

for single_date in daterange(start_date, end_date):
    try:
        dfs = pd.read_html(f'https://www.xe.com/currencytables/?from={from_val}&date={single_date.strftime("%Y-%m-%d")}')[0]
        dfs['Date'] = single_date.strftime("%Y-%m-%d")
        df = pd.concat([df, dfs], ignore_index=True)
        print(f'Parsing for {from_val} in ',single_date.strftime("%Y-%m-%d"))
    except:
        print('No data for ',single_date.strftime("%Y-%m-%d"))
        
print('Finish!')

df_val = df.loc[df['Currency'] == 'USD']
df_val.insert(2, "National currency", [str(from_val) for i in range(len(df_val['Currency']))], True)
df_val_set=df_val[['Date', f'{from_val} per unit',f'Units per {from_val}']].set_index('Date')
df_val_r = df_val.rename(columns={f'Units per {from_val}': f'USD per {from_val}', f'{from_val} per unit': f'{from_val} per USD'})
df_val_r.sort_values('Date', ascending=False, inplace = True)
df_val_set=df_val_r[['Date',f'{from_val} per USD',f'USD per {from_val}']].set_index('Date')

df_val_set.to_csv(f'Exchange_{from_val}_from_{start_date}_to_{end_date}.csv')
#--------------------------------------------------------------------------------------------For all available currency
currency_data = [
    "ADF", "ADP", "AED", "AFA", "AFN", "ALL", "AMD", "ANG", "AOA", "AON", "ARS", "ATS", "AUD", "AWF", "AWG", "AZM", "AZN", 
  "BAM", "BBD", "BDT", "BEF", "BGL", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BYN", "BYR", "BZD", 
  "CAD", "CDF", "CHF", "CLP", "CNY", "COP", "CRC", "CUC", "CUP", "CVE", "CYP", "CZK", "DEM", "DJF", "DKK", "DOP", "DZD", "ECS", "EEK", 
  "EGP", "ERN", "ESP", "ETB", "EUR", "FIM", "FJD", "FKP", "FRA", "FRF", "GBP", "GEL", "GGP", "GHC", "GHS", "GIP", "GMD", "GNF", "GRD", 
  "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "IEP", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "ITL", "JEP", "JMD", "JOD", 
  "JPY", "KES", "KGS", "KHR", "KID", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LTL", "LUF", "LVL", 
  "LYD", "MAD", "MCF", "MDL", "MGA", "MGF", "MKD", "MMK", "MNT", "MOP", "MRO", "MRU", "MTL", "MUR", "MVR", "MWK", "MXN", "MYR", "MZM", 
  "MZN", "NAD", "NGN", "NIO", "NLG", "NOK", "NPR", "NTD", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PSL", "PTE", "PYG", 
  "QAR", "ROL", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDD", "SDG", "SDP", "SEK", "SGD", "SHP", "SIT", "SKK", "SLL", "SOS", 
  "SPL", "SRD", "SRG", "SSP", "STD", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMM", "TMT", "TND", "TOP", "TRL", "TRY", "TTD", "TVD", 
  "TWD", "TZS", "UAH", "UGX", "UYP", "UYU", "UZS", "VAL", "VEB", "VEF", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBT", "XCD", 
  "XCP", "XDR", "XEU", "XOF", "XPD", "XPF", "XPT", "XUA", "YER", "YUN", "ZAR", "ZMK", "ZMW", "ZWD", "ZWL"
]
empty_lists=[[] for i in range(len(currency_data))]
currency_usd=[f'{i}' for i in currency_data]

df = pd.DataFrame()
dict_val=dict(zip(currency_usd,empty_lists))
dict_val['Date']=[]

time1=time.time()
for from_val in currency_data:
    for single_date in daterange(start_date, end_date):
        try:
            dfs = pd.read_html(f'https://www.xe.com/currencytables/?from={from_val}&date={single_date.strftime("%Y-%m-%d")}')[0].iloc[0]
            dict_val[f'{from_val}'].append(dfs.values[2])
            if single_date.strftime("%Y-%m-%d") not in dict_val['Date']:
                dict_val['Date'].append(single_date.strftime("%Y-%m-%d"))
            print(f'Parsing for {from_val} in ',single_date.strftime("%Y-%m-%d"))
        except:
            print(f'{from_val}',single_date.strftime("%Y-%m-%d"))  
            dict_val[f'{from_val}'].append(float('nan'))
            if single_date.strftime("%Y-%m-%d") not in dict_val['Date']:
                dict_val['Date'].append(single_date.strftime("%Y-%m-%d"))
    print(f'Finish for {from_val}')
print('All Finish!')
print("Total time lasted for %s seconds " % (time.time() - time1))

new_df = pd.DataFrame.from_dict(dict_val)

new_df.info()

new_df.sort_values('Date', ascending=False, inplace = True)
new_df.dropna(axis = 1, how = 'all', inplace = True)
n_f=new_df.set_index('Date')
n_fin = n_f.select_dtypes(exclude=['object'])
n_fin.info()

n_fin.to_csv(f'Exchange_all_from_{start_date}_to_{end_date}.csv')




