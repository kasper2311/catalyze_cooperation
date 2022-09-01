# catalyze_cooperation
 A simulation that looks to realize a single instance of the moran process described in:
 
 Gokhale, C.S., Bulbulia, J. & Frean, M. Collective narratives catalyse cooperation. Humanit Soc Sci Commun 9, 85 (2022). https://doi.org/10.1057/s41599-022-01095-7
 
 
## Requirements:
python 3 (Tested on version 3.8.8), pygame (Tested on version 2.1.2 (SDL 2.0.18)), numpy (Tested on version 1.20.1)
 
## Instructions:

 Open the file catalyze_coop.py  

 The variables will be under the commented line under the words "edit these". Once you are done,  
 
 run the script
 ```python catalyze_coop.py```

## Explanation:

 Each circle represents a single hunter.  

 The inner circle represents belief in a particular narrative  
 (**BLUE** corresponds to a belief in **narrative 1**. **YELLOW** corresponds to **narrative 2**)

 The **outer circle** represents actions taken given the group consensus
 
 (The **upper half** outer circle represents **action taken when group consensus is NARRATIVE 1**. If the color is **RED**, the hunter hunts **STAG**. If the color is **GREEN**, the hunter hunts **HARE**  
 The **lower half** outer circle represents **action taken when group consensus is NARRATIVE 2**. If the color is **RED**, the hunter hunts **STAG**. If the color is **GREEN**, the hunter hunts **HARE**)


 The ability to edit the other variables ingame will be coming shortly. I am completely new to everything that I've done for this particular project, so I apologise in advance for any issues.
