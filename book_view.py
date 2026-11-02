
import mysql.connector


class Dbconnect:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_PASSWORD",
            database="book_db"
        )

        print("Connected successfully")


class BookManager(Dbconnect):

    # CREATE - Insert book
    def post(self, **kwargs):
        try:
            cursor = self.connection.cursor()

            query = """
            INSERT INTO book_details
            (book_name, author_name, price, typee, published_year)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                kwargs['book_name'],
                kwargs['author_name'],
                kwargs['price'],
                kwargs['typee'],
                kwargs['published_year']
            )

            cursor.execute(query, values)
            self.connection.commit()

            print("Book Successfully Added")

        except Exception as e:
            print(e)

        finally:
            if 'cursor' in locals():
                cursor.close()

    # READ - Get all books
    def retrieve(self):
        try:
            cursor = self.connection.cursor()

            query = "SELECT * FROM book_details"

            cursor.execute(query)

            records = cursor.fetchall()

            return records

        except Exception as e:
            print(e)
            return []

        finally:
            if 'cursor' in locals():
                cursor.close()

    # GET OBJECT - Get single book
    def get_object(self, book_id):
        try:
            cursor = self.connection.cursor()

            query = "SELECT * FROM book_details WHERE id = %s"

            cursor.execute(query, (book_id,))

            record = cursor.fetchone()

            return record

        except Exception as e:
            print(e)
            return None

        finally:
            if 'cursor' in locals():
                cursor.close()

    # UPDATE - Update book
    def put(self, book_id, **kwargs):
        try:
            cursor = self.connection.cursor()

            query = """
            UPDATE book_details
            SET book_name = %s,
                author_name = %s,
                price = %s,
                typee = %s,
                published_year = %s
            WHERE id = %s
            """

            values = (
                kwargs['book_name'],
                kwargs['author_name'],
                kwargs['price'],
                kwargs['typee'],
                kwargs['published_year'],
                book_id
            )

            cursor.execute(query, values)
            self.connection.commit()

            if cursor.rowcount > 0:
                print("Book Successfully Updated")
            else:
                print("Book Not Found")

        except Exception as e:
            print(e)

        finally:
            if 'cursor' in locals():
                cursor.close()

    # DELETE - Delete book
    def delete(self, book_id):
        try:
            cursor = self.connection.cursor()

            query = "DELETE FROM book_details WHERE id = %s"

            cursor.execute(query, (book_id,))
            self.connection.commit()

            if cursor.rowcount > 0:
                print("Book Successfully Deleted")
            else:
                print("Book Not Found")

        except Exception as e:
            print(e)

        finally:
            if 'cursor' in locals():
                cursor.close()


# Object creation
book_instance = BookManager()


# CREATE
book_instance.post(
    book_name="Saltwater",
    author_name="Jorbin",
    price=700,
    typee="Crime Thriller",
    published_year=2000
)


# READ ALL
print("All Books:")
print(book_instance.retrieve())


# GET SINGLE OBJECT
print("Single Book:")
print(book_instance.get_object(1))


# UPDATE
book_instance.put(
    1,
    book_name="Saltwater Updated",
    author_name="Jorbin",
    price=800,
    typee="Crime Thriller",
    published_year=2000
)


# DELETE
# book_instance.delete(1)


book_instance.connection.close()
