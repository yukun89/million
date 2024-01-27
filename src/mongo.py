#!/usr/bin/python3
#not use mongo now
import time
import pymongo
import api.the_block as block

class Mongo(object):
    def __init__(self, address="mongodb://localhost:27017/", database="million"):
        self.myclient_ = pymongo.MongoClient(address)
        self.mydb_ = self.myclient_[database]
        return

    def insert_many(self, table, lines):
        mycol=self.mydb_[table]
        mycol.insert_many(lines)
        return

    def create_index(self, table, index_content, unique=True):
        mycol=self.mydb_[table]
        mycol.create_index(index_content, unique)
        return

    def collection(self, table):
        return self.mydb_[table]


if __name__ == '__main__':
    mymongo = Mongo()
    theblock = block.TheBlock()
    data_list = theblock.get_daily_transactions('BTC')
    lines = []
    for each in data_list:
        each['Symbol'] = 'BTC';
        lines.append(each)
    mymongo.collection('daily_data').delete_many({})
    mymongo.collection('daily_data').insert_many(lines)
    print(mymongo.collection('daily_data').find().limit(3))
    filters={'Symbol':'BTC', 'Timestamp':{'$gt':int(time.time() - 3600*72)}}
    print(mymongo.collection('daily_data').find(filters, {'_id':0}))
    mymongo.collection('daily_data').create_index([('Timestamp',1), ('Symbol',1)], unique=True)

