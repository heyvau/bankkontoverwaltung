from error_handlers import catch_error


class BaseTable:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor


    @property
    def cls_name(self):
        return self.__class__.__name__


    @catch_error
    def insert(self, **kwargs):
        self.cursor.execute(
            f'INSERT INTO {self.cls_name} ({", ".join(kwargs.keys())}) \
            VALUES ({", ".join(["%s"]*len(kwargs))})',
            tuple(kwargs.values())
        ) 
        self.conn.commit()


    @catch_error
    def rows(self):
        self.cursor.execute(
            f'SELECT * FROM {self.cls_name}'
        )
        return self.cursor.fetchall()


    @catch_error
    def row(self, search_key: str, search_value):
        self.cursor.execute(
            f'SELECT * FROM {self.cls_name} \
            WHERE {search_key} = %s',
            (search_value,)
        )
        return self.cursor.fetchone()


    @catch_error
    def update(self, search_key: str, search_value, set_data: dict):
        set_data_str = ', '.join([f"{k}=%s" for k in set_data])

        self.cursor.execute(
            f'UPDATE {self.cls_name} \
            SET {set_data_str} \
            WHERE {search_key} = %s',
            (*set_data.values(), search_value)
        )
        self.conn.commit()


    @catch_error
    def delete(self, search_key: str, search_value):
        self.cursor.execute(
            f'DELETE FROM {self.cls_name} \
            WHERE {search_key} = %s',
            (search_value,)
        )
        self.conn.commit()
