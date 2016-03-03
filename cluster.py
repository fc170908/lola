import sqlite3
from sklearn.cluster import KMeans

#All fields' name
fields = ['kills', 'deaths', 'assists', 'gold_earned', 'magic_damage', 'physical_damage', 'damage', 'damage_taken',
		'crowd_control_dealt', 'ward_kills', 'wards_placed']
fields_total = ['total_kills', 'total_deaths', 'total_assists', 'total_gold_earned','total_magic_damage',
		'total_physical_damage', 'total_damage', 'total_damage_taken', 'total_crowd_control_dealt','total_ward_kills',
		'total_wards_placed']

conn = sqlite3.connect('lola.db')
cursor = conn.cursor()

#Select matches
cursor.execute('SELECT * FROM TotalChampionStats LIMIT 4000')
stats = cursor.fetchall()

all_stats = {}
all_stats_arr = []
names = []

for item in stats:
	name = item[0]
	names.append(item[0].encode('utf-8'))
	kills_percent = 1000*item[1]/item[12]
	deaths_percent = 1000*item[2]/item[13]
	assists_percent = 1000*item[3]/item[14]
	gold_percent = 1000*item[4]/item[15]
	magic_percent = 1000*item[5]/item[16]
	physical_percent = 1000*item[6]/item[17]
	damage_percent = 1000*item[7]/item[18]
	taken_percent = 1000*item[8]/item[19]
	control_percent = 1000*item[9]/item[20]
	wardK_percent = 1000*item[10]/item[21]
	wardP_percent = 1000*item[11]/item[22]
	tmp_dict = {'kills_percent': kills_percent, 'deaths_percent': deaths_percent, 'assists_percent': assists_percent,
		'gold_percent': gold_percent, 'magic_percent': magic_percent, 'physical_percent': physical_percent,
		'damage_percent': damage_percent, 'taken_percent': taken_percent, 'control_percent': control_percent,
		'wardK_percent': wardK_percent, 'wardP_percent': wardP_percent,}
	tmp_arr = [kills_percent, deaths_percent, assists_percent, gold_percent, magic_percent, physical_percent,
		damage_percent, taken_percent, control_percent, wardK_percent, wardP_percent]
	all_stats[name] = tmp_dict
	all_stats_arr.append(tmp_arr)
#for (k, v) in all_stats.items():
#	print k, '\n', v

km = KMeans(n_clusters=6, max_iter=100, n_init=10)
km.fit(all_stats_arr)

i = 0
label_dict = [[], [], [], [], [], []]
for label in km.labels_:
	label_dict[label].append(names[i])
	i += 1
for group in label_dict:
	print group

cursor.close()
conn.commit()
conn.close()