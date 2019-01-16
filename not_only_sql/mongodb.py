#-*-coding:utf-8-*
import pymongo

# 创建mongo的连接对象
client = pymongo.MongoClient()  # 'localhost'  host='mongodb://localhost:27017',port=27017

# 库
db = client.test

# 指定集合
collection = db.students

# # 插入数据
# student = {
#     'id':'201412211211',
#     'name':'sunbin',
#     'age':'18',
#     'gender':'female'
# }
#
# student2 = {
#     'id':'201412211212',
#     'name':'sunbin2',
#     'age':'18',
#     'gender':'female'
# }
#
# student3 = {
#     'id':'201412211213',
#     'name':'3sunbin2',
#     'age':'18',
#     'gender':'female'
# }
# result = collection.insert_many([student,student2,student3])
# print(result)
# print(result.inserted_ids)

result2 = collection.find_one({ 'name':'sunbin'})
print(result2)

result3 = collection.find({'name':{'regex':'^s.*'}})
print(result3)

count = collection.find().count()
print(count)

# 删除

# 1.remove()
result_remove = collection.remove({"name":"sunbin"})
print(result_remove)
# 2.delete_one()  delete_many()

result_delete = collection.delete_many({"age":{"$lt":25}})
