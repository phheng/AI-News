.PHONY: gateway-run redis-init redis-notify-worker db-migrations-list db-migrate db-rollback

gateway-run:
	@echo "crypto-intel: gateway run"
	cd apps/api-gateway && uvicorn src.main:app --host 0.0.0.0 --port 18080

redis-init:
	@echo "crypto-intel: redis init-streams"
	bash scripts/redis/init_streams.sh

redis-notify-worker:
	@echo "crypto-intel: redis notification worker"
	python3 scripts/redis/worker_notification.py

db-migrations-list:
	@echo "crypto-intel: db migrations list"
	ls -1 scripts/db/migrations

db-migrate:
	@echo "crypto-intel: db migrate"
	bash scripts/db/migrate.sh

db-rollback:
	@echo "crypto-intel: db rollback"
	bash scripts/db/rollback.sh
