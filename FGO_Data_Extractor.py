import bs4 as bs
import requests
import pandas as pd
import numpy as np

Servant_Data = []
column = ['Name','Alias','Class','ID','Rarity','Drain','Max Lvl.','ATK lvl. 1','HP lvl. 1',
           'ATK lvl. 70','HP lvl. 70','ATK lvl. 100','HP lvl. 100','MAX ATK + Fou','MAX HP + Fou',
          'NP gain','Quick Card Hits','Star Weight','Arts Card Hits','Star Rate','Buster Card Hits','Death Rate'
          ,'Extra Attack','Attribute','Noble Phantasm Hits','Traits']

rarity = {'★★★ R':'R','★★★★★ SSR':'SSR','★★★★ SR':'SR','★★':'UC','★':'C'}

Servant_count = 236

for i in range(1,Servant_count):

  'HTTP request to Cirnopedia website '

  req = requests.get('https://fate-go.cirnopedia.org/servant_profile.php?servant=' + str(i),headers={'User Agent': 'Mozilla/5.0'})
  soup = bs.BeautifulSoup(req.content,'lxml')

  'Get contents of the tables in the Servant Profile'

  table = soup.find_all('tbody')
  table_rows1 = table[0].find_all('tr')

  for tr in table_rows1:
    td_desc = tr.find_all('td', class_='desc')
    Servant_Table1 = [str(ia.text.strip()) for ia in td_desc]
    Servant_Data.extend(Servant_Table1)

  table_rows2 = table[1].find_all('tr')

  for tr in table_rows2:
    td_desc = tr.find_all('td',class_='desc')
    Servant_Table2 = [str(ia.text.strip()) for ia in td_desc]
    Servant_Data.extend(Servant_Table2)

'Create a dataframe to store the values and columns'

df = pd.DataFrame(np.array(Servant_Data).reshape(Servant_count - 1,26),columns=column)

df = df[['Name','Alias','Class','ID','Rarity','Drain','Max Lvl.','ATK lvl. 1','HP lvl. 1',
           'ATK lvl. 70','HP lvl. 70','ATK lvl. 100','HP lvl. 100','MAX ATK + Fou','MAX HP + Fou',
          'NP gain','Star Weight','Star Rate','Death Rate','Buster Card Hits','Arts Card Hits','Quick Card Hits',
          'Extra Attack','Attribute','Noble Phantasm Hits','Traits']]

new = df['NP gain'].str.split('・',n=1,expand=True)
df['ATK NP gain'] = new[0]
df['DEF NP gain'] = new[1]
df['ATK NP gain'] = df['ATK NP gain'].replace("Attack: "," ",regex=True)
df['DEF NP gain'] = df['DEF NP gain'].replace("Defense: "," ",regex=True)

df['Buster Card Hits'] = df['Buster Card Hits'].replace('Hits'," ",regex=True)
df['Arts Card Hits'] = df['Arts Card Hits'].replace('Hits'," ",regex=True)
df['Quick Card Hits'] = df['Quick Card Hits'].replace('Hits'," ",regex=True)
df['Noble Phantasm Hits'] = df['Noble Phantasm Hits'].replace('Hits'," ",regex=True)

'Write to a .csv file'

df.to_csv("FGO_Servant_Data.csv",encoding = 'utf-8-sig')


