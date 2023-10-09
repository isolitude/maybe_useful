import glob
from torf import Torrent

add_title='{EHT PERSONALIZED TORRENT - DO NOT REDISTRIBUTE} '
your_personal_key=''


def torrentlist():
    return glob.glob('*.torrent')

def getgallarynum(string):
    indice=[index for index in range(len(string)) if string.startswith('/',index)]
    return string[indice[2]+1:indice[3]]


def addtracker(filepath):
    torrent=Torrent.read(filepath)
    k=0
    for i in torrent.trackers:
        if 'ehtracker.org' in i[0]:
            i[0]='http://ehtracker.org/'+getgallarynum(i[0])+'/'+your_personal_key+'/announce'
            print(i[0])
            k=1
    if k==1:
        torrent.write(add_title+filepath)
    else:
        print('do not find ehtracker.org')


if __name__ =='__main__' :
    tlist=glob.glob('*.torrent')
    for i in tlist:
        addtracker(i)


