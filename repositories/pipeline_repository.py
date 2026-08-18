from models.process_log import ProcessLog
from models.pipeline_run import PipelineRun
from datetime import datetime
from database import SessionLocal
from sqlalchemy.dialects.postgresql import insert
def start_pipeline(execution_id):
    start_time = datetime.now()
    fetch_pipeline(execution_id,status='START',start_time=start_time)

def finish_pipeline(execution_id,error_massage = None):
    finish_time = datetime.now()
    if error_massage is not None:
        status = "ERROR"
    else:
        status = "COMPLETED"
    fetch_pipeline(execution_id,status=status,finish_time=finish_time,error_massage=error_massage)

def process_job(execution_id,process,layer,status=None,read_records=0,finish_at=None,durations=0):
    id_pipeline = fetch_pipeline(execution_id,"PROCESSING")
    fetch_process_job(id_pipeline,process,layer=layer,status=status,records_read=read_records,duration_ms=durations,finish_at=finish_at)


def fetch_process_job(pipeline_run_id,process_name,layer,status,duration_ms=0,records_read=0,error_message=None,error_type=None,finish_at =None):
    data= {
            "pipeline_run_id"  :pipeline_run_id,
            "process_name"    : process_name,
            "layer"               :   layer,
            "status"              :  status,
            "finished_at"        : finish_at,
            "duration_ms"         :duration_ms,
            "records_read"        :records_read
    } 
    
    with SessionLocal() as session:
        smtp = insert(ProcessLog).values(data)
        update_cols = {
                        c.name: smtp.excluded[c.name] 
                        for c in ProcessLog.__table__.columns
                        
                    }
        smtp = smtp.on_conflict_do_update(
            index_elements=['pipeline_run_id','process_name'],
              set_=update_cols
        )
        session.execute(smtp)
        session.commit()

def fetch_pipeline(execution_id,status,start_time=None,finish_time=None,error_massage = None):
    data = {
        "excecution_id":execution_id,
        "status":status,
        "error_message":error_massage,

       
    }
  
    if finish_time is not None:
        data['finished_at']=finish_time
    print(data)
    with SessionLocal() as session:
        stmt = insert(PipelineRun).values(data)
        stmt = stmt.on_conflict_do_update(
                    index_elements=['excecution_id'],
                    set_={
                        'status': stmt.excluded.status,
                        'error_message':stmt.excluded.error_message,
                        'finished_at':stmt.excluded.finished_at
                    }
                ).returning(PipelineRun.id)
        result = session.execute(stmt)
        pipeline_id = result.scalar_one()
        session.commit()
        return pipeline_id