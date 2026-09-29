# Professor Requirements — Final Evidence Matrix

| Requirement | Evidence in repository |
|---|---|
| Deployment/topology | Existing scenario A/B deployment files and report |
| IP/interface/routing documentation | Existing scenario A/B deployment documentation |
| ICMP observation | Scenario A/B measurements + packet captures |
| TCP observation | iperf3 results + packet evidence |
| UDP observation | iperf3 results + packet evidence |
| HTTP/application observation | Nginx tests + response metrics |
| Structured dataset | `scenario-a/measurements/`, `scenario-b/measurements/` |
| Configured values | `SCENARIO_A_MEASUREMENT_PARAMETERS.md`, `SCENARIO_B_MEASUREMENT_PARAMETERS.md` |
| Repeated Scenario B baseline | 3 repetitions for ICMP/TCP/UDP/HTTP |
| Controlled Scenario A conditions | +50 ms, 1% loss, 20 Mbps |
| Controlled Scenario B condition | 20 Mbps N6 rate limit |
| Comparative graphs/bar charts | `scenario-a/analysis/`, `scenario-b/analysis/` |
| Packet-level N3 evidence | `scenario-b/packet-captures/n3-gtpu.pcap` + evidence markdown |
| Python/Matplotlib analysis | Analysis figures and source datasets |
| Failure diagnosis | Initial UE registration and connectivity troubleshooting documented in the final technical report |
| Additional suggested Scenario B experiments | Not claimed unless actually measured: +50 ms delay, 1% loss, N3-vs-N6 comparison, Prometheus/Grafana correlation |
