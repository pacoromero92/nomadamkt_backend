from sqlalchemy import  Column,  String, DateTime, UniqueConstraint,ForeignKey,BigInteger,Integer,TIMESTAMP,Text
from datetime import datetime
from database import Base
class ProcessLog(Base):
    __tablename__ = 'process_log'
    id = Column(BigInteger, primary_key=True) 
    pipeline_run_id =Column(BigInteger,ForeignKey('pipeline_run.id'))
    account_id     = Column(String,nullable=True)
    process_name    = Column(String)
    layer               =   Column(String)
    status              =  Column(String)
    started_at         =Column(TIMESTAMP)
    finished_at        =Column(TIMESTAMP,nullable=True)
    duration_ms         =Column(BigInteger,nullable=True)
    records_read        =Column(Integer,default=0)
    records_created      =Column(Integer,default=0)
    records_updated     =Column(Integer,default=0)
    records_failed      =Column(Integer,default=0)
    error_type          =Column(String,nullable=True)
    error_message       =Column(Text,nullable=True)
    cretated_at         = Column(DateTime, default=datetime.now)
    __table_args__ = (
                    UniqueConstraint('pipeline_run_id','process_name'),
                )