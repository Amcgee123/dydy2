import pandas as pd
df=pd.read_csv(r"C:\Users\M2502074\OneDrive - Middlesbrough College\Documents\programing\python\dataanalasis 21-09_2026\screen_time_large_dataset.csv")
user=input("what user are you user1-50 ")
total_user_screentime = df.loc[df['user_id'] == user]
screentime=sum(total_user_screentime["screen_time_minutes"])
avarage_per_week=int(screentime/7)
print("",avarage_per_week,"is your avrage screentime per week")
#screentime_min = extract["screentime"].min()
print(total_user_screentime["screen_time_minutes"].max())
print(total_user_screentime["screen_time_minutes"].min())
#print(screentime_min)