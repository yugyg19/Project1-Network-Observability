# Project 1: Network Deployment, Measurement, and Observability

## 1. Introduction

This project evaluates network deployment, verification, traffic observation, performance measurement, controlled degradation, and failure diagnosis in two scenarios.

Scenario A implements a hybrid network using Linux network namespaces and a Docker-based application server.

Scenario B models a 5G Standalone (SA) environment using Open5GS and UERANSIM, with an N6 data network containing Nginx and an iperf3 performance server.

The experimental workflow follows the project methodology:

**Deploy → Verify → Observe → Measure → Diagnose → Explain**

---

# 2. Scenario A — Hybrid Network

## 2.1 Architecture

Scenario A consists of:

**UE/Client → Access Network → Core/Gateway → Data Network → Application Server**

Linux namespaces were used for the UE, Access, and Core functions. Virtual Ethernet (veth) pairs provided connectivity between namespaces, while a Docker bridge provided access to the application/data network.

### IP Addressing

| Segment | Device | Address |
|---|---|---|
| UE–Access | UE | 10.10.1.2/24 |
| UE–Access | Access | 10.10.1.1/24 |
| Access–Core | Access | 10.10.2.1/24 |
| Access–Core | Core | 10.10.2.2/24 |
| Core–Data | Core | 10.10.3.1/24 |
| Core–Data | Docker gateway | 10.10.3.2/24 |
| Application | Nginx | 10.10.3.10/24 |

The application server was deployed using Nginx.

## 2.2 Deployment and Verification

The Scenario A network namespaces, virtual Ethernet interfaces, IP addressing, routing, Docker network, and Nginx application server were deployed.

End-to-end communication from the UE through the Access and Core network toward the Nginx application server was successfully verified.

ICMP connectivity and HTTP communication were tested.

## 2.3 Traffic Observation

Packet captures were collected for:

- ICMP
- HTTP
- UDP

The captures provide evidence of endpoints, protocols, ports, and packet behavior.

Important files include:

- `scenario-a/packet-captures/icmp.pcap`
- `scenario-a/packet-captures/http.pcap`
- `scenario-a/packet-captures/udp.pcap`

## 2.4 Baseline and Degraded Measurements

| Measurement | Result |
|---|---:|
| Baseline ICMP average RTT | 0.630 ms |
| ICMP RTT with +50 ms delay | 50.433 ms |
| Configured packet loss | 1% |
| Measured packet loss | 2% |
| Baseline TCP throughput | 29.2 Gbit/s |
| TCP throughput with 20 Mbps limit | 19.1 Mbit/s |
| Baseline UDP throughput | 10.0 Mbit/s |
| UDP jitter | 0.134 ms |
| UDP packet loss | 0% |
| HTTP response time | 9.616 ms |

The measurements demonstrate the effects of controlled delay, loss, and rate impairments.

Increasing delay increased the measured RTT. Packet-loss impairment resulted in measurable packet loss. The TCP rate limitation reduced throughput to approximately the configured target.

---

# 3. Scenario B — 5G Standalone Network

## 3.1 Architecture

Scenario B follows the 5G SA architecture:

**UE → gNB → N3/GTP-U → UPF → N6 → Data Network → Application/Performance Service**

The control and session path is:

**gNB → N2/NGAP/SCTP → AMF → SMF → N4/PFCP → UPF**

### Interface Mapping

| Interface | Connection | Protocol |
|---|---|---|
| UE–gNB | Simulated radio | UERANSIM |
| N2 | gNB–AMF | SCTP/NGAP |
| N3 | gNB–UPF | UDP/GTP-U |
| N4 | SMF–UPF | UDP/PFCP |
| N6 | UPF–Data Network | IP |

## 3.2 Environment

The Scenario B environment was implemented using Docker, Open5GS, UERANSIM, and MongoDB.

The Open5GS core included the main network functions such as AMF, SMF, UPF, NRF, SCP, AUSF, UDR, UDM, PCF, NSSF, BSF, and MongoDB.

UERANSIM provided the simulated gNB and UE.

## 3.3 Open5GS and gNB Deployment

The Open5GS core services were deployed and started.

The UERANSIM gNB was deployed and established an SCTP connection to the AMF.

The gNB logs provided evidence of:

- SCTP connection establishment
- NG Setup Request
- NG Setup Response
- Successful NG Setup procedure

This provides evidence for the N2 control-plane connection.

## 3.4 UE Registration and Failure Diagnosis

The UE detected the configured cell and established an RRC connection.

The UE reached the CM-CONNECTED state and sent an Initial Registration request.

However, registration did not complete. NAS timer expiry occurred and the UE returned to the MM-DEREGISTERED state.

During diagnosis, AMF logs showed SBI connectivity problems involving an endpoint at `172.22.0.35:7777`, including `No route to host` and connection failures.

The relevant core-network services were subsequently restored, and AMF logs showed successful NF registration and an SBI endpoint at `172.22.0.12:7777`.

The UE registration/PDU-session problem nevertheless remained unresolved during the final measurement stage.

Therefore, the N6 performance measurements are not presented as complete UE-to-application 5G user-plane measurements.

## 3.5 Packet Observation

Packet capture points were prepared for the required 5G interfaces.

### N2 — NGAP/SCTP

An N2 capture was configured for SCTP port 38412.

The capture file was created, although no packets were collected during the final capture window.

The earlier gNB log evidence provides the primary N2 verification.

### N3 — GTP-U

An N3 capture was configured for UDP port 2152.

The capture file was created, but no GTP-U packets were observed during the capture window.

This is consistent with the absence of a successful UE PDU session.

### N4 — PFCP

An N4 capture was configured for UDP port 8805.

No PFCP packets were observed during the final capture window.

### N6 — Data Network

An N6 capture was configured for the data-network subnet.

No UE-originated N6 traffic was observed because the UE user-plane session was not successfully established.

---

# 4. Scenario B N6 Data Network

A dedicated N6 Docker bridge network was created:

**10.20.6.0/24**

### N6 Addressing

| Component | Address |
|---|---|
| N6 gateway | 10.20.6.1 |
| UPF N6 address | 10.20.6.2 |
| Nginx | 10.20.6.20 |
| iperf3 | 10.20.6.21 |

The UPF was connected to the N6 network.

Nginx was deployed at `10.20.6.20`.

An HTTP request returned:

**HTTP/1.1 200 OK**

The iperf3 server was deployed at:

**10.20.6.21:5201**

and successful TCP connectivity was verified.

---

# 5. Scenario B Performance Measurements

## 5.1 Baseline

Three TCP iperf3 baseline measurements were performed.

| Run | Receiver Throughput | Retransmissions |
|---|---:|---:|
| Baseline 1 | 25.2 Gbit/s | 4,088 |
| Baseline 2 | 24.0 Gbit/s | 1,953 |
| Baseline 3 | 26.2 Gbit/s | 945 |

The average baseline throughput was:

**25.13 Gbit/s (25,133.33 Mbps)**

These measurements represent the N6/Data Network path between the test client and iperf3 server.

They are not claimed as complete UE-to-5G-user-plane throughput because the UE PDU session was not successfully established.

## 5.2 Controlled 20 Mbps Rate Limitation

A controlled 20 Mbps rate limitation was applied to the iperf3 server's outgoing interface and tested using reverse iperf3 mode.

| Condition | Sender | Receiver |
|---|---:|---:|
| 20 Mbps rate limit | 19.7 Mbit/s | 19.1 Mbit/s |

The measured receiver throughput of **19.1 Mbit/s** was close to the configured 20 Mbps target.

Compared with the 25,133.33 Mbps baseline average, the measured throughput reduction was approximately:

**99.92%**

---

# 6. Python Analysis

The Scenario B measurements were stored in:

`scenario-b/measurements/performance_results.csv`

Python using pandas and Matplotlib was used to calculate:

- baseline average throughput
- degraded throughput
- throughput reduction

The analysis generated:

`scenario-b/analysis/throughput_comparison.png`

The graph uses a logarithmic throughput axis so that the baseline and degraded measurements can both be visualized clearly.

---

# 7. Monitoring

Prometheus/Grafana services were not active in the final Scenario B deployment state.

Therefore, Prometheus/Grafana dashboards were not used for the final quantitative measurements.

This is documented as a project limitation.

---

# 8. Comparison and Discussion

Scenario A provided a complete namespace-based network path with successful end-to-end application connectivity. It therefore allowed direct measurement of ICMP, TCP, UDP, and HTTP behavior together with controlled impairment experiments.

Scenario B provided a more detailed 5G SA architecture. Open5GS and UERANSIM were deployed, the gNB successfully established N2 connectivity with the AMF, and an N6 Data Network was created and measured.

However, the Scenario B UE registration/PDU-session problem prevented complete UE-to-application user-plane measurements.

Therefore, the Scenario B performance results are explicitly presented as N6/Data Network measurements rather than complete 5G UE-to-application throughput.

The project demonstrates the importance of separating:

- control-plane evidence
- user-plane evidence
- application-level evidence
- performance measurements
- failure evidence

Container status alone is not sufficient to prove successful 5G user-plane operation.

---

# 9. Failure Diagnosis

The Scenario B failure can be summarized as an evidence chain:

**UE registration attempt**

↓

**RRC connection established**

↓

**CM-CONNECTED**

↓

**Initial Registration**

↓

**NAS timer expiry**

↓

**MM-DEREGISTERED**

At the core-network side, AMF logs showed SBI connectivity failures toward `172.22.0.35:7777`, including `No route to host`.

After core-network service restoration, NF registration activity was observed and the SBI endpoint changed to `172.22.0.12:7777`.

Despite these corrections, the UE registration/PDU-session procedure did not complete during the final testing stage.

The failure evidence is retained in the Scenario B log and screenshot directories.

---

# 10. Limitations

1. Scenario B UE registration and PDU session establishment were not successfully completed.
2. N3/GTP-U user-plane traffic from the UE was therefore not observed during the final capture windows.
3. N4/PFCP traffic was not observed during the final capture window.
4. Prometheus/Grafana monitoring was not active for the final Scenario B measurements.
5. Scenario B iperf3 results represent the N6/Data Network path rather than a complete UE-to-application 5G path.
6. The controlled degradation experiment was performed on the N6 iperf3 path.

These limitations are considered when interpreting the results.

---

# 11. Conclusion

The project implemented and evaluated two network scenarios.

Scenario A demonstrated a hybrid namespace/Docker network with successful end-to-end application connectivity, packet observation, baseline measurements, and controlled delay, loss, and rate impairments.

Scenario B deployed the Open5GS and UERANSIM components, established gNB-to-AMF N2 connectivity, created an N6 Data Network, deployed Nginx and iperf3 services, and performed quantitative N6 baseline and controlled-rate measurements.

The Scenario B failure investigation identified SBI connectivity problems and documented the remaining UE registration/PDU-session limitation.

The final results therefore distinguish between verified 5G control-plane deployment, verified N6 application/performance connectivity, and the parts of the complete 5G user plane that could not be demonstrated.

Overall, the project demonstrates a practical workflow for network deployment, verification, packet observation, quantitative measurement, controlled degradation, and evidence-based diagnosis.

---

# 12. Project Evidence

## Scenario A

Important Scenario A evidence includes:

- topology and namespace configuration
- interface and routing information
- Docker network and Nginx deployment
- ICMP packet capture
- HTTP packet capture
- UDP packet capture
- baseline measurements
- controlled delay, loss, and rate experiments
- Python analysis and graphs

## Scenario B

Important Scenario B evidence includes:

- Open5GS deployment screenshots
- UERANSIM gNB and UE deployment screenshots
- N2/NGAP evidence
- N3/GTP-U capture
- N4/PFCP capture
- N6 capture
- UE and AMF failure logs
- N6 network configuration
- Nginx connectivity test
- iperf3 connectivity and baseline measurements
- controlled 20 Mbps measurement
- CSV dataset
- Python analysis script
- throughput comparison graph

All implementation materials and supporting evidence should be included in the GitHub repository.

---

# 13. References and Tools

The project used the course assignment requirements as the primary methodology and used the following software/tools during implementation and analysis:

- Docker and Docker Compose
- Linux network namespaces and veth
- Open5GS
- UERANSIM
- MongoDB
- Nginx
- iperf3
- tcpdump
- Wireshark/TShark where applicable
- Python
- pandas
- Matplotlib
- Prometheus/Grafana where applicable
"""

## 13. Figures

### Figure 1 — Scenario B N6 TCP Throughput

The following figure compares the average baseline N6 TCP throughput with the controlled 20 Mbps rate-limited condition.

![Scenario B N6 TCP Throughput](../scenario-b/analysis/throughput_comparison.png)

The logarithmic scale allows both the high baseline throughput and the substantially lower degraded throughput to be visualized on the same graph.

### Figure 2 — Scenario A and Scenario B Evidence

The complete deployment, verification, packet-observation, measurement, and failure-diagnosis screenshots are provided in:

- `scenario-a/screenshots/`
- `scenario-b/screenshots/`

These folders contain the supporting evidence for the experimental procedures and results described in this report.

## 14. Scenario A Analysis Figures

### Figure 3 — Scenario A ICMP RTT

The Scenario A Python analysis compares the baseline ICMP RTT with the controlled +50 ms delay condition.

![Scenario A ICMP RTT Comparison](../scenario-a/analysis/icmp_rtt_comparison.png)

### Figure 4 — Scenario A TCP Throughput

The Scenario A analysis compares the baseline TCP throughput with the controlled 20 Mbps rate-limited condition.

![Scenario A TCP Throughput Comparison](../scenario-a/analysis/tcp_throughput_comparison.png)

The complete Scenario A supporting screenshot evidence is available in `scenario-a/screenshots/`.
