#!/usr/bin/env python
# coding: utf-8

# # 求职数据分析

# ## 读取数据

# In[1]:


import pandas as pd
data = pd.read_excel('./job_data/全国/job_data.xlsx')


# In[2]:


import re
data['标题链接'] = data['标题链接'].map(lambda x: re.sub('\?.*', '', x))
data = data.drop_duplicates(subset='标题链接')


# In[3]:


data.shape


# In[4]:


data = data[['标题', '公司地址', '公司名', '薪资下限', '薪资上限', '学历要求', '经验年限', '公司行业', '公司规模', '人员规模', '技术关键词', '公司优势与福利']]


# In[5]:


data.head()


# ## 总体分析(单维度)

# ### 全局薪资分析（柱状图、饼状图、箱线图）

# In[6]:


# 区间分布
salary_range = (data['薪资下限']+'-'+data['薪资上限']).value_counts()


# In[7]:


from JobDataVis-ShowMeAI import *

x_data = salary_range[:10].index.to_list()
y_data = salary_range[:10].values.tolist()
y_name = "职位数量"
title="薪资分布"
subtitle="高频区间段分布"

bar_salary_range = bar_plot(x_data, y_data, y_name, title, subtitle)
bar_salary_range.render("anaylysis_result_html/全局薪资分析-柱状图.html")
bar_salary_range.render_notebook()


# In[8]:


title = ""
pie_salary_raw = pie_plot_raw(x_data, y_data, title)
pie_salary_raw.render("anaylysis_result_html/全局薪资分析-饼图.html")
pie_salary_raw.render_notebook()


# In[9]:


pie_salary = pie_plot(x_data, y_data, title)
pie_salary.render("anaylysis_result_html/全局薪资分析-饼图2.html")
pie_salary.render_notebook()


# In[10]:


# 计算平均薪资
data['平均薪资'] = (data['薪资下限'].map(lambda x: int(x.replace('k', ''))) + data['薪资上限'].map(lambda x: int(x.replace('k', ''))))/2
data = data[data['平均薪资']<100]


# #### 实习生薪资分布

# In[11]:


# 筛选出实习数据
intern = data[data['标题'].str.match('(.*实习)')]
v1 = [intern['薪资下限'].value_counts().index.map(lambda x: int(x.strip('k'))).tolist()]
v2 = [intern['薪资上限'].value_counts().index.map(lambda x: int(x.strip('k'))).tolist()]
v3 = [intern['平均薪资'].values.tolist()]


# In[12]:


data_list = [v1,v2,v3]
x_label = '实习薪资'
y_labe_list = ['薪资下限', '薪资上限', '平均薪资']

box_intern_salary_raw = box_plot_raw(data_list, x_label, y_labe_list, title)
box_intern_salary_raw.render("anaylysis_result_html/实习生薪资分析-箱型图.html")
box_intern_salary_raw.render_notebook()


# #### 社招薪资分布

# In[13]:


# 筛选出社招数据
# job = data[~data['标题'].str.match('(.*实习)')]
job = data[data['平均薪资']>=12]
v1 = [job['薪资下限'].value_counts().index.map(lambda x: int(x.strip('k'))).tolist()]
v2 = [job['薪资上限'].value_counts().index.map(lambda x: int(x.strip('k'))).tolist()]
v3 = [job['平均薪资'].values.tolist()]


# In[14]:


data_list = [v1,v2,v3]
x_label = '社招薪资'
y_labe_list = ['薪资下限', '薪资上限', '平均薪资']

box_salary_raw = box_plot_raw(data_list, x_label, y_labe_list, title)
box_salary_raw.render("anaylysis_result_html/社招薪资分析-箱型图.html")
box_salary_raw.render_notebook()


# #### 薪资top10的招聘

# In[15]:


# 薪资top10的招聘
top_data = data.sort_values(by='平均薪资', ascending=False).head(15).copy()
top_data = top_data.loc[:,:'人员规模']
top_data['薪资'] = top_data['薪资下限']+'-'+top_data['薪资上限']
top_data = top_data.drop(['薪资下限', '薪资上限'], axis=1)


# In[16]:


table_df = top_data
title = 'top10高薪岗位'

table = show_table(table_df, title)
table.render("anaylysis_result_html/top10高薪岗位.html")
table.render_notebook()


# ### 算法方向分析(柱状图、词云)

# In[17]:


# 标题处理
import re
data['算法方向'] = data['标题'].map(lambda x: re.sub('算法.*', '算法', x))
algo_type = data['算法方向'].value_counts()


# In[18]:


# 柱状图
x_data = algo_type[:7].index.to_list()
y_data = algo_type[:7].values.tolist()
y_name = "职位数量"
title="算法方向分布"
subtitle="方向关键词"

bar_algo_type = bar_plot(x_data, y_data, y_name, title, subtitle)
bar_algo_type.render("anaylysis_result_html/算法方向分析-柱状图.html")
bar_algo_type.render_notebook()


# In[19]:


# 词云
algo_type_data = zip(algo_type.index.to_list(), algo_type.values.tolist())
series_name="算法方向分析"
title="算法方向分析"
word_size_range=[18, 50]

wc_algo_type = word_cloud(series_name, title, word_size_range, algo_type_data)
wc_algo_type.render("anaylysis_result_html/算法方向分析-词云.html")
wc_algo_type.render_notebook()


# ### 城市分布分析（柱状图、饼图、地理图、tree图）

# In[20]:


data['城市'] = data['公司地址'].map(lambda x: x.split('·')[0])
city = data['城市'].value_counts()


# In[21]:


# 柱状图
x_data = city[:10].index.to_list()
y_data = city[:10].values.tolist()
y_name = "职位数量"
title="招聘城市分布"
subtitle = ""

bar_city = bar_plot(x_data, y_data, y_name, title, subtitle)
bar_city.render("anaylysis_result_html/招聘城市分析-柱状图.html")
bar_city.render_notebook()


# In[22]:


# 词云
city_data = zip(city.index.to_list(), city.values.tolist())
series_name="城市分布"
title="招聘城市分布"
word_size_range=[25, 68]

wc_city = word_cloud(series_name, title, word_size_range, city_data)
wc_city.render("anaylysis_result_html/招聘城市分析-词云.html")
wc_city.render_notebook()


# In[23]:


# 树状图
tree_data = [{"value":x[0], "name":x[1]} for x in zip(city.values.tolist(), city.index.tolist())]
title = "城市分布树状图"
des = "岗位分布树状图"

tree_map_city_raw = tree_map_plot_raw(tree_data, title, des)
tree_map_city_raw.render("anaylysis_result_html/招聘城市分析-树图.html")
tree_map_city_raw.render_notebook()


# In[24]:


# Geo图
geo_city_data = zip(city.index.tolist(), city.values.tolist())
des = "招聘主要城市分布"
title = "招聘城市分布"
label_show = False

geo_city_plot_effect_scatter = geo_plot_effect_scatter(geo_city_data, label_show, title, des)
geo_city_plot_effect_scatter.render("anaylysis_result_html/招聘城市分析-GEO图.html")
geo_city_plot_effect_scatter.render_notebook()


# ### 热门区域（柱状图、词云、tree图）

# In[25]:


data['区域'] = data['公司地址'].replace('浦东新…', '浦东新区').map(lambda x: x.split('·')[-1])
district = data['区域'].value_counts()


# In[26]:


# 柱状图
x_data = district[:10].index.to_list()
y_data = district[:10].values.tolist()
y_name = "职位数量"
title="招聘区域分布"
subtitle = ""

bar_district = bar_plot(x_data, y_data, y_name, title, subtitle)
bar_district.render("anaylysis_result_html/招聘区域分析-柱状图.html")
bar_district.render_notebook()


# In[27]:


# 词云
district_data = zip(district.index.to_list(), district.values.tolist())
series_name="区域分布"
title="招聘区域分布"
word_size_range=[25, 68]

wc_district = word_cloud(series_name, title, word_size_range, district_data)
wc_district.render("anaylysis_result_html/招聘区域分布-词云.html")
wc_district.render_notebook()


# In[28]:


# 树状图
tree_data = [{"value":x[0], "name":x[1]} for x in zip(district.values.tolist(), district.index.tolist())]
title = "地区分布树状图"
des = "岗位分布树状图"

tree_map_district_raw = tree_map_plot_raw(tree_data, title, des)
tree_map_district_raw.render("anaylysis_result_html/招聘区域分析-树图.html")
tree_map_district_raw.render_notebook()


# ### 热门公司（柱状图、词云）

# In[29]:


company = data['公司名'].value_counts()


# In[30]:


# 柱状图
x_data = company[:10].index.to_list()
y_data = company[:10].values.tolist()
y_name = "职位数量"
title="头部公司"
subtitle = ""

bar_company = bar_plot(x_data, y_data, y_name, title, subtitle)
bar_company.render("anaylysis_result_html/招聘头部公司-柱状图.html")
bar_company.render_notebook()


# In[31]:


# 词云
company_data = zip(company.index.to_list(), company.values.tolist())
series_name="公司分布"
title="招聘公司分布"
word_size_range=[25, 68]

wc_company = word_cloud(series_name, title, word_size_range, company_data)
wc_company.render("anaylysis_result_html/招聘公司分布-词云.html")
wc_company.render_notebook()


# ### 学历要求（柱状图、饼图）

# In[32]:


ac_level = data['学历要求'].value_counts()


# In[33]:


# 柱状图
x_data = ac_level[:8].index.to_list()
y_data = ac_level[:8].values.tolist()
y_name = "职位数量"
title="学历要求"
subtitle = ""

bar_ac_level = bar_plot(x_data, y_data, y_name, title, subtitle)
bar_ac_level.render("anaylysis_result_html/学历要求-柱状图.html")
bar_ac_level.render_notebook()


# In[34]:


# 饼图
pie_ac_level = pie_plot(x_data, y_data, title)
pie_ac_level.render("anaylysis_result_html/学历-饼图.html")
pie_ac_level.render_notebook()


# ### 工作经验（柱状图、饼图）

# In[35]:


exp = data['经验年限'].value_counts()


# In[36]:


# 柱状图
x_data = exp[:8].index.to_list()
y_data = exp[:8].values.tolist()
y_name = "职位数量"
title="工作经验要求"
subtitle = ""

bar_exp = bar_plot(x_data, y_data, y_name, title, subtitle)
bar_exp.render("anaylysis_result_html/工作经验要求-柱状图.html")
bar_exp.render_notebook()


# In[37]:


# 饼图
pie_exp = pie_plot(x_data, y_data, title)
pie_exp.render("anaylysis_result_html/工作经验要求-饼图.html")
pie_exp.render_notebook()


# ### 公司规模（柱状图、饼图）

# In[38]:


comp_level = data['公司规模'].value_counts()


# In[39]:


# 柱状图
x_data = comp_level[:8].index.to_list()
y_data = comp_level[:8].values.tolist()
y_name = "职位数量"
title="公司规模"
subtitle = ""

bar_comp_level = bar_plot(x_data, y_data, y_name, title, subtitle)
bar_comp_level.render("anaylysis_result_html/公司规模分布-柱状图.html")
bar_comp_level.render_notebook()


# In[40]:


# 饼图
pie_comp_level = pie_plot(x_data, y_data, title)
pie_comp_level.render("anaylysis_result_html/公司规模分布-饼图.html")
pie_comp_level.render_notebook()


# ### 人员规模（柱状图、饼图）

# In[41]:


emp_num = data['人员规模'].value_counts()


# In[42]:


# 柱状图
x_data = emp_num[:8].index.to_list()
y_data = emp_num[:8].values.tolist()
y_name = "职位数量"
title="人员规模"
subtitle = ""

bar_emp_num = bar_plot(x_data, y_data, y_name, title, subtitle)
bar_emp_num.render("anaylysis_result_html/人员规模分布-柱状图.html")
bar_emp_num.render_notebook()


# In[43]:


# 饼图
pie_emp_num = pie_plot(x_data, y_data, title)
pie_emp_num.render("anaylysis_result_html/人员规模分布-饼图.html")
pie_emp_num.render_notebook()


# ### 公司行业（柱状图、词云）

# In[44]:


industry = pd.Series(data['公司行业'].str.split(',').apply(pd.Series, 1).stack().str.split('｜').apply(pd.Series, 1).stack().values).value_counts()


# In[45]:


# 柱状图
x_data = industry[:7].index.to_list()
y_data = industry[:7].values.tolist()
y_name = "职位数量"
title="公司行业分布"
subtitle = ""

bar_industry = bar_plot(x_data, y_data, y_name, title, subtitle)
bar_industry.render("anaylysis_result_html/公司行业分布-柱状图.html")
bar_industry.render_notebook()


# In[46]:


# 词云
industry_data = zip(industry.index.to_list(), industry.values.tolist())
series_name="行业分布"
title="行业分布"
word_size_range=[25, 68]

wc_industry = word_cloud(series_name, title, word_size_range, industry_data)
wc_industry.render("anaylysis_result_html/公司行业分布-词云.html")
wc_industry.render_notebook()


# ### 领域&技术关键词（柱状图、词云、tree图）

# In[47]:


keywords = pd.Series(data['技术关键词'].map(lambda x: re.sub('\s+', ',', str(x))).str.split(',').apply(pd.Series, 1).stack().values).value_counts()


# In[48]:


# 柱状图
x_data = keywords[:7].index.to_list()
y_data = keywords[:7].values.tolist()
y_name = "职位数量"
title="领域&技术关键词"
subtitle = ""

bar_keywords = bar_plot(x_data, y_data, y_name, title, subtitle)
bar_keywords.render("anaylysis_result_html/领域-技术关键词-柱状图.html")
bar_keywords.render_notebook()


# In[49]:


# 词云
keywords_data = zip(keywords.index.to_list(), keywords.values.tolist())
series_name="领域&关键词"
title="领域&关键词"
word_size_range=[25, 68]

wc_keywords = word_cloud(series_name, title, word_size_range, keywords_data)
wc_keywords.render("anaylysis_result_html/领域-关键词-词云.html")
wc_keywords.render_notebook()


# In[50]:


# 树状图
tree_data = [{"value":x[0], "name":x[1]} for x in zip(keywords.values.tolist(), keywords.index.tolist())]
title = "关键词分布树状图"
des = "关键词分布树状图"

tree_map_keywords_raw = tree_map_plot_raw(tree_data, title, des)
tree_map_keywords_raw.render("anaylysis_result_html/招聘关键词分析-树图.html")
tree_map_keywords_raw.render_notebook()


# ### 公司福利与优势（词云）

# In[51]:


extra_info = pd.Series(data['公司优势与福利'].map(lambda x: re.sub('(，\s*)|(；\s*)|(、\s*)|(\s+)', ',', x)).str.split(',').apply(pd.Series, 1).stack().values).value_counts()


# In[52]:


# 词云
extra_info_data = zip(extra_info.index.to_list(), extra_info.values.tolist())
series_name="福利&优势"
title="福利&优势"
word_size_range=[25, 68]

wc_industry = word_cloud(series_name, title, word_size_range, extra_info_data)
wc_industry.render("anaylysis_result_html/公司福利优势-词云.html")
wc_industry.render_notebook()

