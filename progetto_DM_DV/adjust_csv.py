import pandas as pd
import time
import maya
import datetime
import csv
import os
import math
import shutil

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def create_directory(name):
    if not os.path.exists(name):
        os.makedirs(name)

def adjust_csv(directory,origin,destination,highway):
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".csv") or filename[0]=='t':
            string=filename
            df=pd.read_csv(directory+"/"+string)
            if(len(df)!=0):
                string_split=string.split("-")
                file_day=string_split[2]
                file_month=string_split[3]
                temp=string_split[4]
                file_year=temp.split('.')[0]

                content=[]

                for i in range(len(df)):
                    pap=df.iloc[i]['TIMESTAMP']
                    plut=pap[0]
                    plut_2=pap[1]
                    plut_3=pap[2]
                    plut_4=pap[22]
                    plut_fin=pap[44] # ricordarsi che normalmente è 42
                    #for i in range(0,50):
                    #    print(i,pap[i])
                    pap_mod=pap.replace(plut,'')
                    pap_mod=pap_mod.replace(plut_2,'')
                    pap_mod=pap_mod.replace(plut_3,'')
                    pap_mod=pap_mod.replace(plut_4,'')
                    pap_mod=pap_mod.replace(plut_fin,'')
                    pap_split=pap_mod.split(',')
                    #print(pap[22])
                    timestamp=datetime.datetime.strptime(pap_split[0], "%Y-%m-%d %H:%M:%S")
                    dt = maya.parse(timestamp).datetime(to_timezone='Europe/Rome', naive=True)
                    content.append(str(dt))
                    content.append(pap_split[1])
                    content.append(pap_split[2])
                    content.append(pap_split[3])

                    if(int(file_day)==1 or int(file_day)==2 or int(file_day)==3 or int(file_day)==4
                       or int(file_day)==5 or int(file_day)==6 or int(file_day)==7 or int(file_day)==8
                       or int(file_day)==9):
                        date_origin_file=str(file_year)+"-"+"0"+str(file_month)+"-"+"0"+str(file_day)
                    else:
                        date_origin_file=str(file_year)+"-"+"0"+str(file_month)+"-"+str(file_day)

                    #print(date_origin_file)

                    directory_name="C:/Users/dasan/Desktop/DM_project_temp/{}".format(highway)
                    create_directory(directory_name)

                    with open("{}/traffic_data_{}-{}-{}-{}-{}.csv".format(directory_name,origin,destination,
                              file_day,file_month,file_year),'a+') as csv_file:
                        writer = csv.writer(csv_file)
                        if(os.stat(csv_file.name).st_size==0):
                            writer.writerows([["TIMESTAMP","DISTANCE","BASE TIME","TRAFFIC TIME"]])
                        writer.writerows([[content]])

                    content=[]

                    csv_file.close()

                df_new=pd.read_csv("{}/traffic_data_{}-{}-{}-{}-{}.csv".format(directory_name,origin,destination,
        file_day,file_month,file_year))
                for i in range(len(df_new)):
                    pap=df_new.iloc[i]['TIMESTAMP']
                    plut=pap[0]
                    plut_2=pap[1]
                    plut_fin=pap[52] # ricordarsi che normalmente è 50
                    #for i in range(0,55):
                    #    print(i,pap[i])
                    pap_mod=pap.replace(plut,'')
                    pap_mod=pap_mod.replace(plut_2,'')
                    pap_mod=pap_mod.replace(plut_fin,'')
                    pap_split=pap_mod.split(',')
                    timestamp=datetime.datetime.strptime(pap_split[0], "%Y-%m-%d %H:%M:%S")
                    content.append(str(timestamp))
                    content.append(round_up(int(pap_split[1])/1000,0))
                    content.append(round_up(int(pap_split[2])/60,0))
                    content.append(round_up(int(pap_split[3])/60,0))

                    directory_name="C:/Users/dasan/Desktop/DM_project_final_Diana/{}".format(highway)
                    create_directory(directory_name)

                    if(str(timestamp.date())==date_origin_file):
                        with open("{}/traffic_data_{}-{}-{}-{}-{}.csv".format(directory_name,origin,destination,
                                   file_day,file_month,file_year),'a+') as csv_file:
                            writer = csv.writer(csv_file)
                            if(os.stat(csv_file.name).st_size==0):
                                writer.writerows([["TIMESTAMP","DISTANCE (Km)","BASE TIME (minutes)","TRAFFIC TIME (minutes)"]])

                            writer.writerows([content])

                    if(str(timestamp.date())>date_origin_file):
                        with open("{}/traffic_data_{}-{}-{}-{}-{}.csv".format(directory_name,origin,destination,
                                   str(int(file_day)+1),file_month,file_year),'a+') as csv_file:
                            writer = csv.writer(csv_file)
                            if(os.stat(csv_file.name).st_size==0):
                                writer.writerows([["TIMESTAMP","DISTANCE (Km)","BASE TIME (minutes)","TRAFFIC TIME (minutes)"]])

                            writer.writerows([content])
                    content=[]

    shutil.rmtree("C:/Users/dasan/Desktop/DM_project_temp")

if __name__ == '__main__':

    adjust_csv("C:/Users/dasan/Desktop/DM_project_diana/A4_Milano_Bergamo","Milano","Bergamo","A4_Milano_Bergamo")
