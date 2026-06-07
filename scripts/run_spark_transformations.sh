#!/usr/bin/env bash
set -e

if [ -d "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home" ]; then
  JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
elif [ -d "/usr/local/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home" ]; then
  JAVA_HOME="/usr/local/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
else
  JAVA_HOME=$(/usr/libexec/java_home -v 17)
fi

export JAVA_HOME
export PATH="$JAVA_HOME/bin:$PATH"
export SPARK_LOCAL_IP=127.0.0.1

echo "Using Java:"
java -version

echo "Running Spark lakehouse transformations..."

python -m spark.jobs.run_spark_lakehouse

echo "Spark lakehouse transformations completed."