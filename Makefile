all: help

help: ## Show this help
	
serve: ## Development server
	FLASK_DEBUG=1 python app.py
