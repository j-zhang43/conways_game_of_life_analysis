import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")
avgs = df[["Initial_Density","Final_Step_Count","Final_Density"]].groupby("Initial_Density").mean().reset_index()
print(avgs)

fig, ax = plt.subplots(2,2)
ax[0,0].scatter(df["Initial_Density"]/100,df["Final_Step_Count"], s=5, linewidths=0)
ax[0,0].set_xlabel('Initial Density')
ax[0,0].set_ylabel('Final Step Count')
ax[0,0].set_title('Initial Density vs Final Step Count')
ax[0,1].scatter(avgs["Initial_Density"]/100,avgs["Final_Step_Count"], s=5, linewidths=0)
ax[0,1].set_xlabel('Initial Density')
ax[0,1].set_ylabel('Final Step Count')
ax[0,1].set_title('Initial Density vs Final Step Count Average')

ax[1,0].scatter(df["Initial_Density"]/100,df["Final_Density"], s=5, linewidths=0)
ax[1,0].set_xlabel('Initial Density')
ax[1,0].set_ylabel('Final Density')
ax[1,0].set_title('Initial Density vs Final Density')
ax[1,1].scatter(avgs["Initial_Density"]/100,avgs["Final_Step_Count"], s=5, linewidths=0)
ax[1,1].set_xlabel('Initial Density')
ax[1,1].set_ylabel('Final Step Count')
ax[1,1].set_title('Initial Density vs Final Step Count Average')
plt.tight_layout()

plt.show()

max_step_count = df.loc[df['Final_Step_Count'].idxmax()]
print(max_step_count)
