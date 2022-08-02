import { EvaluationResults, MergedData, PingEvaluation } from "./def";

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

export function download(data: any, title: string) {
	const dataString = JSON.stringify(data);
	const aElem = document.createElement("a");
	const file = new Blob([dataString], { type: "text/json" });
	aElem.href = URL.createObjectURL(file);
	aElem.download = title;
	aElem.click();
}

/** Calculates EvaluationResults based on `data`. Slice input `data` to set interval. */
export function calculateEvaluation(data: MergedData[], log = true): EvaluationResults {
	// Duration
	const durationTotalMs = (data[data.length - 1].timestamp - data[0].timestamp);
	const [durationMin, durationSec, durationMs] = getDetailedTime(durationTotalMs);

	// Latency
	const invalidLatencyDataPoints = data.map(entry => entry.latency).filter(l => l === null).length;
	const invalidLatencyDataPointsPercent = Math.round((invalidLatencyDataPoints / data.length) * 100);
	const latencyArr = data.map(entry => entry.latency).filter(l => l !== null);
	const avgLatency = avg(latencyArr);
	const medianLatency = median(latencyArr);

	// True / corrected latency
	const trueLatencyArr = data.map(entry => entry.trueLatency).filter(l => l !== null);
	const avgTrueLatency = avg(trueLatencyArr);
	const medianTrueLatency = median(trueLatencyArr);

	// Fps
	const fpsArr = data.map(entry => entry.fps);
	const avgFps = avg(fpsArr);
	const medianFps = median(fpsArr);

	// QR code generation
	const qrCodeGenTimeArr = data.map(d => d.qrCodeGenerationTime);
	const qrCodeGenTimeArrFiltered = qrCodeGenTimeArr.filter(t => t !== null);
	const missingQRCodeGenDataPoints = qrCodeGenTimeArr.length - qrCodeGenTimeArrFiltered.length;
	const missingQRCodeGenDataPointsPercent = Math.round((missingQRCodeGenDataPoints / data.length) * 100);
	const avgQrCodeGenTime = avg(qrCodeGenTimeArrFiltered);
	const medianQrCodeGenTime = median(qrCodeGenTimeArrFiltered);

	// Latency method / QR code parsing method
	const latencyMethodArr = data.map(entry => entry.latencyMethodRuntime);
	const avgLatencyMethod = avg(latencyMethodArr);
	const medianLatencyMethod = median(latencyMethodArr);

	// Ping data
	const hasPingData = data.find(e => !!e.ping) !== undefined;
	let ping: PingEvaluation | undefined;
	if (hasPingData) {
		const pingData = data.map(entry => entry.ping);
		const pingDataFiltered = pingData.filter(d => d !== undefined);

		const missingPingDataPoints = pingData.length - pingDataFiltered.length;
		const missingPingDataPointsPercent = Math.round((missingPingDataPoints / data.length) * 100);

		const rtt = pingDataFiltered.map(d => d.rtt);
		const avgPingRtt = avg(rtt);
		const medianPingRtt = median(rtt);

		const timeToServer = pingDataFiltered.map(d => d.timeToServer);
		const avgPingTimeToServer = avg(timeToServer);
		const medianPingTimeToServer = median(timeToServer);

		const timeBack = pingDataFiltered.map(d => d.timeBack);
		const avgPingTimeBack = avg(timeBack);
		const medianPingTimeBack = median(timeBack);

		ping = {
			missingPingDataPoints,
			missingPingDataPointsPercent,
			avgPingRtt,
			medianPingRtt,
			avgPingTimeToServer,
			medianPingTimeToServer,
			avgPingTimeBack,
			medianPingTimeBack
		};
	}

	if (log) {
		console.group("Evaluation");
		console.log(`Data Points: ${data.length}`);
		console.log(`Duration: ${durationMin}m, ${durationSec}s, ${durationMs}ms`);
		console.log(`Invalid Latency Data Points: ${invalidLatencyDataPoints} (${invalidLatencyDataPointsPercent}%)`);
		console.log("Average Latency:", avgLatency, "ms");
		console.log("Median Latency:", medianLatency, "ms");
		console.log("Average FPS:", avgFps);
		console.log("Median FPS:", medianFps);

		console.group("QR Code Generation Time - Does affect latency");
		console.log(`Missing QR Code Generation Data Points: ${missingQRCodeGenDataPoints} (${missingQRCodeGenDataPointsPercent}%)`);
		console.log("Average QR Code Generation time:", avgQrCodeGenTime, "ms");
		console.log("Median QR Code Generation time:", medianQrCodeGenTime, "ms");
		console.groupEnd();

		console.group("QR Code Parsing Time - Does not directly affect latency");
		console.log("Average Latency Method Runtime:", avgLatencyMethod, "ms");
		console.log("Median Latency Method Runtime:", medianLatencyMethod, "ms");
		console.groupEnd();

		if (hasPingData) {
			console.group("Ping API");
			console.log(`Missing Ping Data Points: ${ping.missingPingDataPoints} (${ping.missingPingDataPointsPercent}%)`);
			console.log("Average RTT:", ping.avgPingRtt, "ms");
			console.log("Median RTT:", ping.medianPingRtt, "ms");
			console.log("Average Time To Server:", ping.avgPingTimeToServer, "ms");
			console.log("Median Time To Server:", ping.medianPingTimeToServer, "ms");
			console.log("Average Time Back:", ping.avgPingTimeBack, "ms");
			console.log("Median Time Back:", ping.medianPingTimeBack, "ms");
			console.groupEnd();
		} else {
			console.group("No ping data found");
			console.groupEnd();
		}

		console.groupEnd();
	}

	return {
		dataPoints: data.length,
		durationTotalMs,
		durationSec,
		durationMin,
		durationMs,
		invalidLatencyDataPoints,
		invalidLatencyDataPointsPercent,
		avgLatency,
		medianLatency,
		avgTrueLatency,
		medianTrueLatency,
		missingQRCodeGenDataPoints,
		missingQRCodeGenDataPointsPercent,
		avgQrCodeGenTime,
		medianQrCodeGenTime,
		avgLatencyMethod,
		medianLatencyMethod,
		avgFps,
		medianFps,
		ping
	};
}
