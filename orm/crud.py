from sqlalchemy import MetaData, Table
from sqlalchemy.engine import Engine
from itertools import chain

from sqlalchemy.dialects.postgresql import Insert as PGInsert


def _prepare_data(data: list[dict], table: Table):
    columns = table.c.keys()
    keys = set(chain.from_iterable(data))

    valid_keys = [x for x in keys if x in columns]

    for d in data:
        d.update({key: None for key in keys if key not in d})

        for key in list(d.keys()):
            if key not in valid_keys:
                del d[key]

    return data


def upsert(
    data: list[dict], table_name: str, schema: str, engine: Engine
):
    if not data:
        return

    metadata = MetaData(bind=engine, schema=schema)
    metadata.reflect()

    table = Table(table_name, metadata)

    data = _prepare_data(data, table)

    with engine.connect() as connection:
        insert_stmt = PGInsert(table).values(data)
        update_dict = {
            c.name: c for c in insert_stmt.excluded if not c.primary_key}
        stmt = insert_stmt.on_conflict_do_update(
            constraint=table.primary_key, set_=update_dict
        )
        connection.execute(stmt)
