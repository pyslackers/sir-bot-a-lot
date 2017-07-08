sirbot:
  port: ${port}
  plugins:
% for plugin in plugins:
    - ${plugin}
% endfor

${name}:
    priority: 1

logging:
  version: 1
  disable_existing_loggers: false
  formatters:
    simple:
      format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  handlers:
    console:
      class: logging.StreamHandler
      level: DEBUG
      formatter: simple
      stream: ext://sys.stdout
  root:
    level: ${log_level}
    handlers: [console]
    propagate: no
