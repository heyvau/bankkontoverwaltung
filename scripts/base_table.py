from __future__ import annotations
from error_handlers import catch_error


class BaseTable:
    def __init__(
            self, 
            conn, cursor,
            fields: tuple[str],
            pk: str,
            references: list[BaseTable] = [],
            fk: str | None = None
            ) -> None:

        self.conn = conn
        self.cursor = cursor
        self.fields = fields
        self.pk = pk
        self.references = references
        self.fk = fk


    @property
    def cls_name(self):
        return self.__class__.__name__


    @catch_error
    def insert(self, **kwargs) -> None:
        self.cursor.execute(
            f'INSERT INTO {self.cls_name} ({", ".join(kwargs.keys())}) \
            VALUES ({", ".join(["%s"]*len(kwargs))})',
            tuple(kwargs.values())
        ) 
        self.conn.commit()


    @catch_error
    def rows(self, **kwargs) -> list[dict]:
        if not kwargs:
            self.cursor.execute(
                f'SELECT * FROM {self.cls_name}'
            )
        else:
            search_key, search_value = next(iter(kwargs.items()))
            self.cursor.execute(
            f'SELECT * FROM {self.cls_name} \
            WHERE {search_key} = %s',
            (search_value,)
        )
        return self.cursor.fetchall()


    @catch_error
    def row(self, **kwargs) -> dict | None:
        search_key, search_value = next(iter(kwargs.items()))
        self.cursor.execute(
            f'SELECT * FROM {self.cls_name} \
            WHERE {search_key} = %s',
            (search_value,)
        )
        return self.cursor.fetchone()


    @catch_error
    def update(self, set_data: dict, **kwargs) -> None:
        search_key, search_value = next(iter(kwargs.items()))
        set_data_str = ', '.join([f"{k}=%s" for k in set_data])

        self.cursor.execute(
            f'UPDATE {self.cls_name} \
            SET {set_data_str} \
            WHERE {search_key} = %s',
            (*set_data.values(), search_value)
        )
        self.conn.commit()


    @catch_error
    def delete(self, **kwargs) -> None:
        search_key, search_value = next(iter(kwargs.items()))
        self.cursor.execute(
            f'DELETE FROM {self.cls_name} \
            WHERE {search_key} = %s',
            (search_value,)
        )
        self.conn.commit()
