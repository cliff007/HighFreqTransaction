# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 22:00:29 2016

@author: Hao Lyn
         Xinyue Zhou
         Lynyun Zhao
"""
import numpy as np
import pandas as pd
data1 = pd.read_csv("../data/AAPL_05222012_0930_1300_LOB_2.csv")
data1=data1.dropna()
#data1 = pd.read_csv("AAPL_05222012_0930_1300_LOB_2.csv")
# column name
col1 = list(data1.columns.values)[2:62]
len(col1)
col2 = [i[16:] for i in col1]
new_names = list(data1.columns.values)[0:2]+ [i[:-19] for i in col2]
data1.columns = new_names

### First do all the operations on all data #####
# delete times
# data1 = data1.head(203350)
# data1.shape
# data1.head(10)

#create desired names 
level  = range(1,11)
"BID_PRICE"+str(level[1])
bidpc_name = ["BID_PRICE"+str(level[i]) for i in range(10)]
askpc_name = ["ASK_PRICE"+str(level[i]) for i in range(10)]
bidsz_name = ["BID_SIZE"+str(level[i]) for i in range(10)]
asksz_name = ["ASK_SIZE"+str(level[i]) for i in range(10)]

################################### feature 2 ######################################
level = np.arange(10)+1
bid_P = "BID_PRICE"
ask_P = "ASK_PRICE"
ask_V = "BID_SIZE"
bid_V = "ASK_SIZE"

def feature2_1(dataset):
    ret = pd.DataFrame()
    for i in level:
        ret["diff_ab" + str(i)] = data1[bid_P + str(i)] - data1[ask_P + str(i)]
    return ret

def feature2_2(dataset):
    ret = pd.DataFrame()
    for i in level:
        ret["mid_ab" + str(i)] = (data1[bid_P + str(i)]+data1[ask_P + str(i)])/2
    return ret

##################################### feature 3 ########################################
bidlist = range(2,62,6)
asklist = range(5,65,6)
def feature3(data):
    bid = data.ix[:,bidlist]
    bid_feature = abs(bid.diff(axis = 1).ix[:,range(1,10)])
    names = ["bid"+str(i+1)+"-"+"bid"+str(i) for i in range(1,10)]
    bid_feature.columns = names
    bid_feature2 = pd.DataFrame(bid["BID_PRICE1"] - bid["BID_PRICE10"])
    bid_feature2.columns = ["bid1-bid10"]
    bid_feature = pd.concat([bid_feature,bid_feature2],axis=1)
    ask = data.ix[:,asklist]
    ask_feature = abs(ask.diff(axis = 1).ix[:,range(1,10)])
    names = ["ask"+str(i+1)+"-"+"ask"+str(i) for i in range(1,10)]
    ask_feature.columns = names
    ask_feature2 = pd.DataFrame(ask["ASK_PRICE1"] - ask["ASK_PRICE10"])
    ask_feature2.columns = ["ask1-ask10"]
    ask_feature = pd.concat([ask_feature,ask_feature2],axis=1)
    v3 = pd.concat([ask_feature,bid_feature],axis=1)
    return v3;


# v3 = v3feature(data1)
# v3.shape

##################################### feature4 #######################################
def feature4 (data,level=10) :
    askpc_mean=np.sum(data1.ix[:,askpc_name],axis=1)/level
    bidpc_mean=np.sum(data1.ix[:,bidpc_name],axis=1)/level
    asksz_mean=np.sum(data1.ix[:,asksz_name],axis=1)/level
    bidsz_mean=np.sum(data1.ix[:,bidsz_name],axis=1)/level
    askpc_mean=askpc_mean.tolist()
    bidpc_mean=bidpc_mean.tolist()
    asksz_mean=asksz_mean.tolist()
    bidsz_mean=bidsz_mean.tolist() 
    v4 = pd.DataFrame({"Mean_Ask_Price":askpc_mean,"Mean_Bid_Price":bidpc_mean,
                  "Mean_Ask_Size":asksz_mean,"Mean_Bid_Size":bidsz_mean})
    return v4
# v4 = feature4(data1,10)
# v4.head(10)

##################################### feature5 ########################################
def feature5 (data):
    pc_diff = np.sum(data1.ix[:,askpc_name],axis=1)- np.sum(data1.ix[:,bidpc_name],axis=1)
    sz_diff = np.sum(data1.ix[:,asksz_name],axis=1)- np.sum(data1.ix[:,bidsz_name],axis=1)
    pc_diff = pc_diff.tolist()
    sz_diff = sz_diff.tolist()
    v5 = pd.DataFrame({"Acc_Price_Diff":pc_diff,"Acc_Size_Diff":sz_diff})
    return v5;
# v5 = feature5(data1)
# v5.head(10)


##################################### feature 6 #######################################
volbidlist = range(4,64,6)
volasklist = range(7,67,6)
def feature6(data,delta = 30):
    v6_1 = pd.concat([data.ix[:,bidlist],data.ix[:,asklist]],axis=1).diff(periods = delta, axis = 0).ix[delta:,:]/delta
    v6_2 = pd.concat([data.ix[:,volbidlist],data.ix[:,volasklist]],axis=1).diff(periods = delta, axis = 0).ix[delta:,:]/delta
    v6 = pd.concat([v6_1,v6_2],axis = 1)
    v6 = pd.concat([pd.DataFrame(index=range(0,delta), columns=v6.columns.values),v6],axis = 0)
    v6.index =range(data.shape[0])
    v6.columns = ["Deriv "+ x for x in bidpc_name]+["Deriv "+ x for x in askpc_name]+["Deriv "+ x for x in bidsz_name]+["Deriv "+ x for x in asksz_name]
    return v6;
#v6= feature6(data1)
#v6

#################################### feature 7 #######################################
#define ratio
def volumn_ratio (data):
    v_ratio=np.sum(data1.ix[:,asksz_name[0:4]],axis=1)/np.sum(data1.ix[:,bidsz_name[0:4]],axis=1)
    v_ratio=v_ratio.tolist()
    volumn_ratio = pd.DataFrame({"top_five_volumn_ratio":v_ratio})
    return volumn_ratio;

# volumn_ratio(data1).head(10)


###feature 8 
def mid_diff(data,delta=30):
    mid = data["mid_ab1"].tolist()
    result = np.zeros(len(mid)).tolist()
    result2 = np.zeros(len(mid)).tolist()
    for i in range(delta,len(mid)):
        sub = mid[i-delta:i]
        result[i]=(max(sub)+min(sub))/2
        result2[i] = np.mean(sub)
    mid_diff = np.array(mid) - np.array(result)
    mid_diff2 = np.array(mid) - np.array(result2)
    mid_diff = pd.DataFrame({"mid_diff_hl":mid_diff,"mid_diff_mean":mid_diff2})
    return mid_diff;


###feature 9
def aroon(data,delta=30):
    mid = data["mid_ab1"].tolist()
    n_high = np.zeros(len(mid)).tolist()
    n_low = np.zeros(len(mid)).tolist()
    up_ind = np.zeros(len(mid)).tolist()
    down_ind = np.zeros(len(mid)).tolist()
    for i in range(delta,len(mid)):
        sub = mid[i-delta:i]
        ix_max = sub.index(max(sub))
        ix_min = sub.index(min(sub))
        n_high[i] = delta-ix_max
        n_low[i] = delta-ix_min
        up_ind[i] = 100*(ix_max/delta)
        down_ind[i] = 100*(ix_min/delta)
    aroon_ind = pd.DataFrame({"SinceHigh":n_high,"SinceLow":n_low,"UpIndicator":up_ind,"DownIndicator":down_ind})
    return aroon_ind;

###feature 10
def mid_sd(data,delta=30):
    mid = data["mid_ab1"].tolist()
    mid_sd = np.zeros(len(mid)).tolist()
    for i in range(delta,len(mid)):
        sub = mid[i-delta:i]
        mid_sd[i] = np.std(sub)
    mid_sd = pd.DataFrame({"mid_sd":mid_sd})
    return mid_sd;

################
#### labels ####
################

################################### Mid-price ######################################
def label_midprice(dataset,step):
    tmp =  dataset["mid_ab1"].diff(periods = step)
    Y_midprice = pd.Series(np.nan, index= range(dataset.shape[0]),name="Y_midprice")
    Y_midprice[tmp>0] = "upward"
    Y_midprice[tmp<0] = "downward"
    Y_midprice[tmp==0] = "stationary"
    Y_midprice[0:-step] =  Y_midprice[step:]
    Y_midprice[-step:] = np.nan
    return Y_midprice
  
# sum(Y_midprice=="downward"),sum(Y_midprice=="upward")
#label_midprice(temp,step)


############################# Bid-ask spread crossing ###############################
def label_spread(dataset, step):
    bid_t2 = pd.Series(0, index= range(dataset.shape[0]))
    bid_t2[0:-step] = dataset["BID_PRICE1"][step:]
    indc1 = bid_t2 - dataset["ASK_PRICE1"]
    
    ask_t2 = pd.Series(0, index= range(dataset.shape[0]))
    ask_t2[0:-step] = dataset["ASK_PRICE1"][step:]
    indc2 = ask_t2 - dataset["BID_PRICE1"]
    Y_spread = pd.Series("stationary", index= range(dataset.shape[0]))
    Y_spread[indc1>0] = "upward"
    Y_spread[indc2<0] = "downward"
    Y_spread[-step:] = np.nan
    return pd.DataFrame({"Y_spread":Y_spread})






###############################
#### some helper functions ####
###############################

# merge dataset
def merge_dataset(dataset_ls):

    """
    Input
    -----
    List of DataFrame with the same index (number of rows)

    Output
    ------
    A big merged DataFrame
    """

    n = len(dataset_ls)
    ret = pd.DataFrame(index = range(data1.shape[0]))
    for i in dataset_ls:
        ret = pd.concat([ret,i],axis = 1)
    return ret


# randomly select given ratio
def random_subset(dataset,label,size,ratio = (1,1,2),RT = True):

    """
    Input
    -------- 
        dataset - Whole dataset with all features and labels
        label   - Name of a label, for example 'Y_midprice'
        ratio   - a tuple,  (upward, downward, stationary) ratio, eg: (1,1,2)
        size    - The size of subset 
        RT      - If given the ratio or not. If not, just randomly select indices.
    Output
    ------
        dataframe -  a dataframe of subset
    """
    np.random.seed(12345)
    if (RT ==False):
        indx = set(np.random.choice(dataset.index,replace=False,size = size))
        rest_indx = set(dataset.index) - indx
        ret = dataset.loc[np.sort(list(indx)),:]
        rest_data = dataset.loc[np.sort(list(rest_indx)),:]
        return ret,rest_data
    n_u,n_d,n_s = int(ratio[0]/sum(ratio)*size),int(ratio[1]/sum(ratio)*size),int(ratio[2]/sum(ratio)*size )
    xin = dataset["Y_spread"].value_counts()
    num_u,num_d,num_s = xin.loc["upward"],xin.loc["downward"],xin.loc["stationary"]
    r_u,r_d,r_s = False,False,False
    if (num_u < n_u):
        r_u = True
    if (num_d < n_d):
        r_d = True
    if (num_s < n_s):
        r_s = True
        
    ind_u = list(dataset[dataset[label]=="upward"].index)
    ind_d = list(dataset[dataset[label]=="downward"].index)
    ind_s = list(dataset[dataset[label]=="stationary"].index)
    indice = np.array([])
    indice = np.append(indice,np.random.choice(ind_u,replace=r_u,size = n_u))
    indice = np.append(indice,np.random.choice(ind_d,replace=r_d,size = n_d))
    indice = np.append(indice,np.random.choice(ind_s,replace=r_s,size = n_s))
    temp = set(np.sort(indice).astype(int))
    rest_ind = set(dataset.index) - temp
    ret = dataset.loc[np.sort(list(temp)),:]
    rest_data = dataset.loc[np.sort(list(rest_ind)),:]
    return ret,rest_data

######### preprocession script ##########
tmp = feature2_2(data1)

mid_step = 40
list_df = [data1.ix[:,np.concatenate((bidlist,asklist,volbidlist,volasklist))], feature2_1(data1), feature2_2(data1), feature3(data1), feature4(data1), feature5(data1),feature6(data1,40),volumn_ratio(data1),mid_diff(tmp,delta=40),aroon(tmp,delta=40),mid_sd(tmp,40),label_midprice(tmp,step=40),label_spread(data1,step=40)]
data_all = merge_dataset(list_df)
# delete times (time 9:30-11:00)
data_9to11 = data_all.head(203350)
data_9to11 = data_9to11.dropna()

mid_step = 100
list_df_spread = [data1.ix[:,np.concatenate((bidlist,asklist,volbidlist,volasklist))], feature2_1(data1), feature2_2(data1), feature3(data1), feature4(data1), feature5(data1),feature6(data1,mid_step),volumn_ratio(data1),mid_diff(tmp,delta=mid_step),aroon(tmp,delta=mid_step),mid_sd(tmp,mid_step),label_midprice(tmp,step=mid_step),label_spread(data1,step=mid_step)]
data_all_spread = merge_dataset(list_df_spread)
# delete times (time 9:30-11:00)
data_9to11_spread = data_all_spread.head(203350)
data_9to11_spread = data_9to11_spread.dropna()

train_set_midprice,rest_set_midprice = random_subset(data_9to11,"Y_midprice",30000, (3,3,1))
test_set_midprice = random_subset(rest_set_midprice,"Y_midprice",50000,RT = False)[0]
train_set_spread, rest_set_spread = random_subset(data_9to11_spread,"Y_spread",30000, (1,1,2))
test_set_spread = random_subset(rest_set_spread,"Y_spread",50000,RT = False)[0]
predict_data_midprice = data_all.ix[203350: ,]
predict_data_spread = data_all_spread.ix[203350: ,]
#predict_data = predict_data.dropna()
#create train_set and test_set
train_set_midprice.to_csv("../data/train_set_midprice.csv",index = False)
test_set_midprice.to_csv("../data/test_set_midprice.csv",index = False)
train_set_spread.to_csv("../data/train_set_spread.csv",index = False)
test_set_spread.to_csv("../data/test_set_spread.csv",index = False)
predict_data_midprice.to_csv("../data/predict_data_midprice.csv",index = False)
predict_data_spread.to_csv("../data/predict_data_spread.csv",index = False)
