import { Layer, Stage } from "react-konva";
import Video from "../atoms/Video/Video";
import { useState, useEffect } from "react";
import { CANVAS_SIZE } from "../../utils/constants";

function ParticipantVideo({ localStream }) {
    let participantData = {
        size: {
            width: CANVAS_SIZE.width,
            height: CANVAS_SIZE.height
        },
        position: {
            x: 0,
            y: 0
        }
    }
    const [participantVideoData, setParticipantVideoData] = useState(participantData);
    const [participantStream, setParticipantStream] = useState(localStream);

    useEffect(() => {
        setParticipantStream(localStream);
    }, [localStream]);

    return (
        <Stage width={CANVAS_SIZE.width} height={CANVAS_SIZE.height}>
            <Layer>
                <Video
                    src={participantStream}
                    participantData={participantVideoData}
                />
            </Layer>
        </Stage>
    )
}

export default ParticipantVideo;
