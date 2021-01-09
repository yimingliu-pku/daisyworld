import matplotlib.pyplot as plt
#结果存储列表
result_avg=[]
result_dead=[]
black_cover=[]
white_cover=[]
plot_x=[(0.3+time*(1.3/200)) for time in range(200)]
#初始面积条件 以比例表示
Uncovered_Area = 1.0 
Black_Area = 0
White_Area = 0

#基础预设条件
black_albedo = 0.15#黑daisy的反照率
white_albedo = 0.65#白daisy的反照率
uncovered_albedo = 0.4#未覆盖区域的反照率
death_rate = 0.3#黑白daisy的死亡率（面积消亡比例）
heat_absorp_fact = 20#温度吸收常数，单位差距albedo所带来的局部温度差
SB_constant = 5.669e-8 #Stefan-Boltzmann常数 W/°K**4
Solar_Flux_Constant_list = [1367*2/3,1367,1367*4/3] #太阳常数 W/m2 daisyworld 表面单位面积每秒种接受的太阳辐射
Solar_Flux_Constant=Solar_Flux_Constant_list[2]
#系统运转计算平衡温度过程
for time in range(200):
    Solar_Luminosity = 0.3+(time*(1.3/200))#太阳光度系数
    save_last_tem=1000#存储上一次的daisyworld温度，设置很大的初值
    while_time=0#循环次数
    #迭代过程
    while True:
        planetary_albedo = (Uncovered_Area*uncovered_albedo)+(Black_Area*black_albedo)+(White_Area*white_albedo)#星球表面的平均albedo
        Avg_Planet_Temp = ((Solar_Luminosity*Solar_Flux_Constant*(1-planetary_albedo)/SB_constant)**0.25)-273#当前星球表面的平均温度
        if (abs(Avg_Planet_Temp-save_last_tem)<1e-9 or while_time>=1000):#足够稳定或者循环次数过多跳出
            break
        Temp_Black_Land = heat_absorp_fact*(planetary_albedo-black_albedo)+Avg_Planet_Temp#黑daisy区域温度

        Temp_White_Land = heat_absorp_fact*(planetary_albedo-white_albedo)+Avg_Planet_Temp#白daisy区域温度

        #生长因子

        Black_Growth_fact =max(0,1-0.003265*((22.5-Temp_Black_Land)**2))
        White_Growth_fact =max(0,1-0.003265*((22.5-Temp_White_Land)**2))
        #黑白daisy面积变化
        black_growth = Black_Area*(Uncovered_Area*Black_Growth_fact-death_rate)+0.001 #.001简单的初始速度，相当于“微扰”，下同，否则一直为0

        white_growth = White_Area*(Uncovered_Area*White_Growth_fact-death_rate)+0.001 
        #变化后的面积，注意，总和为1且必须均大于等于0
        Black_Area=max(black_growth+Black_Area,0)
        White_Area=max(white_growth+White_Area,0)
        Uncovered_Area=Uncovered_Area-black_growth-white_growth
        save_last_tem=Avg_Planet_Temp
        while_time+=1
    T_Dead_Planet = ((Solar_Luminosity*Solar_Flux_Constant*(1-uncovered_albedo)/SB_constant)**0.25)-273#若无daisy的温度,作为参考
    black_cover.append(Black_Area)
    white_cover.append(White_Area)
    result_avg.append(Avg_Planet_Temp)
    result_dead.append(T_Dead_Planet )

#绘图
plt.title(f'Solar_Flux_Constant={Solar_Flux_Constant:.0f}'+f'({Solar_Flux_Constant/1367:.2f}earth_S)')
plt.plot(plot_x,result_avg,color='red',label='daisy world')
plt.plot(plot_x,result_dead,color='black',label='dead world')
plt.legend()
plt.xlim(0.3,1.8)
plt.xlabel('Solar Luminosity')
plt.ylabel('Temperature/℃')
plt.savefig(r'D:\plot_daisyworld\Temperature.png')
plt.show()
plt.title(f'Solar_Flux_Constant={Solar_Flux_Constant:.0f}'+f'({Solar_Flux_Constant/1367:.2f}earth_S)')
plt.plot(plot_x,white_cover,color='red',label='white daisy')
plt.plot(plot_x,black_cover,color='black',label='black daisy')
plt.legend(loc=2)
plt.xlim(0.3,1.8)
plt.ylim(0,1.0)
plt.xlabel('Solar Luminosity')
plt.ylabel('Areal Cover')
plt.savefig(r'D:\plot_daisyworld\Areal Cover.png')
plt.show()

