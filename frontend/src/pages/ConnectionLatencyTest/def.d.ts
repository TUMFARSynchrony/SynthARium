
export interface LocalStreamData {
	timestamp: number;
	qrCodeGenerationTime: number;
}

export interface RemoteStreamData {
	latency: number;
	fps: number;
	timestamp: number;
	qrCodeTimestamp: number;
	frame: number;
	latencyMethodRuntime: number;
	dimensions: {
		width: number;
		height: number;
	};
}

export interface MergedData extends RemoteStreamData {
	qrCodeGenerationTime: number;
	trueLatency: number;
}

export interface EvaluationResults {
	dataPoints: number;
	durationTotalMs: number;
	durationSec: number;
	durationMin: number;
	durationMs: number;
	invalidLatencyDataPoints: number;
	invalidLatencyDataPointsPercent: number;
	avgLatency: number;
	medianLatency: number;
	avgTrueLatency: number;
	medianTrueLatency: number;
	missingQRCodeGenDataPoints: number;
	missingQRCodeGenDataPointsPercent: number;
	avgQrCodeGenTime: number;
	medianQrCodeGenTime: number;
	avgLatencyMethod: number;
	medianLatencyMethod: number;
	avgFps: number;
	medianFps: number;
}

declare global {
	interface Window {
		MediaStreamTrackProcessor: any;
	}
}

