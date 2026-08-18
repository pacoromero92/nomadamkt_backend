from services.bronze_service import fetch_to_bronze
from services.silver_service import process_to_silver
from services.gold_service import fetch_gold
from services.adcampaings_service import fetch_campaings
from repositories.pipeline_repository import start_pipeline,finish_pipeline,process_job
from datetime import datetime
import uuid
class PipelineService:

    def start_log(self,execution_id):
        start_pipeline(execution_id=execution_id)

    def finish_log(self,execution_id):
        finish_pipeline(execution_id)

    def finisht_error(self,execution_id,error_message):
        finish_pipeline(execution_id=execution_id,error_massage=error_message)

    def start_procees(self,execution_id,process,layer):
        process_job(execution_id=execution_id,process=process,layer=layer,status="Start Process")

    def finish_procees(self,execution_id,process,layer,read_account=0,finish_at=None,duration =0):
        process_job(execution_id=execution_id,
                    process=process,
                    layer=layer,
                    status="Complete",
                    read_records=read_account,
                    durations=duration,
                    finish_at=finish_at
                    )
    def run(self):
        try:
            
            execution_id = uuid.uuid4()
            self.start_log(execution_id)
            start_time = datetime.now()
            self.start_procees(execution_id,'campaings','bronze')
            records =fetch_campaings()
            date = datetime.now()
            duration = date-start_time
            self.finish_procees(execution_id,'campaings','bronze',read_account=records,duration=duration.total_seconds()*1000,finish_at=date)

            start_time = datetime.now()
            self.start_procees(execution_id,'bronze_insights','bronze')
            records = fetch_to_bronze()
            date = datetime.now()
            duration = date-start_time
            self.finish_procees(execution_id,'bronze_insights','bronze',read_account=records,duration=duration.total_seconds()*1000,finish_at=date)

            start_time = datetime.now()
            self.start_procees(execution_id,'silver_insights','silver')
            records = process_to_silver()
            date = datetime.now()
            duration = date-start_time
            self.finish_procees(execution_id,'silver_insights','silver',read_account=records,duration=duration.total_seconds()*1000,finish_at=date)

            start_time = datetime.now()
            self.start_procees(execution_id,'gold_insights','gold')
            records = fetch_gold()
            date = datetime.now()
            duration = date-start_time
            self.finish_procees(execution_id,'gold_insights','gold',read_account=records,duration=duration.total_seconds()*1000,finish_at=date)


            self.finish_log(execution_id)
        except Exception as e:
            self.finisht_error(execution_id,str(e))

        
if __name__ == "__main__":
    pipeline = PipelineService()
    pipeline.run()
