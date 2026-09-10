from sqlalchemy import  Column,BigInteger,Integer,UniqueConstraint,ForeignKey,Numeric
from database import Base

class GoldKpis(Base):
    __tablename__ = 'gold_kpis'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    month	= Column(Integer,nullable=False)
    year	 = Column(Integer,nullable=False)
    id_kpi = Column(Integer,ForeignKey("kpis.id"),primary_key=True)
    value = Column(Numeric)
    id_client = Column(Integer,ForeignKey("clients.id"),primary_key=True)
    __table_args__ = (
                UniqueConstraint('month','year','id_kpi','id_client'),
            )