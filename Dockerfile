FROM alpine:3.16
RUN apk add python3 git patch bash
WORKDIR /app
COPY . .
RUN ./scripts/install.sh
CMD ./narwhalizer.sh

RUN addgroup app
RUN adduser -D -G app -h /app app
RUN chown -R app:app /app
USER app
