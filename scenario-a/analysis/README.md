# Scenario A — Quantitative Analysis

## Main observations

- Adding the recorded +50 ms delay changed average ICMP RTT from **0.630 ms** to **50.433 ms**.
- The 1% configured packet-loss condition produced **2% measured loss** in the recorded test.
- The 20 Mbps rate limit reduced TCP receiver throughput from **29.2 Gbit/s** baseline to **19.1 Mbit/s**.
- UDP was offered at **10.0 Mbit/s** and received at **10.0 Mbit/s**, with **0.134 ms jitter** and **0% loss**.
- Baseline HTTP response time was **9.616 ms**.

## Interpretation

The delay experiment demonstrates that an added network delay appears directly in measured RTT.
The rate-limitation experiment demonstrates that the transport throughput becomes constrained by the
configured bottleneck. The UDP result shows that, under the recorded baseline condition, the offered
10 Mbps stream was received without measured packet loss.

The packet-loss result is reported as measured rather than assumed: the configured condition was 1%,
while the recorded measurement was 2%.

## Important presentation rule

Do not treat the graphs as independent measurements. Each graph is a visualization of the recorded
values in `scenario-a/measurements/scenario_a_summary.csv`.
