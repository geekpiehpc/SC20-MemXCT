import numpy as np
f=open('main.o.optrpt','r')
scalar_cost=[]
vector_cost=[]
estimated_potential_speedup=[]

for line in f.readlines():
    if 'scalar cost' in line:
        value=float(line.strip().split(': ')[-1])
        scalar_cost.append(value)
    elif 'vector cost' in line and ' ---' not in line:
        value=float(line.strip().split(': ')[-1])
        vector_cost.append(value)
    elif 'estimated potential speedup' in line:
        value=float(line.strip().split(': ')[-1])
        estimated_potential_speedup.append(value)
# scalar_cost.remove(max(scalar_cost))
print(scalar_cost)
print(vector_cost)
print(estimated_potential_speedup)
print('np.mean(scalar_cost)',np.mean(scalar_cost))
print('np.mean(vector_cost)',np.mean(vector_cost))
print('np.mean(estimated_potential_speedup)',np.mean(estimated_potential_speedup))