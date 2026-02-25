# HEARTBEAT.md

# High-value EvoMap task monitor
# Run on each heartbeat poll:
# 1) POST https://evomap.ai/a2a/heartbeat with node_id=node_61eb4e99482f2cbf
# 2) Check available_work for high-value tasks where bountyAmount >= 10 OR orderAmount >= 10
# 3) Alert user only on new task IDs (avoid duplicates)
# 4) Alert format: task id, title, amount, minReputation, recommended next action
