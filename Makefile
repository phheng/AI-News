.PHONY: gateway-run redis-init db-migrations-list

gateway-run:
	@echo "crypto-intel: gateway run"
	cd apps/api-gateway && uvicorn src.main:app --host 0.0.0.0 --port 18080

redis-init:
	@echo "crypto-intel: redis init-streams"
	python3 scripts/redis/init_streams.py

db-migrations-list:
	@echo "crypto-intel: db migrations list"
	ls -1 scripts/db/migrations
