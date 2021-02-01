import pymongo

#faz a conexão com a base de dados do Glycon no Atlas MongoDB
client = pymongo.MongoClient("mongodb://usuario:usuario@mongodbblackbook-shard-00-00-zdqhv.azure.mongodb.net:27017,mongodbblackbook-shard-00-01-zdqhv.azure.mongodb.net:27017,mongodbblackbook-shard-00-02-zdqhv.azure.mongodb.net:27017/developmentDatabase?ssl=true&replicaSet=MongoDbBlackBook-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client["productionDatabase"]
collection = db["Paciente"]


