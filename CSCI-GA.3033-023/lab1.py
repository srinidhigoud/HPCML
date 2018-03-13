

# coding: utf-8

# In[41]:

import numpy as np
import time
ip = [[0.5 + ((i+j)%50-30)/50.0 for i in range(224)] for j in range (224)]
w1 = [[0.5 + ((i+j)%50-30)/50.0 for i in range(50176)] for j in range (4000)]


# In[42]:

x = []
for row in ip:
    x += row
w2 = [[0.5 + ((i+j)%50-30)/50.0 for i in range(4000)] for j in range (1000)]
z = [0]*1000


# In[43]:

def forward(mat,x):
    output = [0]*len(mat)
#     print(len(output),len(mat),len(mat[0]),len(x))
    for i in range(len(mat)):
        for j in range(len(x)):
            output[i] += mat[i][j]*x[j]
        output[i] = max(0,output[i])
    return output
        


# In[44]:

def forwardNp(A,B):
    C = np.dot(A,B)
    return C.clip(0)


# In[45]:

start_t = time.time()
z = (forward(w2,forward(w1,x)))
end_t = time.time()
total_t = end_t - start_t 
print("C2 elapsed time is:", total_t)
print("Sum of- for C2 is:",sum(z))


# In[46]:

xNP = np.array(x)
wNP1 = np.array(w1)
wNP2 = np.array(w2)
start_tNP = time.time()
zNP = (forwardNp(wNP2,forwardNp(wNP1,xNP)))
end_tNP = time.time()
total_tNP = end_tNP - start_tNP
print("C3 elapsed time is:", total_tNP)
print("Sum of- for C3 is:",sum(zNP))



# In[ ]:




# In[ ]:




# In[ ]:



