from database.DB_connect import DBConnect
from model.prodotto import Prodotto


class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def read_all_category():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor()
        query = """ SELECT *
                    FROM category  """
        cursor.execute(query)

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()

        return results

    @staticmethod
    def read_product(categoria):

        conn = DBConnect.get_connection()

        results = {}

        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from product
                    where category_id = %s """
        cursor.execute(query,(categoria,))

        for row in cursor:
            results[row['id']] = Prodotto(**row)

        cursor.close()
        conn.close()

        return results

    @staticmethod
    def read_vendite(prodotti,first,last):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor()
        query = """ select oi.product_id , count(*) as vendite
                    from `order` o ,order_item oi 
                    where o.id = oi.order_id  and o.order_date  between %s AND %s
                    group by oi.product_id  """
        cursor.execute(query,(first,last))

        for row in cursor:

            if row[0] in prodotti:

                results.append(row)

        cursor.close()
        conn.close()

        return results
