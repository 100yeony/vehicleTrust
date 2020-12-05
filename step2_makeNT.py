import math

# AS=10
# NT=0


def make_NT(AS) :
    #네트워크 신뢰성 관련
    distanceij = 10
    con = math.exp(-distanceij)
    print('con', con)
    # CF  = # of packets forwarded / avg number of packets observed at neighbors
    CF = 3
    NT = AS*con*CF
    return NT





#
# df = pd.DataFrame({'grp_col' : ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b'],
#                    'val' : np.arange(10)+1,
#                    'weight' : [0.0, 0.1, 0.2, 0.3, 0.4, 0.0, 0.1, 0.2, 0.3, 0.4]})
# df
#
#
# # group weighted average by category
# grouped = df.groupby('grp_col')
# weighted_avg_func = lambda g:np.average(g['val'], weights=g['weight'])
# grouped.apply(weighted_avg_func)
#
# grp_col
# a    4.0
# b    9.0
# dtype: float64
#
#
# # split
# df_a = df[df['grp_col']=='a']
# df_b = df[df['grp_col']=='b']
#
#
# # apply
# weighted_avg_a = sum((df_a['val']*df_a['weight']))/sum(df_a['weight'])
# weighted_avg_b = sum((df_b['val']*df_b['weight']))/sum(df_b['weight'])
#
#
# # combine
# weighted_avg_ab = pd.DataFrame({'grp_col': ['a', 'b'],
#                                'weighted_average': [weighted_avg_a, weighted_avg_b]})
#
# weighted_avg_ab


# make_UR(DR, AS)
# make_NT(AS)
