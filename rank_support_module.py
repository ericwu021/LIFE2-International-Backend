import requests
import json
import datetime
import pandas as pd

def score_cal_func(start_data, cwid):
  rank_id = 'rank'
  rank_file_path = './ranking/{}.csv'.format(rank_id)

  date_receive = str(start_data)
  time_last = pd.to_datetime(date_receive)

  print (time_last)

  time_current = datetime.datetime.now()

  try:
    days = (time_current - time_last).days
  except:
    days = 0

  try:
    hours = (time_current - time_last).hours
  except:
    hours = 0

  try:
    secs = (time_current - time_last).seconds
  except:
    secs = 0

  try:
    micro_secs = (time_current - time_last).microseconds
  except:
    micro_secs = 0

  current_score = days * 86400 + hours * 3600 + secs + micro_secs / 1000000.0

  cwid = cwid.upper().replace(' ', '')

  columns = ['DATE', 'SECONDS', 'RANK']
  df = pd.DataFrame(index=[cwid], columns=columns)

  data_current = [time_current, current_score, 99999]
  df.iloc[0, :] = data_current

  df_loaded = pd.read_csv(rank_file_path, index_col=0)
  df_loaded_temp = df_loaded[df_loaded.index == cwid]

  if df_loaded_temp.shape[0] == 0:
    df_loaded = df_loaded.append(df)

  else:
    last_score = df_loaded_temp['SECONDS'].values[0]

    if (current_score < last_score):
      df_loaded[df_loaded.index == cwid] = data_current

    else:
      pass

  df_loaded = df_loaded[df_loaded.index != 'VISITOR']

  df_loaded['RANK'] = df_loaded['SECONDS'].rank()

  df_loaded.to_csv(rank_file_path)

  to_frontend = {"results": [

    {"seconds": current_score}]}

  df_rank = df_loaded[df_loaded.RANK <= 5]
  if df_rank[df_rank.index == cwid].shape[0] == 0:
    if cwid != 'VISITOR':
      df_rank = df_rank.append(df_loaded[df_loaded.index == cwid])

    else:
      df_rank['RANK'] = df_rank['RANK'].astype('int')
      df_rank = df_rank.append(df)


  df_rank['RANK'] = df_rank['RANK'].astype('int')
  df_rank['CWID'] = df_rank.index
  return df_rank[['RANK','CWID','SECONDS']]
