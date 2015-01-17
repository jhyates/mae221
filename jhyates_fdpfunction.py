"""
Joseph Yates
MAE 221
01/13/15
Design Problem: Optimization Function
"""

# IMPORTS

from pithy import *
from CoolProp.CoolProp import Props as pr


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
    """
    except:
        out = {}
        out['T'] = 0.0
        out['H'] = 0.0
        out['S'] = 0.0
        out['Q'] = 0.0
        out['P'] = 0.0
        out['D'] = 0.0
        return out"""
    
def CycleEff(alpha, beta, gamma, delta, p_alpha, p_bravo, p_charlie, p_delta, p_echo, p_foxtrot, p_gulf, T_1, T_5):
    # GIVEN VALUES
    W_out = 100 * 1000 #kW
    cost_ele = 0.12 #$/kWh
    cost_fuel = 0.025 #$/kWh
    eta_turb = 0.85 #%
    eta_pump = 0.85 #%
    max_heat_disch = 56836.8082 #kW, based on Brayton Point Power Plant in MA w/ new regulations
    p_atm = 101.325 #kPa
    
    # MASS FRACTIONS AND STATE DEFINITIONS - VARIABLES
    
    """
    # User Inputs - Mass Fractions
    alpha = 0.1
    beta = 0.1
    gamma = 0.1
    delta = 0.1
    
    # User Inputs - Turbine Pressures
    p_alpha = 10 * 1000 #kPa
    p_bravo = 3 * 1000 #kPa
    p_charlie = 1 * 1000 #kPa
    p_delta = 500 #kPa
    p_echo = 350 #kPa
    p_foxtrot = 60 #kPa
    p_gulf = 8 #kPa
    
    # User Inputs - Steam Generator Temperatures
    T_1 = 500 + 273 #K
    T_5 = 300 + 273 #K
    """
    
    # Assumed
    q_9 = 0 #%
    q_12 = 0 #%
    q_15 = 0 #%
    q_17 = 0 #%

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
    h_14 = state[13]['H'] + beta * state[3]['H'] + alpha * state[16]['H'] - (alpha * beta) * state[17]['H']
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
    
    # WORK, TOTAL MASS FLOW, HEAT TRANSFER, THERMAL EFFICIENCY, BWR
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
    eta = (W_out - W_in) / Q_in
    bwr = W_in / W_out
    
    output = {}
    output['Qin'] = Q_in
    output['Qout'] = Q_out
    output['Win'] = W_in
    output['WP1'] = W_P1
    output['WP2'] = W_P2
    output['eta'] = eta
    output['bwr'] = bwr
    
    return output



""""""
# User Inputs - Mass Fractions
a = 0.18 # Must total to less than 1.00
b = 0.25
c = 0.05
d = 0.05

# User Inputs - Turbine Pressures
p_a = 11 * 1000 #kPa Pcrit = 22.1 MPa for water
p_b = 10.7 * 1000 #kPa
p_c = 3 * 1000 #kPa
p_d = 2 * 1000 #kPa
p_e = 1.3 * 1000 #kPa
p_f = 50 #kPa
p_g = 10 #kPa

# User Inputs - Steam Generator Temperatures
t_1 = 793 #K Tcrit = 647 K for water
t_5 = 793 #K
""""""
# User Inputs - Variable to be Optimized
""""""
top_lim = 50
bot_lim = 0.001
""""""
test = linspace(bot_lim, top_lim, 50)

op = {}

# mini = 30000000000
# maxi = 0
# mindex = 0

for i in range(len(test)):
    try:
        op[i] = CycleEff(a,b,c,d,p_a,p_b,p_c,p_d,p_e,p_f,test[i],t_1,t_5)
        # if (op[i]['eta'] > maxi):
        #     maxi = op[i]['eta']
        #     mini = op[i]['Qin']
        #     mindex = i
            
    except:
        output = {}
        output['Qin'] = 0.0
        output['Qout'] = 0.0
        output['Win'] = 0.0
        output['WP1'] = 0.0
        output['WP2'] = 0.0
        output['eta'] = 0.0
        output['bwr'] = 0.0
        op[i] = output
        
#print op
# print maxi
# print mini
# print test[mindex]

qins = []
qouts = []
wins = []
wp1s = []
wp2s = []
etas = []
bwrs = []

for i in range(len(test)):
    qins.append(op[i]['Qin'])
    qouts.append(op[i]['Qout'])
    wins.append(op[i]['Win'])
    wp1s.append(op[i]['WP1'])
    wp2s.append(op[i]['WP2'])
    etas.append(op[i]['eta'])
    bwrs.append(op[i]['bwr'])


# Plot
figure(figsize=(10,32))
subplot(5,1,1)
plot(test, qins)
ylabel("Q_in (kW)")
subplot(5,1,2)
plot(test, qouts)
ylabel("Q_out (kW)")
subplot(5,1,3)
plot(test, wins)
ylabel("W_in (kW)")
# subplot(7,1,4)
# plot(test, wp1s)
# ylabel("W_P1 (kW)")
# subplot(7,1,5)
# plot(test, wp2s)
# ylabel("W_P2 (kW)")
subplot(5,1,4)
plot(test, etas)
ylabel("Thermal Efficiency")
subplot(5,1,5)
plot(test, bwrs)
ylabel("Back Work Ratio")
showme()

