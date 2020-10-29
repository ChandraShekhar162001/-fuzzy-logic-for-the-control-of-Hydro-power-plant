wl = {}
fr = {}

mfwl = ['Very Low','Low','Below Danger','Danger','Above Danger']
mffr = ['Very Slow','Slow','Normal','Fast','Very Fast']

mfov = {'Fully Closed':[0,0,5],'25% Opened':[0,25,50],'50% Opened':[40,50,60],'75% Opened':[50,70,90],'Fully Opened':[70,100,100]}

wl_range = [[0,0,5],[0,5,10],[5,10,15],[10,15,20],[15,20,20]]
fr_range = [[0,0,25000],[0,25000,50000],[25000,50000,75000],[50000,75000,100000],[75000,100000,100000]]


for i in range(5):
	wl[mfwl[i]] = wl_range[i]
	fr[mffr[i]] = fr_range[i]

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

water_level = ctrl.Antecedent(np.arange(0,21,1), 'Water Level')
flow_rate = ctrl.Antecedent(np.arange(0,100001,1), 'Flow Rate')
drain_valve = ctrl.Consequent(np.arange(0,101,1), 'Drain Valve')
release_valve = ctrl.Consequent(np.arange(0,101,1), 'Release Valve')

for i,j in wl.items():
	water_level[i] = fuzz.trimf(water_level.universe, j)
for i,j in fr.items():
	flow_rate[i] = fuzz.trimf(flow_rate.universe, j)

for i,j in mfov.items():
	drain_valve[i] = fuzz.trimf(drain_valve.universe, j)
	release_valve[i] = fuzz.trimf(release_valve.universe, j)

import pandas as pd
df = pd.read_csv('rules.csv')

rules = []

waterLevel = df["Water Level"].tolist()
flowRate = df["Flow Rate"].tolist()

releaseValve = df["Release Valve"].tolist()
drainValve= df["Drain Valve"].tolist()


for i in range(25):
	rules.append(ctrl.Rule(water_level[waterLevel[i]] & flow_rate[flowRate[i]], release_valve[releaseValve[i]]))
	rules.append(ctrl.Rule(water_level[waterLevel[i]] & flow_rate[flowRate[i]], drain_valve[drainValve[i]]))

dc_ctrl = ctrl.ControlSystem(rules)
dc = ctrl.ControlSystemSimulation(dc_ctrl)

dc.input["Water Level"] = int(input("Enter Water Level: "))
dc.input["Flow Rate"] = int(input("Enter Flow Rate: "))

dc.compute()

print("Drain Valve: ",dc.output["Drain Valve"],"%")
print("Release Valve: ",dc.output["Release Valve"],"%")
drain_valve.view(sim = dc)
release_valve.view(sim = dc)

plt.show()
