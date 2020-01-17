ARG GO_VERSION
FROM golang:latest as builder

WORKDIR /go/src/github.com/optimizely/sidedoor
COPY . .
RUN make ci_build_static_binary

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /go/src/github.com/optimizely/sidedoor/bin/optimizely /optimizely
EXPOSE 3000
CMD ["/optimizely"]
