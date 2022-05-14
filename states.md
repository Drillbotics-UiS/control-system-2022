States:
0: 
- Manuell styring via GUI

10: 
- Automatisk start
- Kjør hositing opp til limit switch

20:
- Mål "hook load"(?)

30:
- Kjør hoisting ned
- 5% økning på WOB (weight on bit) (for å vite når vi treffer blokken)
- Lagre høyde sensor H0

40:
- Kjør hoisting opp til WOB = Hook Load

50:
- Kjør stabiliser på plass

60:
- Kjør stabiliser ut

70: 
- Top drive
- WOB
- PID
- H >= H0 + 10cm

80:
- WOB PID
- Pressure PID
- H >= H0 + Target depth
