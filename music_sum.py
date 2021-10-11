import mutagen 
import pandas as pd
import matplotlib.pyplot as plt
import os

music_dir = '/home/aid/Music'
desired_tags = ('TITLE', 'GENRE', 'ALBUM', 'TRACKNUMBER') 
audio_formats = ('.mp3', '.flac', '.wav', '.aac', '.ogg', '.aiff')
library_df = pd.DataFrame(columns=desired_tags)

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
            got_tags.append("MISSING TAG")
    return got_tags

for subdir, dirs, files in os.walk(music_dir):
    for file in files:
        if file.endswith(audio_formats):
            file_location = os.path.join(subdir, file)
            library_df.loc[len(library_df)] = get_tags(mutagen.File(file_location))

print(library_df)
print(library_df.describe())

library_df['GENRE'].value_counts().plot(kind='bar')
plt.show()

library_df.to_csv(music_dir + '/music_lib_summary.csv')