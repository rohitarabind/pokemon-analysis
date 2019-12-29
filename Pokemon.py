
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as soup
from PIL import Image
from io import BytesIO


## Cleaning the database

pokemon_raw = pd.read_csv('pokemon.csv')
pokemon_raw.drop(columns=['abilities','base_egg_steps', 'base_happiness', 'capture_rate',
       'classfication', 'experience_growth', 'height_m',
       'japanese_name', 'percentage_male',
       'generation', ],inplace=True)
pokemon_raw = pokemon_raw[['name','base_total','attack','defense','hp', 'sp_attack', 'sp_defense', 'speed',
                           'type1', 'type2','against_bug', 'against_dark', 'against_dragon', 'against_electric',
       'against_fairy', 'against_fight', 'against_fire', 'against_flying',
       'against_ghost', 'against_grass', 'against_ground', 'against_ice',
       'against_normal', 'against_poison', 'against_psychic', 'against_rock',
       'against_steel', 'against_water','is_legendary','pokedex_number']]
pokemon = pokemon_raw.copy()
pokemon = pokemon.set_index('name')
pokemon_type = pokemon[['type1','attack','defense','hp', 'sp_attack', 'sp_defense', 'speed']].groupby('type1').mean()

# Get pokemon Image
def combined(df,names=[]):
    ## sub functions
    def stats(name):
        stats = df.loc[name,labels].values
        return np.concatenate((stats,[stats[0]]))
    def add_subplot(stats,name):
        ax.plot(angles,stats,'o-',linewidth = 1)
        ax.fill(angles,stats,alpha=.25)
        ax.tick_params('y',labelsize=7)
        ax.set_thetagrids(angles * 180/np.pi, labels)
        ax.grid(True)
    def find_img(name):
        r = requests.get('https://pokemondb.net/pokedex/national')
        if r.status_code == 200:
            html = soup(r.text)
        else:
            print('pokemon database is down')
        imgs = html.findAll('span',attrs={'class':'img-fixed img-sprite'})
        if imgs:
            for tag in imgs:
                html_name = tag.get('data-alt').split(' ')[0]
                if name == html_name:
                    img = tag.get('data-src')
                    break
        else:
            print("NO IMAGES FOUND")
        return img
    ## set up things
    n_images = len(names)
    titles = names
    labels = np.array(['attack','defense','hp', 'sp_attack', 'sp_defense', 'speed'])
    angles = np.linspace(0,2*np.pi,len(labels),endpoint=False)
    angles = np.concatenate((angles,[angles[0]]))
    fig = plt.figure()
    ## add images
    images = []
    for name in names:
        response = requests.get(find_img(name))
        raw_img = Image.open(BytesIO(response.content))
        images.append(raw_img.convert('RGBA'))
    dist = [1,3]
    for n, (image,title) in enumerate(zip(images,titles)):
        subplt = fig.add_subplot(1,3,dist[n])
        plt.imshow(image,interpolation='nearest')
        subplt.axis('off')
    ## add scatterplot
    ax = fig.add_subplot(232,polar=True)
    lim = []
    for name in names:
        name_stats = stats(name)
        lim.append(max(name_stats))
        add_subplot(name_stats,name)
    ax.set_title('Stats Comparison: '+' vs. '.join(names))
    ax.set_ylim([1,max(lim)+25])
    ax.legend(names,bbox_to_anchor=[-0.5,-0.5,1.2,0])
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
    plt.show()

# In[ ]:
print('Have you ever wanted to compare the base stats of two pokemon? Well now you can!')
x = input('Enter first pokemon: ')
y = input('Enter second pokemon: ')

combined(pokemon,[x,y])
