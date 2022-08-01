/** Calculate average */
export function avg(arr: number[]) {
	const filtered = arr.filter(e => e !== undefined);
	if (arr.length !== filtered.length) {
		console.warn("Ignoring", arr.length - filtered.length, "undefined values in input for avg()");
	}
	return filtered.reduce((a, b) => a + b, 0) / filtered.length;
}

/** Calculate median */
export function median(arr: number[]) {
	const filtered = arr.filter(e => e !== undefined);
	if (arr.length !== filtered.length) {
		console.warn("Ignoring", arr.length - filtered.length, "undefined values in input for median()");
	}

	const sorted = filtered.sort((a, b) => a - b);
	const half = Math.floor(filtered.length / 2);
	if (filtered.length % 2) {
		return sorted[half];
	}
	return (sorted[half - 1] + sorted[half]) / 2;
}

export function getDetailedTime(ms: number) {
	const sec = Math.floor((ms / 1000) % 60);
	const min = Math.floor((ms / 1000) / 60);
	const remainingMs = ms % 1000;
	return [min, sec, remainingMs];
}
