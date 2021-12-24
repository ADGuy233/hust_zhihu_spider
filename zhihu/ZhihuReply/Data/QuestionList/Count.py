import pandas as pd
file_path = r"C:\Users\bdzyl\OneDrive\论文硕士\知乎豆瓣\Spiders\Data\QuestionList\questionlist.csv"
Data = pd.read_csv(file_path)
# 以排序方式为essence的问题列表中的qid为种子
question_list_essence = Data[Data['sortby']=="essence"]['qid'].to_list()
question_list = list(set(question_list_essence))
print(len(question_list))