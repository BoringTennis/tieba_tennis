from bs4 import BeautifulSoup
import re
import time
import requests
import sys

# get all matches info
idstr = '4844'
# year = [i for i in range(1993,1999)]
# year.extend([i for i in range(2000,2010)])
str1 = "http://www.wtatennis.com/fragment/wtaTennis/fragments/components/players/tournamentResultsTables/fragment_playerId/"
str2 = "/fragment_matchType/S/fragment_year/"
tournament = []
# for y in year:
url = str1+idstr+str2+str('all')
h = requests.get(url)
bsObj = BeautifulSoup(h.content,'lxml')

tournament.extend(bsObj.find_all('div',{"class":"result"}))
tourname = [tournament[i].find('a').get_text() for i in range(len(tournament))]
tourinfo = [tournament[i].find('p').get_text() for i in range(len(tournament))]
tourtime = [tourinfo[i].split('//')[2].strip() for i in range(len(tournament))]

# minor modification
# print(tourname.index('BANGKOK 13'))
# print([i for i,_ in enumerate(tourname) if _=='HONG KONG'])
# tournament.pop(178) Pierce
# tournament.pop(tourname.index('BANGKOK 13'))
# tournament.pop(148)

tournaments = []
for tm in tournament:
    matches = []
    num = (len(tm.find('tbody').contents))//2
    for n in range(num):
        matchinfo = tm.find('tbody').contents[n*2+1].find_all('td')
        match=[]
        for idx,mi in enumerate(matchinfo):
            if idx == 2:
                if len(mi.contents)==3:
                    match.append(mi.contents[1].string)
                else:
                    match.append('None')
            match.append(str(mi.string).strip())
        matches.append(match)
    tournaments.append(matches)

f = open("source/"+idstr+'.txt','w',encoding='utf-8')
for t,tname,ttime in zip(tournaments,tourname,tourtime):
    for m in t:
        m.remove('None')
        m.insert(0,tname)
        m.insert(0,ttime)
        f.writelines('%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n'%tuple(m))
f.close()

# calculate the bagels
# readin
allmatches = []
f = open("source/"+idstr+'.txt','r',encoding='utf-8')
for l in f.readlines():
    allmatches.append(list(l.split('\t')[:-1]))
f.close()

#
webpage = 'http://www.wtatennis.com/players/player/{}'.format(idstr)
h = requests.get(webpage)
bsObj = BeautifulSoup(h.content,'lxml')
idname = bsObj.find("div",{"class":"player-bio clearfix"}).find('h1',{"class":"header-2"}).string.strip()

f = open("result/"+idstr+'result.txt','w',encoding='utf-8')
f.writelines(str(idname)+' 吞蛋历史：\n')
f.writelines('---------\n')
count,countium = 0,0
for match in allmatches:
    if match[3].startswith('W'):
        if len(re.findall(r'([0]\-[6])',match[6]))>0:
            f.writelines('%s %s %s %s %s %s %s \n'%tuple(match))
            count += 1
    elif match[3].startswith('L'):
        if len(re.findall(r'([6]\-[0])',match[6]))>0:
            f.writelines('%s %s %s %s %s %s %s \n'%tuple(match))
            count+=len(re.findall(r'([6]\-[0])',match[6]))
            if len(re.findall(r'([6]\-[0])',match[6]))==2:
                countium+=1
    else:
        pass
f.writelines('---------\n')
f.writelines("总共吞蛋{}个，吞双蛋{}次".format(count,countium))
f.close()
sys.exit(0)
sys.exit(1)
