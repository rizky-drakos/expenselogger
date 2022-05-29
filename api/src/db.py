import logging

from common                     import K_PRICE, K_USERID, K_DATENAME, K_NAME, K_DATE, TABLE_NAME
from decimal                    import Decimal
from boto3                      import resource
from boto3.dynamodb.conditions  import Key
from botocore.exceptions        import ClientError

class LivingExpenseDB():

    def __init__(self):
        try:
            self.livingExpenseTable = resource('dynamodb').Table(TABLE_NAME)
            if self.livingExpenseTable.table_status != 'ACTIVE':
                raise ClientError("The requested table is not ACTIVE!")
        except Exception as error:
            logging.error('Errors in connecting to table {}, details:\n{}'.format(TABLE_NAME, error))
        else:
            logging.info('Successfully connected to table {}'.format(TABLE_NAME))

    def create_item(self, userid, name, date, price):
        """
        Dynamo API calls for creating an item.
        
        :param  userid  :
        :param  name    :
        :param  date    :
        :param  price   :
        """
        try:
            self.livingExpenseTable.put_item(
                Item = {
                    K_USERID: userid,
                    K_DATENAME: "{}#{}".format(date, name),
                    K_PRICE: price
                }
            )
        except ClientError as error:
            logging.error('Errors in creating an item, details:\n{}'.format(error))
        else:
            logging.info('Successfully created an item.')

    def get_items_by_date(self, userid, date):
        """
        Dynamo API calls for retrieving items by a given date.
        
        :param  userid  :
        :param  name    :
        :param  date    :
        :param  price   :
        :return: 
        """
        try:
            rs = self.livingExpenseTable.query(
                KeyConditionExpression = Key(K_USERID).eq(userid) & Key(K_DATENAME).begins_with(date)
            )
            for item in rs['Items']:
                item[K_PRICE] = int(item[K_PRICE])
                item[K_USERID] = int(item[K_USERID])
                item[K_NAME] = item[K_DATENAME].split('#')[0]
                item[K_DATE] = item[K_DATENAME].split('#')[1]
                del item[K_DATENAME]
        except ClientError as error:
            logging.error('Errors in retrieving items, details:\n{}'.format(error))
        else:
            logging.info('Successfully retrieved items.')
            return rs['Items']

    def update_item(self, name, date, price, userid=1):
        """
        Dynamo API calls for updating an item.
        
        :param  userid  :
        :param  name    :
        :param  date    :
        :param  price   :
        """
        try:
            self.livingExpenseTable.update_item(
                Key={K_USERID: userid, K_DATENAME: "{}#{}".format(date, name)},
                UpdateExpression = "SET {} = :priceVal".format(K_PRICE),
                ExpressionAttributeValues = { ':priceVal': Decimal(price) }
            )
        except Exception as error:
            logging.error('Errors in updating an item, details:\n{}'.format(error))
        else:
            logging.info('Successfully updated an item.')

    def delete_item(self, name, date, userid=1):
        """
        Dynamo API calls for deleting an item.
        
        :param  userid  :
        :param  name    :
        :param  date    :
        """
        try:
            self.livingExpenseTable.delete_item(
                Key={K_USERID: userid, K_DATENAME: "{}#{}".format(date, name)},
            )
        except Exception as error:
            logging.error('Errors in deleting an item, details:\n{}'.format(error))
        else:
            logging.info('Successfully deleted an item.')
