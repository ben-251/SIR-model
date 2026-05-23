from typing import Any, Dict, Iterable, Iterator, List
from backend import HealthStatus
import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt


def get_total_matching_health_status(state, health_status):
	return sum(1 for blob in state["blobs"] if blob["status"] == health_status)


def plot_SIR_graph(states:List[Dict[str,Any]]):
	state_totals = []
	for health_type in HealthStatus:
		totals = []
		for i, state in enumerate(states):
			total = get_total_matching_health_status(state, health_type)
			totals.append(total)	
		state_totals.append(totals)

	x = [state["id"] for state in states]
	for y, status in zip(state_totals, HealthStatus):
		raw_rgb = status.value.convert_hex_to_rgb() 
		rgb = [colour/255 for colour in [raw_rgb.red, raw_rgb.green, raw_rgb.blue]]
		plt.plot(x, y, color=rgb, label=status.name)

	plt.xlabel("Frame")
	plt.ylabel("Blob Count")
	plt.title("Epidemic Model")
	plt.legend()
	plt.savefig("output/plot")

def survival_hypothesis_test(states:List[Dict[str,Any]], survival_rate:float, significance_level):
	'''
	See whether it's plausible that the supplied data matches a given survival_rate.

	H_0: P(survive | no longer infected) = survival_rate
	H_1: P(survive | no longer infected) =/= survival_rate (two-sided)

	The actual proportion from the data is simply #surviving/(#surviving = )

	survival_rate (float): 0 to 1
	significance_level (float): such that 100(1-sig_lvl)% = P(t in C)
	'''
	total_survived = get_total_matching_health_status(states[-1], HealthStatus.RECOVERED)
	N = len(states)
	# T ~  Bin(n, survival_rate)
	# 	
	t_lower = max(k for k in range(N+1) if binom.cdf(k, N, survival_rate) <= significance_level/2)
	t_upper = min(k for k in range(N+1) if binom.sf(k-1, N, survival_rate) <= significance_level/2)

	return total_survived <= t_lower or total_survived >= t_upper


