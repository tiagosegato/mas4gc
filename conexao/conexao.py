import pymongo

client = pymongo.MongoClient("mongodb://usuario:usuario@mongodbblackbook-shard-00-00-zdqhv.azure.mongodb.net:27017,mongodbblackbook-shard-00-01-zdqhv.azure.mongodb.net:27017,mongodbblackbook-shard-00-02-zdqhv.azure.mongodb.net:27017/developmentDatabase?ssl=true&replicaSet=MongoDbBlackBook-shard-0&authSource=admin&retryWrites=true&w=majority")

collection = client["developmentDatabase"]["Paciente"]

#todos os pacientes
cursor = collection.find({})
for document in cursor:
    print(document)

#apenas um paciente
'''x = collection.find_one()
print(x)'''

### executar
### /usr/local/bin/python /Users/tiagosegatoifb/mas4gc/conexao/conexao.py