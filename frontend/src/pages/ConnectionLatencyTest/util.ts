/** Calculate average */
export function avg(arr: number[]) {
	return arr.reduce((a, b) => a + b, 0) / arr.length;
}

/** Calculate median */
export function median(arr: number[]) {
	const sorted = arr.sort((a, b) => a - b);
	const half = Math.floor(arr.length / 2);
	if (arr.length % 2) {
		return sorted[half];
	}
	return (sorted[half - 1] + sorted[half]) / 2;
}
