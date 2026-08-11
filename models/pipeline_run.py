from sqlalchemy import  Column,  String, DateTime, UniqueConstraint,ForeignKey,BigInteger,UUID,TIMESTAMP,Text
from datetime import datetime

from database import Base
class PipelineRun(Base):
    __tablename__ = 'pipeline_run'
    id = Column(BigInteger, primary_key=True)  
    excecution_id = Column(UUID)
    started_at  = Column(TIMESTAMP)
    finished_at   = Column(TIMESTAMP,nullable=True)
    status  = Column(String)
    error_message  = Column(Text,nullable=True)
    cretated_at = Column(DateTime, default=datetime.now)
    __table_args__ = (
                UniqueConstraint('excecution_id'),
            )
