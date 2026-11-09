import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from argModel import test

def load_data():
    print("Loading data")
    df = pd.read_csv('Speed Dating Data.csv', encoding='ISO-8859-1')
    kolumny = ['iid','dec', 'attr', 'fun', 'shar', 'wave', 'order', 'gender', 'dec_o']
    dane = df[kolumny].dropna().copy()
    print("Data loaded")

    dane = dane.sort_values(by=['iid', 'order'])

    dane['wave_gender_mean_attr'] = dane.groupby(['wave', 'gender'])['attr'].transform('mean')
    dane['attr_rel'] = dane['attr'] - dane['wave_gender_mean_attr']
    dane['attr_prev'] = dane.groupby('iid')['attr'].shift(1)

    dane['attr_memory'] = (
        dane.groupby('iid')['attr']
        .transform(lambda x: x.shift(1).ewm(alpha=0.8).mean())
        .fillna(dane['attr'])
    )

    dane['fun_memory'] = (
        dane.groupby('iid')['fun']
        .transform(lambda x: x.shift(1).ewm(alpha=0.6).mean())
        .fillna(dane['fun'])
    )

    dane['shar_memory'] = (
        dane.groupby('iid')['shar']
        .transform(lambda x: x.shift(1).ewm(alpha=0.3).mean())
        .fillna(dane['shar'])
    )

    dane['med_attr_rat'] =(dane.groupby('iid')['attr'].transform(lambda x: x.mean()))


    dane['dec_prev'] = dane.groupby('iid')['dec'].shift(1).fillna(0.43)
    dane['dec_o_prev'] = dane.groupby('iid')['dec_o'].shift(1).fillna(0.43)


    dane = dane.dropna(subset=['attr_prev']).copy()
    return dane


# test(dane, ['attr', 'fun', 'shar'], 'base')
# #test(dane, ['attr', 'fun', 'shar', 'attr_rel'], 'rel')
# #test(dane, ['attr', 'fun', 'shar', 'attr_rel', 'attr_prev'], 'attr_rel attr_prev')
# #test(dane, ['attr', 'fun', 'shar', 'attr_rel', 'attr_memory'], 'attr_rel attr_memory')
# #test(dane, ['attr', 'fun', 'shar', 'attr_memory'], 'attr_memory')
# #test(dane, ['attr', 'fun', 'shar', 'attr_memory', 'fun_memory', 'shar_memory'], 'full memory')
# #test(dane, ['attr', 'fun', 'shar', 'attr_memory', 'fun_memory', 'shar_memory', 'attr_rel'], 'full memory attr_rel')
# test(dane, ['attr', 'fun', 'shar', 'attr_memory', 'fun_memory', 'shar_memory', 'attr_rel', 'dec_prev'], 'full memory attr_rel dec_prev')
# test(dane, ['attr', 'fun', 'shar', 'attr_memory', 'fun_memory', 'shar_memory', 'attr_rel', 'dec_prev','dec_o_prev'], 'full memory attr_rel dec_prev dec_o_prev')