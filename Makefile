.PHONY: gateway-run redis-init redis-notify-worker redis-paper-bridge db-migrations-list db-migrate db-rollback e2e-smoke rate-limit-stress

gateway-run:
	@echo "crypto-intel: gateway run"
	cd apps/api-gateway && uvicorn src.main:app --host 0.0.0.0 --port 18080

redis-init:
	@echo "crypto-intel: redis init-streams"
	bash scripts/redis/init_streams.sh

redis-notify-worker:
	@echo "crypto-intel: redis notification worker"
	python3 scripts/redis/worker_notification.py

redis-paper-bridge:
	@echo "crypto-intel: redis paper->strategy bridge worker"
	python3 scripts/redis/worker_paper_to_strategy.py

db-migrations-list:
	@echo "crypto-intel: db migrations list"
	ls -1 scripts/db/migrations

db-migrate:
	@echo "crypto-intel: db migrate"
	bash scripts/db/migrate.sh

db-rollback:
	@echo "crypto-intel: db rollback"
	bash scripts/db/rollback.sh

e2e-smoke:
	@echo "crypto-intel: e2e smoke"
	python3 scripts/devops/e2e_smoke.py

rate-limit-stress:
	@echo "crypto-intel: rate-limit stress"
	python3 scripts/devops/rate_limit_stress.py
