start prefect server:
	prefect server start    

run maintenance_flow:
	python flows/orchestration/maintenance.py  

deploy ingest_flow:
	prefect deployment build flows/ingestion/ingest_spac_collection.py:ingest_spac_collection -n ingest_deployment

create dev profile:
	prefect profile create dev
	prefect profile use dev
	prefect config set PREFECT_LOGGING_LEVEL=DEBUG
	prefect config set PREFECT_API_KEY=xxxxxxxxxxxxx
	# prefect cloud workspace set --workspace "default"