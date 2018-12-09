FROM sirisurab/dq-base3 AS app
USER root
RUN python -m spacy download en_core_web_lg && \
rm -Rf /app && \
mkdir /app && \
chmod -R 777 /app && \
git clone -v "git://github.com/sirisurab/dupquest.git" /app
# Set the working directory to /app
WORKDIR /app
RUN chmod -R 777 /app
ENV PYTHONPATH="/app/src:${PYTHONPATH}"