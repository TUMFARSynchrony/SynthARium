export interface TestConfigObj {
	participantId: string;
	sessionId: string;
	fps: number;
	background: boolean;
	width: number;
	height: number;
	qrCodeSize: number;
	printTime: boolean;
	outlineQrCode: boolean;
	connectionLogging: boolean;
	ping: boolean;
	pingData: string;
}

export interface PingData {
	sent: number,
	received: number,
	serverTime: number,
}

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
	ping?: {
		rtt: number;
		timeToServer: number;
		timeBack: number;
	};
}

export interface PingEvaluation {
	missingPingDataPoints: number;
	missingPingDataPointsPercent: number;
	avgPingRtt: number;
	medianPingRtt: number;
	avgPingTimeToServer: number;
	medianPingTimeToServer: number;
	avgPingTimeBack: number;
	medianPingTimeBack: number;
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
	ping?: PingEvaluation;
}

declare global {
	interface Window {
		MediaStreamTrackProcessor: any;
	}
}

