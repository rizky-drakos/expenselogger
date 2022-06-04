import logging

from common                     import K_PRICE, K_USERNAME, K_DATENAME, K_NAME, K_DATE, TABLE_NAME
from decimal                    import Decimal
from boto3                      import resource
from boto3.dynamodb.conditions  import Key
from botocore.exceptions        import ClientError

class LivingExpenseDB():

    def __init__(self):
        try:
            self.livingExpenseTable = resource('dynamodb', 'ap-south-1').Table(TABLE_NAME)
            if self.livingExpenseTable.table_status != 'ACTIVE':
                raise ClientError("The requested table is not ACTIVE!")
        except Exception as error:
            logging.error('Errors in connecting to table {}, details:\n{}'.format(TABLE_NAME, error))
        else:
            logging.info('Successfully connected to table {}'.format(TABLE_NAME))

    def __transform_items(self, items):
        """
        Transforms the format of items returned by DynamoDB so that they become
        compatible with response outputs. 
        
        :param  items:
        """
        for item in items:
            item[K_PRICE] = int(item[K_PRICE])
            item[K_NAME] = item[K_DATENAME].split('#')[1]
            item[K_DATE] = item[K_DATENAME].split('#')[0]
            del item[K_DATENAME]
        return items

    def create_item(self, username, name, date, price):
        """
        Dynamo API calls for creating an item.
        
        :param  username  :
        :param  name    :
        :param  date    :
        :param  price   :
        """
        try:
            self.livingExpenseTable.put_item(
                Item = {
                    K_USERNAME: username,
                    K_DATENAME: "{}#{}".format(date, name),
                    K_PRICE: price
                }
            )
        except ClientError as error:
            logging.error('Errors in creating an item, details:\n{}'.format(error))
        else:
            logging.info('Successfully created an item.')

    def get_items(self, username):
        """
        Dynamo API calls for retrieving items by a given date.
        
        :param  username  :
        :param  name    :
        :param  date    :
        :param  price   :
        :return: 
        """
        try:
            rs = self.livingExpenseTable.query(KeyConditionExpression = Key(K_USERNAME).eq(username))
        except ClientError as error:
            logging.error('Errors in retrieving items, details:\n{}'.format(error))
            return None
        else:
            logging.info('Successfully retrieved items.')
            return self.__transform_items(rs['Items'])

    def get_items_by_date(self, username, date):
        """
        Dynamo API calls for retrieving items by a given date.
        
        :param  username  :
        :param  name    :
        :param  date    :
        :param  price   :
        :return: 
        """
        try:
            rs = self.livingExpenseTable.query(
                KeyConditionExpression = Key(K_USERNAME).eq(username) & Key(K_DATENAME).begins_with(date)
            )
        except ClientError as error:
            logging.error('Errors in retrieving items, details:\n{}'.format(error))
            return None
        else:
            logging.info('Successfully retrieved items.')
            return self.__transform_items(rs['Items'])

    def update_item(self, name, date, price, username):
        """
        Dynamo API calls for updating an item.
        
        :param  username  :
        :param  name    :
        :param  date    :
        :param  price   :
        """
        try:
            self.livingExpenseTable.update_item(
                Key={K_USERNAME: username, K_DATENAME: "{}#{}".format(date, name)},
                UpdateExpression = "SET {} = :priceVal".format(K_PRICE),
                ExpressionAttributeValues = { ':priceVal': Decimal(price) }
            )
        except Exception as error:
            logging.error('Errors in updating an item, details:\n{}'.format(error))
        else:
            logging.info('Successfully updated an item.')

    def delete_item(self, name, date, username):
        """
        Dynamo API calls for deleting an item.
        
        :param  username  :
        :param  name    :
        :param  date    :
        """
        try:
            self.livingExpenseTable.delete_item(
                Key={K_USERNAME: username, K_DATENAME: "{}#{}".format(date, name)},
            )
        except Exception as error:
            logging.error('Errors in deleting an item, details:\n{}'.format(error))
        else:
            logging.info('Successfully deleted an item.')
