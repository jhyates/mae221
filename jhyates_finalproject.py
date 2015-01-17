"""
Joseph Yates
MAE 221
01/13/15
Design Problem: Notes and Code
"""

# IMPORTS

from pithy import *
from CoolProp.CoolProp import Props as pr

"""
GOALS:
- Minimize Qin, Win
- Maximize Efficiency
- Minimize Fuel Cost
- Maximize Profit/Value over 30 years

ASSUMPTIONS:
- Design is basis for modern power plants
- 100 MW = W*out
- $0.12 kW/h price of electricity
- $0.025 kW/h cost of fuel
- Maximum heat rejection to environment can be found: ???
- Valves isenthalpic
- 0.85 turbine efficiency
- Heat exchangers isobaric
- Investigate:
    Condenser produces saturated liquid?
    Pumps and Turbines isentropic?
    Depreciation rate?
    One 100 MW Turbine, or 6 that total to 100 MW? (also for other components)

DEFINE MASS FLOW CONVENTIONS
Total Mass Flow: mf
Mass fraction that breaks away at turbine 1: alpha
Mass flow that breaks away at turbine 2: m_2
Mass flow that breaks away after turbine 4: m_4
Mass flow that breaks away after turbine 5: m_5


IMPLIED PROPERTIES OF THE STATES
1 
2 85% efficiency 
3 85% efficiency 
4 p5 = p4; 85% efficiency
5 
6 85% efficiency 
7 85% efficiency 
8 85% efficiency 
9 p9 = p8; q9 = 0
10 p10 = p6; 85% efficiency assumed
11 p11 = p6; 
12 p12 = p6; q12 = 0
13 p13 = p1; 85% efficiency assumed
14 p14 = p1; 
15 p15 = p2; q15 = 0
16 p16 = p3; h16 = h15
17 p17 = p3; q17 = 0
18 p18 = p6; h18 = h17
19 p19 = p7; q19 = 0 <- later changed to not overdefine the system; q19 != 0
20 p20 = p8; h20 = h19
21 p21 = p1; 

IDEAS:
- Make flows that exit exchangers saturated liquid (qX = 0) as well - thus q12 = q15 = q17 = q19 = 0?
- Use large mass flows to reduce delta enthalpy requirements - see turbine, etc. stats sheets. This however, will NOT reduce Qin or Win
- Make Qout small
- Reduce Qin and Win
- Increase Wout

- Brayton Point Power Plant (Somerset, MA) heat discharge: 1.7 billion BTU/year = 56836808.2 W = 56.837 MW [Q_out]; source: http://yosemite.epa.gov/opa/admpress.nsf/6d651d23f5a91b768525735900400c28/350c2ad3e01ed983852573f3007d3222!OpenDocument

"""

# FUNCTIONS

def pp(var,unit):
    print "%s=%s %s" % (var,round(eval(var),3),unit)    

def stater(arg1,arg2,arg3,arg4):
    out = {}
    out['T'] = pr('T',arg1,arg2,arg3,arg4,'water') #K
    out['H'] = pr('H',arg1,arg2,arg3,arg4,'water') #kJ/kg
    out['S'] = pr('S',arg1,arg2,arg3,arg4,'water') #kJ/(kg*K)
    out['Q'] = pr('Q',arg1,arg2,arg3,arg4,'water') #%
    out['P'] = pr('P',arg1,arg2,arg3,arg4,'water') #kPa
    out['D'] = pr('D',arg1,arg2,arg3,arg4,'water') #kg/m^3
    return out
    
def setupTSPlot():
    Tcrit = pr('water', 'Tcrit')
    Ts = linspace(275,Tcrit,100)
    envelope0 = pr('S', 'T', Ts, 'Q', 0, 'water')
    envelope1 = pr('S', 'T', Ts, 'Q', 1, 'water')
    ss = linspace(envelope0[0], envelope1[0], 100)
    envelope = concatenate( (envelope0, list(reversed(envelope1))))
    Ts2 = concatenate( (Ts, list(reversed(Ts))) )
    figure(figsize=(10,8))
    plot(envelope, Ts2, 'black')
    xlabel("S (kJ *K / kg)")
    ylabel("T (K)")
    ylim( [min(Ts) / 1.5,Tcrit * 1.25] )
    return ss
    
def setupPVPlot():
    Pcrit = pr('water', 'pcrit')
    Ps = linspace(1,Pcrit,100) #Min 1 kPa
    envelope0 = (1/pr('D', 'P', Ps, 'Q', 0, 'water'))
    envelope1 = (1/pr('D', 'P', Ps, 'Q', 1, 'water'))
    vs = linspace(envelope0[0], envelope1[0], 100)
    envelope = concatenate( (envelope0, list(reversed(envelope1))))
    Ps2 = concatenate( (Ps, list(reversed(Ps))) )
    figure(figsize=(10,8))
    plot(envelope, Ps2, 'black')
    xlabel("v (m^3/kg)")
    ylabel("P (kPa)")
    loglog()
    #xlim([0,4])
    #ylim([0,30*1000])
    #ylim( [min(Ps) / 1.5,Pcrit * 1.25] )
    return vs
    
    
def setupPHPlot():
    Pcrit = pr('water', 'pcrit')
    Ps = linspace(1,Pcrit,100) #Min 225 kPa
    envelope0 = pr('H', 'P', Ps, 'Q', 0, 'water')
    envelope1 = pr('H', 'P', Ps, 'Q', 1, 'water')
    hs = linspace(envelope0[0], envelope1[0], 100)
    envelope = concatenate( (envelope0, list(reversed(envelope1))))
    Ps2 = concatenate( (Ps, list(reversed(Ps))) )
    figure(figsize=(10,8))
    plot(envelope, Ps2, 'black')
    xlabel("h (kJ/kg)")
    ylabel("P (kPa)")
    loglog()
    #ylim( [min(Ps) / 1.5,Pcrit * 1.25] )
    return hs
    

def drawIsobar(p, ss):
    pCurve = pr('T', 'P', p, 'S', ss, 'water')
    plot(ss, pCurve, '0.6')

def drawIsotherm(T, vs):
    ds = 1/vs
    TCurve = pr('P', 'T', T, 'D', ds, 'water')
    plot(vs, TCurve, '0.6')




# GIVEN VALUES

W_out = 100 * 1000 #kW
cost_ele = 0.12 #$/kWh
cost_fuel = 0.025 #$/kWh
eta_turb = 0.85 #%
eta_pump = 0.85 #%
max_heat_disch = 56836.8082 #kW, based on Brayton Point Power Plant in MA w/ new regulations
p_atm = 101.325 #kPa

# MASS FRACTIONS AND STATE DEFINITIONS - VARIABLES

""""""
# User Inputs - Mass Fractions
alpha = 0.18
beta = 0.25
gamma = 0.05
delta = 0.05

# User Inputs - Turbine Pressures
p_alpha = 11 * 1000 #kPa Pcrit = 22.1 MPa for water
p_bravo = 10.7 * 1000 #kPa
p_charlie = 3 * 1000 #kPa
p_delta = 2000 #kPa
p_echo = 1300 #kPa
p_foxtrot = 50 #kPa
p_gulf = 10 #kPa

# User Inputs - Steam Generator Temperatures
T_1 = 793 #K Tcrit = 647 K for water
T_5 = 793 #K
""""""

# Assumed
q_9 = 0 #%
q_12 = 0 #%
q_15 = 0 #%
q_17 = 0 #%

""" UNUSED VARIABLES AFTER MASS FRACTIONS DEFINED
#T_11 = 80 + 273 #K
#T_14 = 200 + 273 #K
#T_15 = 200 + 273 #K
#T_21 = 280 + 273 #K
#q_19 = 0 #%
"""


# STATE DEFINITIONS - DEPENDENTS

state = {}

#State 1
#SG-T1
state[1] = stater('P',p_alpha,'T',T_1)

#State 2s
s_2s = state[1]['S']
state['2s'] = stater('P',p_bravo,'S',s_2s)

#State 2
#T1-T2
h_2 = state[1]['H']-eta_turb*(state[1]['H']-state['2s']['H'])
state[2] = stater('P',p_bravo,'H',h_2)

#State 3s
s_3s = state[2]['S']
state['3s'] = stater('P',p_charlie,'S',s_3s)

#State 3
#T2-T3
h_3 = state[2]['H']-eta_turb*(state[2]['H']-state['3s']['H'])
state[3] = stater('P',p_charlie,'H',h_3)

#State 4s
s_4s = state[3]['S']
state['4s'] = stater('P',p_delta,'S',s_4s)

#State 4
#T3-SGREHEAT
h_4 = state[3]['H']-eta_turb*(state[3]['H']-state['4s']['H'])
state[4] = stater('P',p_delta,'H',h_4)

#State 5
#SGREHEAT-T4
state[5] = stater('P',p_delta,'T',T_5)

#State 6s
s_6s = state[5]['S']
state['6s'] = stater('P',p_echo,'S',s_6s)

#State 6
#T4-T5
h_6 = state[5]['H']-eta_turb*(state[5]['H']-state['6s']['H'])
state[6] = stater('P',p_echo,'H',h_6)

#State 7s
s_7s = state[6]['S']
state['7s'] = stater('P',p_foxtrot,'S',s_7s)

#State 7
#T5-T6
h_7 = state[6]['H']-eta_turb*(state[6]['H']-state['7s']['H'])
state[7] = stater('P',p_foxtrot,'H',h_7)

#State 8s
s_8s = state[7]['S']
state['8s'] = stater('P',p_gulf,'S',s_8s)

#State 8
#T6-CO
h_8 = state[7]['H']-eta_turb*(state[7]['H']-state['8s']['H'])
state[8] = stater('P',p_gulf,'H',h_8)

#State 9
#CO-P1
state[9] = stater('P',p_gulf,'Q',q_9)

#State 10s
s_10s = state[9]['S']
state['10s'] = stater('P',p_echo,'S',s_10s)

#State 10
#P1-H1
#h_10 = state[9]['H']-eta_pump*(state[9]['H']-state['10s']['H'])
h_10 = (state['10s']['H'] - state[9]['H']) / eta_pump + state[9]['H']
state[10] = stater('P',p_echo,'H',h_10)

#State 11 requires State 18 definition in order to solve for the open feedwater heater (H0)

#State 12
#H0-P2
state[12] = stater('P',p_echo,'Q',q_12)

#State 13s
s_13s = state[12]['S']
state['13s'] = stater('P',p_alpha,'S',s_13s)

#State 13
#P2-H2
#h_13 = state[12]['H']-eta_pump*(state[12]['H']-state['13s']['H'])
h_13 = (state['13s']['H'] - state[12]['H']) / eta_pump + state[12]['H']
state[13] = stater('P',p_alpha,'H',h_13)

# State 14 requires State 16 and State 17 definitions in order to solve for the closed feedwater heater 2 (H2)

#State 15
#H3-V3
state[15] = stater('P',p_bravo,'Q',q_15)

#State 16
#V3-H2
state[16] = stater('P',p_charlie,'H',state[15]['H'])

#State 17
#H2-V2
state[17] = stater('P',p_charlie,'Q',q_17)

#State 14
#H2-H3, solve closed feedwater heater 2 (H2)
h_14 = state[13]['H'] + beta * state[3]['H'] + alpha * state[16]['H'] - (alpha + beta) * state[17]['H']
state[14] = stater('P',p_alpha,'H',h_14)

#State 18
#V2-H0
state[18] = stater('P',p_echo,'H',state[17]['H'])

#State 11
#H1-H0, solve open feedwater heater (H0)
h_11 = (state[12]['H'] - gamma * state[6]['H'] - (alpha + beta) * state[18]['H']) / (1 - alpha - beta - gamma)
state[11] = stater('P',p_echo,'H',h_11)

#State 19
#H1-V1, solve closed feedwater heater 1 (H1). Used to be solved with q_19 = 0
h_19 = state[7]['H'] - ( (1 - alpha - beta - gamma) * (state[11]['H'] - state[10]['H']) / delta)
state[19] = stater('P',p_foxtrot,'H',h_19)

#State 20
#V1-CO
state[20] = stater('P',p_gulf,'H',state[19]['H'])

#State 21
#H3-SG, solve closed feedwater heater 3 (H3)
h_21 = state[14]['H'] + alpha * (state[2]['H'] - state[15]['H'])
state[21] = stater('P',p_alpha,'H',h_21)


# CYCLE EXCEPTIONS
if ((-1.0 < state[1]['Q'] < 0.9) or (-1.0 < state[2]['Q'] < 0.9) or (-1.0 < state[3]['Q'] < 0.9) or (-1.0 < state[4]['Q'] < 0.9) or (-1.0 < state[5]['Q'] < 0.9) or (-1.0 < state[6]['Q'] < 0.9) or (-1.0 < state[7]['Q'] < 0.9) or (-1.0 < state[8]['Q'] < 0.9)):
    print "Turbine quality error!"

if not(((state[7]['T'] > state[11]['T']) and (state[19]['T'] > state[10]['T'])) or ((state[7]['T'] > state[10]['T']) and (state[19]['T'] > state[11]['T']))):
    print "Closed Feedwater Heater 1 Temperature Error!"

if not(((state[2]['T'] > state[21]['T']) and (state[15]['T'] > state[14]['T'])) or ((state[2]['T'] > state[14]['T']) and (state[15]['T'] > state[21]['T']))):
    print "Closed Feedwater Heater 3 Temperature Error!"

if not((((state[3]['T'] > state[14]['T']) or (state[16]['T'] > state[14]['T'])) and (state[17]['T'] > state[13]['T'])) or (((state[3]['T'] > state[13]['T']) or (state[16]['T'] > state[13]['T'])) and (state[17]['T'] > state[14]['T']))):
    print "Closed Feedwater Heater 2 Temperature Error!"


# WORK, TOTAL MASS FLOW, HEAT TRANSFER, THERMAL EFFICIENCY, BWR
"""
# GIVEN VALUES
W_out = 100 * 1000 #kW
max_heat_disch = 56836.8082 #kW, based on Brayton Point Power Plant in MA
"""
mf = W_out / ((state[1]['H'] - state[2]['H']) + (1 - alpha) * (state[2]['H'] - state[3]['H']) + (1 - alpha - beta) * (state[3]['H'] - state[4]['H']) + (1 - alpha - beta) * (state[5]['H'] - state[6]['H']) + (1 - alpha - beta - gamma) * (state[6]['H'] - state[7]['H']) + (1 - alpha - beta - gamma - delta) * (state[7]['H'] - state[8]['H'])) # dear god

# Solve steam generator for Q_in
Q_in = mf * (state[1]['H'] - state[21]['H']) + mf * (1 - alpha - beta) * (state[5]['H'] - state[4]['H'])

# Solve condenser for Q_out
Q_out = mf * (1 - alpha - beta - gamma - delta) * state[8]['H'] + mf * delta * state[20]['H'] - mf * (1 - alpha - beta - gamma) * state[9]['H']

# Solve pumps for W_in *** KEEP VALUE POSITIVE AND SUBTRACT ***
W_P1 = mf * (1 - alpha - beta - gamma) * (state[10]['H'] - state[9]['H'])
W_P2 = mf * (state[13]['H'] - state[12]['H'])
W_in = W_P1 + W_P2

# Thermal Efficiency and Back Work Ratio
eta_th = (W_out - W_in) / Q_in
bwr = W_in / W_out
#???: ((state[10]['H'] - state[9]['H']) + (state[13]['H'] - state[12]['H'])) / (

# Print
print "Heat and Power Properties:\n"
print "W_out: " + (str)(W_out) + " kW\n"
print "W_in: " + (str)(W_in) + " kW\n"
print "Q_out: " + (str)(Q_out) + " kW\n"
print "Q_in: " + (str)(Q_in) + " kW\n"
print "Mass Flow: " + (str)(mf) + " kg/s\n"
print "Thermal Efficiency: " + (str)(eta_th) + "\n"
print "Back Work Ratio: " + (str)(bwr) + "\n"

legal = ""
if Q_out < max_heat_disch:
    legal = "Yes!"
else:
    legal = "No!"
print "Is this heat rejection into a body of water legal in Somerset, MA? " + legal + "\n\n"
# Put it somewhere else!



# COST, REVENUE, DISCOUNTING, ?????, PROFIT
#cost_ele = 0.12 #$/kWh
#cost_fuel = 0.025 #$/kWh
#Note that the plant's cash flow is the same each year, since it is assumed that the plant draws and outputs constant amounts of power over the time period

plantcost = 1000 * W_out + 100000000 #$; Determined from component pricing and cost to construct Brayton Point cooling towers (2009)
hrsyr = 8765.81277 #hr/yr, for unit conversions to use correct periods
cashflow = cost_ele * hrsyr * (W_out - W_in) - cost_fuel * hrsyr * Q_in #$/year
dr = 0.01
period = 30 #years, INTEGERS ONLY
profitafter = 0
positiveboolean = 0

NPV = 0 - plantcost # "At time 0..." 
for t in range(1, period):
    NPV += cashflow / ((1 + dr) ** t)
    if ((positiveboolean == 0) & (NPV >= 0.0)):
        profitafter = t
        positiveboolean = 1
    
print "Economics:\n"
print "Cost to Build: $" + (str)(plantcost) + "\n"
print "Annual Cash Flow: $" + (str)(cashflow) + "\n"
print "Net Present Value: $" + (str)(NPV) + "\n"
print "Profit After: " + (str)(profitafter) + " years\n"


# PRETTY TABLE -----

keys = state[1].keys()
stiller = """
<style>
    table{
        font-family: Helvetica;
        font-size:13px;
    }
    
    td
    {
        padding:5px;
    }
    </style>
"""
print stiller.replace("\n","\r")

print "<table><tr><td></td>",
for k in keys:
    print "<td>%s</td>" % k,
print "</tr>",

for i in range(1,22):
    print "<tr><td>",
    print i,
    print "</td>",
    for k in keys:
        try: a = round(state[i][k],3)
        except: a = round(state[i][k][p],3)
        print "<td>",a,"</td>",
    print "</tr>",
print "</table>"


# DATASETS FOR PLOTTING - FUN

# Isobars for T-s Diagram

# Process 4-5, for main loop
s45 = linspace(state[4]['S'],state[5]['S'],40)
T45 = pr('T','S',s45,'P',state[4]['P'],"water")
# Process 14-21, for main loop
s1421 = linspace(state[14]['S'],state[21]['S'],40)
T1421 = pr('T','S',s1421,'P',state[14]['P'],"water")
# Process 21-1, for main loop
s211 = linspace(state[21]['S'],state[1]['S'],40)
T211 = pr('T','S',s211,'P',state[21]['P'],"water")
# Process 2-15, for alpha fraction loop
s215 = linspace(state[2]['S'],state[15]['S'],40)
T215 = pr('T','S',s215,'P',state[2]['P'],"water")
# Process 6-11, for gamma fraction loop
s612 = linspace(state[6]['S'],state[12]['S'],50)
T612 = pr('T','S',s612,'P',state[12]['P'],"water")
# Process 3-17, for beta fraction loop
s317 = linspace(state[3]['S'],state[17]['S'],50)
T317 = pr('T','S',s317,'P',state[3]['P'],"water")
# Process 7-19, for delta fraction loop
s719 = linspace(state[7]['S'],state[19]['S'],50)
T719 = pr('T','S',s719,'P',state[7]['P'],"water")


# MAIN LOOP
ss1 = [state[1]['S'], state[2]['S'], state[3]['S'], state[4]['S']]#, state[5]['S'], state[6]['S'], state[7]['S'], state[8]['S'], state[9]['S'], state[10]['S'], state[11]['S'], state[12]['S'], state[13]['S'], state[14]['S']]#, state[21]['S'], state[1]['S']]
Ts1 = [state[1]['T'], state[2]['T'], state[3]['T'], state[4]['T']]#, state[5]['T'], state[6]['T'], state[7]['T'], state[8]['T'], state[9]['T'], state[10]['T'], state[11]['T'], state[12]['T'], state[13]['T'], state[14]['T']]#, state[21]['T'], state[1]['T']]
for i in range(len(s45)):
    ss1.append(s45[i])
    Ts1.append(T45[i])
ss1.append(state[5]['S'])
Ts1.append(state[5]['T'])
ss1.append(state[6]['S'])
Ts1.append(state[6]['T'])
ss1.append(state[7]['S'])
Ts1.append(state[7]['T'])
ss1.append(state[8]['S'])
Ts1.append(state[8]['T'])
ss1.append(state[9]['S'])
Ts1.append(state[9]['T'])
ss1.append(state[10]['S'])
Ts1.append(state[10]['T'])
ss1.append(state[11]['S'])
Ts1.append(state[11]['T'])
ss1.append(state[12]['S'])
Ts1.append(state[12]['T'])
ss1.append(state[13]['S'])
Ts1.append(state[13]['T'])
ss1.append(state[14]['S'])
Ts1.append(state[14]['T'])
for i in range(len(s1421)):
    ss1.append(s1421[i])
    Ts1.append(T1421[i])
ss1.append(state[21]['S'])
Ts1.append(state[21]['T'])
for i in range(len(s211)):
    ss1.append(s211[i])
    Ts1.append(T211[i])

Ps1 = [state[1]['P'], state[2]['P'], state[3]['P'], state[4]['P'], state[5]['P'], state[6]['P'], state[7]['P'], state[8]['P'], state[9]['P'], state[10]['P'], state[11]['P'], state[12]['P'], state[13]['P'], state[14]['P'], state[21]['P'], state[1]['P']]
hs1 = [state[1]['H'], state[2]['H'], state[3]['H'], state[4]['H'], state[5]['H'], state[6]['H'], state[7]['H'], state[8]['H'], state[9]['H'], state[10]['H'], state[11]['H'], state[12]['H'], state[13]['H'], state[14]['H'], state[21]['H'], state[1]['H']]
vs1 = [1/state[1]['D'], 1/state[2]['D'], 1/state[3]['D'], 1/state[4]['D'], 1/state[5]['D'], 1/state[6]['D'], 1/state[7]['D'], 1/state[8]['D'], 1/state[9]['D'], 1/state[10]['D'], 1/state[11]['D'], 1/state[12]['D'], 1/state[13]['D'], 1/state[14]['D'], 1/state[21]['D'], 1/state[1]['D']]

# ALPHA FRACTION LOOP
ss2 = [state[2]['S']]#, state[15]['S'], state[16]['S'], state[17]['S']]
Ts2 = [state[2]['T']]#, state[15]['T'], state[16]['T'], state[17]['T']]
for i in range(len(s215)):
    ss2.append(s215[i])
    Ts2.append(T215[i])
ss2.append(state[15]['S'])
Ts2.append(state[15]['T'])
ss2.append(state[16]['S'])
Ts2.append(state[16]['T'])
ss2.append(state[17]['S'])
Ts2.append(state[17]['T'])


Ps2 = [state[2]['P'], state[15]['P'], state[16]['P'], state[17]['P']]
hs2 = [state[2]['H'], state[15]['H'], state[16]['H'], state[17]['H']]
vs2 = [1/state[2]['D'], 1/state[15]['D'], 1/state[16]['D'], 1/state[17]['D']]

# BETA FRACTION LOOP
ss3 = [state[3]['S']]#, state[17]['S'], state[18]['S'], state[12]['S']]
Ts3 = [state[3]['T']]#, state[17]['T'], state[18]['T'], state[12]['T']]
Ps3 = [state[3]['P'], state[17]['P'], state[18]['P'], state[12]['P']]
hs3 = [state[3]['H'], state[17]['H'], state[18]['H'], state[12]['H']]
vs3 = [1/state[3]['D'], 1/state[17]['D'], 1/state[18]['D'], 1/state[12]['D']]
for i in range(len(s317)):
    ss3.append(s317[i])
    Ts3.append(T317[i])
ss3.append(state[17]['S'])
Ts3.append(state[17]['T'])
ss3.append(state[18]['S'])
Ts3.append(state[18]['T'])
ss3.append(state[12]['S'])
Ts3.append(state[12]['T'])

# GAMMA FRACTION LOOP
ss4 = [state[6]['S']]
Ts4 = [state[6]['T']]
for i in range(len(s612)):
    ss4.append(s612[i])
    Ts4.append(T612[i])
ss4.append(state[12]['S'])
Ts4.append(state[12]['T'])


Ps4 = [state[6]['P'], state[12]['P']]
hs4 = [state[6]['H'], state[12]['H']]
vs4 = [1/state[6]['D'], 1/state[12]['D']]

# DELTA FRACTION LOOP
ss5 = [state[7]['S']]#, state[19]['S'], state[20]['S'], state[9]['S']]
Ts5 = [state[7]['T']]#, state[19]['T'], state[20]['T'], state[9]['T']]
Ps5 = [state[7]['P'], state[19]['P'], state[20]['P'], state[9]['P']]
hs5 = [state[7]['H'], state[19]['H'], state[20]['H'], state[9]['H']]
vs5 = [1/state[7]['D'], 1/state[19]['D'], 1/state[20]['D'], 1/state[9]['D']]
for i in range(len(s719)):
    ss5.append(s719[i])
    Ts5.append(T719[i])
ss5.append(state[19]['S'])
Ts5.append(state[19]['T'])
ss5.append(state[20]['S'])
Ts5.append(state[20]['T'])
ss5.append(state[9]['S'])
Ts5.append(state[9]['T'])


# ACTUALLY PLOTTING -----
# MediumSeaGreen DarkGreen LimeGreen GreenYellow
# marker='o', linestyle='-', color='b'

#T-S Diagram
ss = setupTSPlot()
drawIsobar(p_alpha, ss)
drawIsobar(p_bravo, ss)
drawIsobar(p_charlie, ss)
drawIsobar(p_delta, ss)
drawIsobar(p_echo, ss)
drawIsobar(p_foxtrot, ss)
drawIsobar(p_gulf, ss)

plot(ss1, Ts1, linestyle='-', color='b')
plot(ss2, Ts2, linestyle='-', color='Green')
plot(ss3, Ts3, linestyle='-', color='Orange')
plot(ss4, Ts4, linestyle='-', color='DarkMagenta')
plot(ss5, Ts5, linestyle='-', color='r')
showme()

#P-V Diagram
vs = setupPVPlot()
# drawIsotherm(T_1, vs)
# drawIsotherm(T_5, vs)

plot(vs1, Ps1, linestyle='-', color='b')
plot(vs2, Ps2, linestyle='-', color='Green')
plot(vs3, Ps3, linestyle='-', color='Orange')
plot(vs4, Ps4, linestyle='-', color='DarkMagenta')
plot(vs5, Ps5, linestyle='-', color='r')
showme()

#P-H Diagram
hs = setupPHPlot()
plot(hs1, Ps1, linestyle='-', color='b')
plot(hs2, Ps2, linestyle='-', color='Green')
plot(hs3, Ps3, linestyle='-', color='Orange')
plot(hs4, Ps4, linestyle='-', color='DarkMagenta')
plot(hs5, Ps5, linestyle='-', color='r')
showme()








""" JUNK CODE, unused ideas beyond this point



# MASS FRACTIONS -----

# Solve the feedwater heaters; use enthalpies to find mass fractions
#H3 for fraction alpha
mf_alpha = (state[2]['H']-state[15]['H'])/(state[21]['H']-state[14]['H'])

#H2 for fraction beta
mf_beta = (state[14]['H'] - state[13]['H'] + mf_alpha * (state[17]['H']-state[16]['H']))/(state[3]['H'] - state[17]['H'])

#H0 for fraction gamma
mf_gamma = (state[12]['H'] - (mf_alpha + mf_beta) * state[18]['H'] - (1 - mf_alpha - mf_beta) * state[11]['H'])/(state[6]['H']-state[11]['H'])

#H1 for fraction delta
mf_delta = (1 - mf_alpha - mf_beta - mf_gamma) * (state[11]['H']-state[10]['H']) / (state[7]['H']-state[9]['H'])

#Print
print "Mass Fractions: \n"
print "Alpha: "+(str)(mf_alpha)+"\n"
print "Beta:  "+(str)(mf_beta)+"\n"
print "Gamma: "+(str)(mf_gamma)+"\n"
print "Delta: "+(str)(mf_delta)+"\n"





#ss1 = [state[1]['S'], state[2]['S'], state[3]['S'], state[4]['S'], state[5]['S'], state[6]['S'], state[7]['S'], state[8]['S'], state[9]['S'], state[10]['S'], state[11]['S'], state[12]['S'], state[13]['S'], state[14]['S'], state[15]['S'], state[16]['S'], state[17]['S'], state[18]['S'], state[19]['S'], state[20]['S'], state[21]['S']] #]#
#Ts1 = [state[1]['T'], state[2]['T'], state[3]['T'], state[4]['T'], state[5]['T'], state[6]['T'], state[7]['T'], state[8]['T'], state[9]['T'], state[10]['T'], state[11]['T'], state[12]['T'], state[13]['T'], state[14]['T'], state[15]['T'], state[16]['T'], state[17]['T'], state[18]['T'], state[19]['T'], state[20]['T'], state[21]['T']] #]#
"""