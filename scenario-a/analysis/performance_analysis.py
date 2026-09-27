import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

base = Path.home() / "Project1-Network-Observability"

df = pd.read_csv(base / "measurements" / "performance_results.csv")

print("\n=== Performance Dataset ===")
print(df.to_string(index=False))

# ICMP RTT comparison
icmp = df[df["Metric"] == "ICMP Average RTT"]

plt.figure(figsize=(8, 5))
plt.bar(icmp["Condition"], icmp["Value"])
plt.ylabel("Average RTT (ms)")
plt.xlabel("Condition")
plt.title("ICMP RTT: Baseline vs 50 ms Delay")
plt.tight_layout()
plt.savefig(base / "analysis" / "icmp_rtt_comparison.png", dpi=200)
plt.close()

# TCP throughput comparison
tcp = df[df["Metric"] == "TCP Throughput"]

plt.figure(figsize=(8, 5))
plt.bar(tcp["Condition"], tcp["Value"])
plt.yscale("log")
plt.ylabel("TCP Throughput (Mbit/s, logarithmic scale)")
plt.xlabel("Condition")
plt.title("TCP Throughput: Baseline vs 20 Mbps Rate Limit")
plt.tight_layout()
plt.savefig(base / "analysis" / "tcp_throughput_comparison.png", dpi=200)
plt.close()

print("\nGraphs created successfully.")
