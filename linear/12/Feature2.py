import numpy as np
import matplotlib.pyplot as plt
plot_x=np.linspace(-0.5,5.5,200)
plot_y=(plot_x-2.5)**2+3
plt.plot(plot_x,plot_y,color='g')
plt.show()
def der_fun(x):
    return 2*(x-2.5)


def fun_val(x):
    try:
        return (x-2.5)**2+3
    except:
        return float('inf')

x=0.0
eta=0.1
epsilon=1e-8
history_x=[x]
count=0
min=0
while True:
    gradient=der_fun(x) #梯度（导数）
    last_x=x
    x=x-eta*gradient
    history_x.append(x)
    count=count+1
    if (abs(fun_val(last_x)-fun_val(x)) <epsilon):
        min=x
        break

plt.plot(plot_x,plot_y,color='g')
plt.plot(np.array(history_x),fun_val(np.array(history_x)),color='r',marker='+')
plt.show()
print ('min_x =',min)
print ('min_y =',fun_val(min)) 
print ('count =',count)


sum_eta=[]
result=[]
for i in range(5,100,5):
    x=0.0 
    eta=i*0.01
    sum_eta.append(eta)
    epsilon=1e-8 #用来判断是否满足二次函数最小值点的条件
    num=0
    min=0
    while True:
        gradient=der_fun(x) #梯度（导数）
        last_x=x
        x=x-eta*gradient
        num=num+1
        if (abs(fun_val(last_x)-fun_val(x)) <epsilon): #用来判断是否逼近最低点
            min=x
            break
    result.append(num)

plt.scatter(sum_eta,result,c='#B22222')
plt.plot(sum_eta,result,c='#00FFFF')
plt.title("relation")
plt.xlabel("eta")
plt.ylabel("count")
plt.show()
print(result)