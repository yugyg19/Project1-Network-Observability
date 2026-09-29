# Scenario A — Measurement Parameters and Procedure

This file documents the values/conditions used for the recorded Scenario A results. The numerical
results below are the values already collected during the project; no new values are invented here.

## Reference path

UE namespace → Access namespace → Core/Gateway namespace → Docker Data Network → Nginx application.

## Recorded test conditions

| Experiment | Configured condition | Recorded result |
|---|---|---:|
| ICMP baseline | No artificial impairment | 0.630 ms average RTT |
| ICMP delay | +50 ms delay | 50.433 ms average RTT |
| Packet loss | 1% configured loss | 2% measured loss |
| TCP baseline | No rate limit | 29.2 Gbit/s |
| TCP rate limit | 20 Mbps | 19.1 Mbit/s receiver |
| UDP baseline | 10 Mbps offered | 10.0 Mbit/s received |
| UDP baseline | 10 Mbps offered | 0.134 ms jitter, 0% loss |
| HTTP baseline | Nginx over TCP/80 | 9.616 ms response |

## Measurement layers

1. Network: RTT and packet loss.
2. Transport: TCP throughput/retransmissions and UDP throughput/jitter/loss.
3. Application: HTTP response time.

## Reproducibility note

The project also contains the original Scenario A packet captures and screenshots. Exact command output
should be read together with those original artifacts where the presentation requires command-level evidence.
