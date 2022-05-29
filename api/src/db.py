from common                     import K_PRICE, K_USERID, K_NAMEDATE, K_NAME, K_DATE
from decimal                    import Decimal
from boto3                      import resource
from boto3.dynamodb.conditions  import Key

class LivingExpenseDB():

    def __init__(self):
        try:
            self.livingExpenseTable = resource('dynamodb').Table('livingexpense')
            if self.livingExpenseTable.table_status != 'ACTIVE':
                raise ValueError("The requested table is not ACTIVE!")
        except Exception as error:
            pass

    def create_item(self, userid, name, date, price):
        try:
            self.livingExpenseTable.put_item(
                Item = {
                    K_USERID: userid,
                    K_NAMEDATE: "{}_{}".format(name, date),
                    K_PRICE: price
                }
            )
        except Exception as error:
            pass

    def get_items_by_userid(self, userid=1):
        try:
            rs = self.livingExpenseTable.query(KeyConditionExpression=Key(K_USERID).eq(userid))
            for item in rs['Items']:
                item[K_PRICE] = int(item[K_PRICE])
                item[K_USERID] = int(item[K_USERID])
                item[K_NAME] = item[K_NAMEDATE].split('_')[0]
                item[K_DATE] = item[K_NAMEDATE].split('_')[1]
                del item[K_NAMEDATE]
            return rs['Items']
        except Exception as error:
            pass

    def update_item_by_userid(self, name, date, price, userid=1):
        try:
            self.livingExpenseTable.update_item(
                Key={K_USERID: userid, K_NAMEDATE: "{}_{}".format(name, date)},
                UpdateExpression = "SET {} = :priceVal".format(K_PRICE),
                ExpressionAttributeValues = { ':priceVal': Decimal(price) }
            )
        except Exception as error:
            pass

    def delete_item_by_userid(self, name, date, userid=1):
        try:
            self.livingExpenseTable.delete_item(
                Key={K_USERID: userid, K_NAMEDATE: "{}_{}".format(name, date)},
            )
        except Exception as error:
            pass
