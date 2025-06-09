# kafka-init/Dockerfile
FROM confluentinc/cp-kafka:7.5.1

# Create a directory for logs with proper permissions
RUN mkdir -p /tmp/kafka-logs && \
    chmod -R 777 /tmp/kafka-logs

# Set log directory environment variable
ENV LOG_DIR=/tmp/kafka-logs

COPY init-kafka.sh /init-kafka.sh
CMD [sh /init-kafka.sh]