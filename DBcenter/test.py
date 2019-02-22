# coding=utf-8
from clickhouse_sqlalchemy import make_session, get_declarative_base, types, engines, Table
from sqlalchemy import create_engine, MetaData, Column, literal

uri = 'clickhouse://default:@localhost/test'

engine = create_engine(uri)
session = make_session(engine)
metadata = MetaData(bind=engine)
Base = get_declarative_base(metadata=metadata)

class Rate(Base):
    day = Column(types.Date, primary_key=True)
    value = Column(types.Int32)

    __table_args__ = (
        engines.Memory(),
    )

another_table = Table('another_rate', metadata,
    Column('day', types.Date, primary_key=True),
    Column('value', types.Int32, server_default=literal(1)),
    engines.Memory()
)