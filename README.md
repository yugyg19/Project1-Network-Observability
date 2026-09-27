# Project 1: Network Deployment, Measurement, and Observability

## Overview

This project evaluates network deployment, verification, traffic observation, performance measurement, controlled degradation, and failure diagnosis.

Two scenarios were implemented.

## Scenario A - Hybrid Network

Architecture:

UE -> Access Network -> Core/Gateway -> Data Network -> Nginx

Scenario A uses Linux network namespaces, veth interfaces, Docker networking, and an Nginx application server.

Main measurements:

- Baseline ICMP RTT: 0.630 ms
- ICMP RTT with +50 ms delay: 50.433 ms
- Configured packet loss: 1%
- Measured packet loss: 2%
- Baseline TCP throughput: 29.2 Gbit/s
- 20 Mbps rate-limited TCP throughput: 19.1 Mbit/s
- Baseline UDP throughput: 10.0 Mbit/s
- UDP jitter: 0.134 ms
- UDP packet loss: 0%
- HTTP response time: 9.616 ms

Scenario A evidence is available in scenario-a/screenshots/.

## Scenario B - 5G Standalone

Architecture:

UE -> gNB -> N3/GTP-U -> UPF -> N6 -> Data Network

Control/session path:

gNB -> N2/NGAP/SCTP -> AMF -> SMF -> N4/PFCP -> UPF

Main components:

- Open5GS
- UERANSIM
- MongoDB
- Nginx
- iperf3
- Docker

The N6 Data Network uses 10.20.6.0/24.

Nginx: 10.20.6.20
iperf3: 10.20.6.21:5201

Three N6 TCP baseline measurements produced an average throughput of 25.13 Gbit/s.

A controlled 20 Mbps rate limitation produced 19.1 Mbit/s receiver throughput.

The Scenario B UE registration/PDU-session procedure did not complete successfully. Therefore, the iperf3 results are reported as N6/Data Network measurements rather than complete UE-to-application 5G user-plane throughput.

## Failure Diagnosis

UE registration reached RRC connection and CM-CONNECTED states, but NAS timer expiry occurred and the UE returned to MM-DEREGISTERED.

AMF logs also showed SBI connectivity problems during diagnosis.

Failure logs are stored in scenario-b/logs/.

## Measurements and Analysis

Scenario B dataset:

scenario-b/measurements/performance_results.csv

Python analysis:

scenario-b/analysis/performance_analysis.py

Generated graph:

scenario-b/analysis/throughput_comparison.png

## Packet Captures

Scenario A packet captures are stored in scenario-a/packet-captures/, including ICMP, HTTP, and UDP captures.

Scenario B captures are stored in scenario-b/packet-captures/.

Scenario B includes N2/NGAP, N3/GTP-U, N4/PFCP, and N6 capture files.

## Evidence

Scenario A screenshots:

scenario-a/screenshots/

Scenario B screenshots:

scenario-b/screenshots/

## Technical Report

The complete technical report is available at:

report/technical_report.md

## Limitations

Scenario B UE registration and PDU session establishment were not completed. Complete UE-originated N3/GTP-U traffic was therefore not demonstrated.

Prometheus/Grafana monitoring was not active for the final quantitative measurements.

The detailed limitations and experimental discussion are documented in the technical report.
