load:
	python src/etl/loader.py

test:
	pytest tests/

ratios:
	python src/analytics/ratio_engine.py

report:
	python src/reporting/report_generator.py

dashboard:
	streamlit run src/dashboard/app.py

api:
	python src/api/main.py

clean:
	del /Q output\*.csv