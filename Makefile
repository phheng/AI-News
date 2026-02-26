.PHONY: gateway-run redis-init redis-notify-worker redis-paper-bridge db-migrations-list db-migrate db-rollback e2e-smoke rate-limit-stress e2e-up e2e-report infra-nginx-up infra-nginx-down cloudflared-up cloudflared-down news-collector-up news-collector-down

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

e2e-up:
	@echo "crypto-intel: e2e bootstrap"
	bash scripts/devops/e2e_bootstrap.sh

e2e-report:
	@echo "crypto-intel: e2e report"
	python3 scripts/devops/e2e_report.py

infra-nginx-up:
	@echo "crypto-intel: infra nginx up"
	bash scripts/devops/start_infra_nginx.sh

infra-nginx-down:
	@echo "crypto-intel: infra nginx down"
	bash scripts/devops/stop_infra_nginx.sh

cloudflared-up:
	@echo "crypto-intel: cloudflared up"
	bash scripts/devops/start_cloudflared.sh

cloudflared-down:
	@echo "crypto-intel: cloudflared down"
	bash scripts/devops/stop_cloudflared.sh

news-collector-up:
	@echo "crypto-intel: news collector up"
	bash scripts/devops/start_news_collector.sh

news-collector-down:
	@echo "crypto-intel: news collector down"
	bash scripts/devops/stop_news_collector.sh
