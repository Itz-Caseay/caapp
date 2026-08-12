import multiprocessing

# Bind to the port Render provides
bind = "0.0.0.0:8000"

# Number of workers
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class
worker_class = "sync"

# Timeout
timeout = 120

# Log level
loglevel = "info"

# Access log
accesslog = "-"
errorlog = "-"