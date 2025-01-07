import numpy as np 
population_size=100
degisken_sayisi=2

mutation_rate = 0.1
#deneme=np.random.randint(min_price,max_price,size=(population_size,degisken_sayisi))

data=[]
def generate_population(population_size):
    kilolar=np.random.randint(0,100,100)
    
    fiyatlar=np.array(list(map(lambda x:np.random.randint(x,x+300),kilolar)))
    yem_cesit=np.random.randint(0,4,100)
    global data
    data=np.column_stack((kilolar,fiyatlar,yem_cesit))
    return data

birim_fiyat=[]
def birim_fiyat(data):
    global birim_fiyat
    birim_fiyat=data[:,1]/data[:,0]
    

def fitness_func(population):
    toplam_kg=0
    price=0
    idxs=np.where(population==1)
    for i in range(len(idxs[0])):
        toplam_kg+=data[idxs[0][i]][0]
        price+=data[idxs[0][i]][1]
    return toplam_kg,price,idxs
    
def crossover(parent1,parent2):
    crossover_point=np.random.randint(0,len(parent1)-1)
    
    child1=np.concatenate((parent1[:crossover_point],parent2[crossover_point:len(parent1)]))
    child2=np.concatenate((parent2[:crossover_point],parent1[crossover_point:len(parent2)] ))
    return child1,child2
    
def mutation(ind):
    rnd=np.random.randint(0,100)
    if ind[rnd]==0:
        ind[rnd]=1
    elif ind[rnd]==1:
        ind[rnd]=0
    return ind,rnd
    
generate_population(population_size)

birim_fiyat(data)
hangiUrun=np.argsort(birim_fiyat)
siralanmis=np.sort(birim_fiyat)


kromozom_list=[]
fiyat_liste=[]
kilo_listesi=[]
for j in range(0,100):# bu döngü 100 tane başlangıç kromozomu üretiyor rastgele
    i=0
    kilo_toplam=0
    fiyat_toplam=0

    kromozom=np.zeros(100) # 100 tane satıcı oldugunu dusunerek yaptım
    rnd_list=[]
    while True:
        
            
        rnd_sayi=np.random.randint(0,100)
        if rnd_sayi not in rnd_list:
            rnd_list.append(rnd_sayi)
        else:
            continue
        kilo_toplam+=data[rnd_sayi,[0]]
        fiyat_toplam+=data[rnd_sayi,[1]]
        kromozom[rnd_sayi]=1
        i+=1
        
        if fiyat_toplam>=1990:
            
            break
    kromozom_list.append([kilo_toplam,kromozom])
    fiyat_liste.append(fiyat_toplam)
    kilo_listesi.append(kilo_toplam)
    

kilo_listesi=np.squeeze(kilo_listesi)  #burda sorted işlemini yapabilmek için bunu kullandım boyut azaltma
sorted_population=sorted(kilo_listesi,reverse=True) 

sorted_population_argsort=np.argsort(kilo_listesi) 
sorted_population_argsort=sorted_population_argsort[::-1]

elite_kromozom_indices=sorted_population_argsort[:20] # 20 tane en yüksek kiloyu veren kromozom seçildi
selected_kromozom_indices=sorted_population_argsort[20:100]

elite_kromozoms=[kromozom_list[x][1] for x in elite_kromozom_indices]# burda indislerine göre kromozomları çektim
selected_kromozoms=[kromozom_list[x] for x in selected_kromozom_indices]

offspring=[]
for k in range(0,len(selected_kromozoms),2):
    parent1,parent2=selected_kromozoms[k],selected_kromozoms[k+1]
    child1,child2=crossover(parent1[1], parent2[1])
    mute1=mutation(child1)
    mute2=mutation(child2)
    offspring.append(child1)
    offspring.append(child2)
    
main_population=np.concatenate( (elite_kromozoms,offspring))
best_ind=main_population[0]

kilo,fiyat,idxs=fitness_func(best_ind)

print("En iyi değer için \n kilo:{}, fiyat:{}".format(kilo,fiyat))

