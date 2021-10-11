import mutagen 
import pandas as pd
import matplotlib.pyplot as plt
import os

def get_dir():
    valid_input = False
    user_in = ''
    while(not valid_input):
        user_in = input('Enter the address of your music directory : ')
        if os.path.isdir(user_in): #Check if existing directory
            valid_input = True
        else:
            print('Invalid address. Try again')
    if user_in.endswith('/'): #Remove undesired /
        return user_in[0:-1]
    return user_in

def get_tags(audio_file):
    got_tags = [] 
    for tag in desired_tags:
        try:
            raw_tags = audio_file.tags[tag]
            if len(raw_tags) > 1: #Extra formatting for tags with multiple values
                proc_tag = ''
                for i in raw_tags:
                    proc_tag += (i + ', ')
                got_tags.append(proc_tag[0:-2]) #Sliced as a simple way to remove extra comma and space
            else:
                got_tags.append(*raw_tags)
        except:
            got_tags.append('MISSING TAG')
    return got_tags

music_dir = get_dir()
desired_tags = ('TITLE', 'GENRE', 'ALBUM', 'ARTIST', 'TRACKNUMBER') 
audio_formats = ('.mp3', '.flac', '.wav', '.aac', '.ogg', '.aiff')
library_df = pd.DataFrame(columns=desired_tags)

for subdir, dirs, files in os.walk(music_dir):
    for file in files:
        if file.endswith(audio_formats):
            file_location = os.path.join(subdir, file)
            library_df.loc[len(library_df)] = get_tags(mutagen.File(file_location))

print(library_df)
print(library_df.describe())

fig, axes = plt.subplots(nrows=1, ncols=2)
library_df['GENRE'].value_counts().plot(ax=axes[0], figsize=(15, 10), kind='barh', color='purple', title='Genre Dist. By Track')
library_df['ARTIST'].value_counts().plot(ax=axes[1], figsize=(15, 10), kind='barh', color='green', title='Artist Dist. By Track')
plt.tight_layout(h_pad=10)

plt.savefig(music_dir + '/music_lib_visual.jpg', dpi=500)
library_df.to_csv(music_dir + '/music_lib_summary.csv')