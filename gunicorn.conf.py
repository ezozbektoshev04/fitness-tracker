# Binding
bind = "0.0.0.0:8000"

# Workers
workers = 3
worker_class = "sync"
worker_connections = 1000

# Timeout
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "fitness_tracker"

# Reload (set False in production)
reload = False
