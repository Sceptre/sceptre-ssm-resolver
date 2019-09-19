FROM alpine:3.7

RUN addgroup -g 3434 circleci
RUN adduser -D -u 3434 -G circleci -s /bin/bash circleci
WORKDIR /home/circleci
ENV LANG=C.UTF-8 \
    HOME=/home/circleci

RUN apk add --no-cache \
    bash \
    ca-certificates \
    curl \
    g++ \
    git \
    libffi-dev \
    make \
    openjdk8-jre \
    openssh \
    openssl-dev \
    python3 \
    python3-dev

RUN pip3 install --upgrade pip setuptools && pip3 install virtualenv

ENV JAVA_HOME /usr/lib/jvm/java-1.8-openjdk
ENV PATH $PATH:/usr/lib/jvm/java-1.8-openjdk/jre/bin:/usr/lib/jvm/java-1.8-openjdk/bin

RUN curl https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-3.3.0.1492-linux.zip --output sonar.zip && \
unzip ./sonar.zip && \
rm ./sonar.zip && rm sonar-scanner-3.3.0.1492-linux/jre -rf && \
sed -i 's/use_embedded_jre=true/use_embedded_jre=false/g' /home/circleci/sonar-scanner-3.3.0.1492-linux/bin/sonar-scanner

ENV SONAR_RUNNER_HOME=/home/circleci/sonar-scanner-3.3.0.1492-linux
ENV PATH="/home/circleci/sonar-scanner-3.3.0.1492-linux/bin/:${PATH}"

USER circleci

CMD ["/bin/sh"]
