import { ToastContainer, toast } from "react-toastify";
import { useEffect } from "react";
import Checkbox from "../../components/molecules/Checkbox/Checkbox";
import { useState } from "react";
import { ActionButton } from "../../components/atoms/Button";
import Box from "@mui/material/Box";
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import FormControlLabel from "@mui/material/FormControlLabel";
import TextField from "@mui/material/TextField";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import ListSubheader from "@mui/material/ListSubheader";
import Chip from "@mui/material/Chip";
import ListItem from "@mui/material/ListItem";
// REMOVE: Mocking filters data until filter API call is established
import filtersData from '../../filters.json'
import { getParticipantInviteLink } from "../../utils/utils";

// Loading filters data befor eth component renders, because the Select component needs value
const testData = filtersData.filters;
const defaultFilterId = "test";

// const getIndividualFilters = () => {
//   return filtersData.filters.filter(filter => filter.groupFilter !== true);
// };

// const getGroupFilters = () => {
//   return filtersData.filters.filter(filter => filter.groupFilter === true);
// };


function ParticipantDataModal({
  originalParticipant,
  sessionId,
  index,
  showParticipantInput,
  setShowParticipantInput,
  handleParticipantChange,
  onDeleteParticipant
}) {
  const [participantCopy, setParticipantCopy] = useState(originalParticipant);
  // const [individualFilters, setIndividualFilters] = useState(getIndividualFilters());
  // const [groupFilters, setGroupFilters] = useState(getGroupFilters());
  const [selectedFilter, setSelectedFilter] = useState(testData.find((filter) => filter.id == defaultFilterId));
  const [appliedFilters, setAppliedFilters] = useState([]);

  const handleChange = (objKey, objValue) => {
    const newParticipantData = { ...participantCopy };
    newParticipantData[objKey] = objValue;
    setParticipantCopy(newParticipantData);
  };

  const onCloseModalWithoutData = () => {
    setShowParticipantInput(!showParticipantInput);

    let newParticipantInputEmpty =
      participantCopy.first_name === "" && participantCopy.last_name === "";

    if (newParticipantInputEmpty) {
      onDeleteParticipant(index);
      toast.warning(
        "You did not enter any information. Participant will be deleted now."
      );
      return;
    }

    let requiredInformationMissing =
      participantCopy.first_name === "" || participantCopy.last_name === "";

    if (requiredInformationMissing) {
      onDeleteParticipant(index);
      toast.warning(
        "Required information (First Name/Last Name) missing. Participant will be deleted now."
      );
      return;
    }

    let participantOriginalEmpty =
      originalParticipant.first_name.length === 0 &&
      originalParticipant.last_name.length === 0;

    let newInputEqualsOld = participantCopy === originalParticipant;

    if (participantOriginalEmpty && !newInputEqualsOld) {
      onDeleteParticipant(index);
      toast.warning("You need to save the information first.");
      return;
    }

    if (!newInputEqualsOld) {
      toast.warning("You need to save the information first.");
      setParticipantCopy(originalParticipant);
      return;
    }
  };

  const onSaveParticipantData = () => {
    if (participantCopy.first_name === "" || participantCopy.last_name === "") {
      toast.error(
        "Failed to save participant since required fields are missing!"
      );
      return;
    }

    setShowParticipantInput(!showParticipantInput);
    handleParticipantChange(index, participantCopy);
  };

  const handleFilterSelect = (event) => {
    event.preventDefault();
    const filter = event.target.value;
    setSelectedFilter(filter);

    const newParticipantData = { ...participantCopy };
    if (["test", "edge", "rotation", "delay-v"].includes(filter.id)) {
      newParticipantData.video_filters = [...newParticipantData.video_filters, filter];
    }
    else {
      newParticipantData.audio_filters = [...newParticipantData.audio_filters, filter];
    }
    setParticipantCopy(newParticipantData);
  };

  const handleDeleteFilter = (filterDelete) => {
    console.log(filterDelete);
    const newParticipantData = { ...participantCopy };
    if (["test", "edge", "rotation", "delay-v"].includes(filterDelete.id)) {
      newParticipantData.video_filters = newParticipantData.video_filters.filter((filter) => filter.id !== filterDelete.id);
    }
    else {
      newParticipantData.audio_filters = newParticipantData.audio_filters.filter((filter) => filter.id !== filterDelete.id);
    }
    setParticipantCopy(newParticipantData);
  };

  // TO REMOVE
  useEffect(() => {
    // console.log(selectedFilter);
  }, [selectedFilter]);

  return (

    <Dialog open={showParticipantInput} onClose={() => onCloseModalWithoutData()}>
      <DialogTitle sx={{ textAlign: "center", fontWeight: "bold" }}>Participant Details</DialogTitle>
      <DialogContent>
        <Box>
          <Box sx={{ display: "flex", justifyContent: "space-between", gap: 5, my: 3 }}>
            <TextField label="First Name" value={participantCopy.first_name} size="small" fullWidth required onChange={(event) => { handleChange("first_name", event.target.value) }} />
            <TextField label="Last Name" value={participantCopy.last_name} size="small" fullWidth required onChange={(event) => { handleChange("last_name", event.target.value) }} />
          </Box>
          <Box>
            <TextField label="Invite Link" size="small" fullWidth disabled value={
              !(participantCopy.id.length === 0 || sessionId.length === 0)
                ? getParticipantInviteLink(participantCopy.id, sessionId)
                : "Save session to generate link."
            } />
          </Box>
          <Box sx={{ display: "flex", justifyContent: "space-between", gap: 4, my: 3 }}>
            <TextField label="Width" size="small" value={participantCopy.size.width} disabled />
            <TextField label="Height" size="small" value={participantCopy.size.height} disabled />
            <TextField label="x coordinate" size="small" value={participantCopy.position.x} disabled />
            <TextField label="y coordinate" size="small" value={participantCopy.position.y} disabled />
          </Box>
          <Box sx={{ display: "flex", justifyContent: "center", gap: 2, my: 3 }}>
            <FormControlLabel control={<Checkbox defaultChecked />} label="Mute Audio" checked={participantCopy.muted_audio} onChange={(event) => { handleChange("muted_audio", !participantCopy.muted_audio) }} />
            <FormControlLabel control={<Checkbox defaultChecked />} label="Mute Video" checked={participantCopy.muted_video} onChange={() => { handleChange("muted_video", !participantCopy.muted_video) }} />
          </Box>

          <Box sx={{ display: "flex", justifyContent: "space-between" }}>

            <Box>
              <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
                <InputLabel id="filters-select">Filters</InputLabel>
                {
                  <Select value={selectedFilter} defaultValue="" id="filters-select" label="Filters" onChange={handleFilterSelect}>
                    {/* <ListSubheader sx={{ fontWeight: "bold", color: "black" }}>Individual Filters</ListSubheader>
                    {
                      individualFilters.map((individualFilter) => {
                        if (individualFilter.id == defaultFilterId) {
                          return <MenuItem key={individualFilter.id} value={individualFilter}><em>{individualFilter.id}</em></MenuItem>
                        }
                        else {
                          return <MenuItem key={individualFilter.id} value={individualFilter}>{individualFilter.id}</MenuItem>
                        }
                      })
                    }
                    <ListSubheader sx={{ fontWeight: "bold", color: "black" }}>Group Filters</ListSubheader>
                    {
                      groupFilters.map((groupFilter) => {
                        return <MenuItem key={groupFilter.id} value={groupFilter}>{groupFilter.id}</MenuItem>
                      })
                    } */}
                    {
                      testData.map((filter) => {
                        if (filter.id == defaultFilterId) {
                          return <MenuItem key={filter.id} value={filter}>{filter.id}</MenuItem>
                        }
                        else {
                          return <MenuItem key={filter.id} value={filter}>{filter.id}</MenuItem>
                        }
                      })
                    }
                  </Select>
                }

              </FormControl>
            </Box>

            {/* <Box sx={{ display: "flex", justifyContent: "flex-start", flexWrap: "wrap" }}>
              <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
                <InputLabel htmlFor="grouped-select">Direction</InputLabel>
                <Select defaultValue="" id="grouped-select" label="Direction">
                  <MenuItem value={1}>clockwise</MenuItem>
                  <MenuItem value={2}>anti-clockwise</MenuItem>
                </Select>
              </FormControl>
              <TextField label="Frame Rate" id="" defaultValue="" type="number"
                InputProps={{
                  endAdornment: <InputAdornment position="end">fps</InputAdornment>,
                }} size="small" sx={{ m: 1, width: '10vw', minWidth: 140 }} />
              <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
                <InputLabel htmlFor="grouped-select">Direction</InputLabel>
                <Select defaultValue="" id="grouped-select" label="Direction">
                  <MenuItem value={1}>clockwise</MenuItem>
                  <MenuItem value={2}>anti-clockwise</MenuItem>
                </Select>
              </FormControl>
              <TextField label="Frame Rate" id="" defaultValue="" type="number"
                InputProps={{
                  endAdornment: <InputAdornment position="end">fps</InputAdornment>,
                }} size="small" sx={{ m: 1, width: '10vw', minWidth: 140 }} />
            </Box>
            <Box sx={{ display: "flex", alignItems: "flex-start" }}>
              <IconButton variant="outlined" color="success" sx={{ my: 1, mr: 1, }}>
                <AddIcon />
              </IconButton>
              <IconButton color="error" sx={{ my: 1, mr: 1 }}>
                <DeleteOutlineIcon />
              </IconButton>
            </Box> */}

          </Box>

          {/* Display applied filters */}
          <Box>
            {
              participantCopy.audio_filters.map((audioFilter, audioFilterIndex) => {
                return (
                  <Chip key={audioFilterIndex} label={audioFilter.id} variant="outlined"  size="medium" color="secondary"
                  onDelete={() => {handleDeleteFilter(audioFilter)}} />
                  // <Chip key={audioFilterIndex} variant="outlined" label={audioFilter.id} size="small" color="secondary" />
                )
              })
            }
            {
              participantCopy.video_filters.map((videoFilter, videoFilterindex) => {
                return (
                  // <ListItem key={videoFilter.id}>
                    <Chip key={videoFilterindex} label={videoFilter.id} variant="outlined"  size="medium" color="secondary"
                    onDelete={() => {handleDeleteFilter(videoFilter)}}
                    />
                  // </ListItem>
                  // <Chip key={videoFilterindex} variant="outlined" label={videoFilter.id} size="small" color="secondary" />
                )
              })
            }
          </Box>
        </Box>
      </DialogContent>
      <DialogActions sx={{ alignSelf: "center" }}>
        <ActionButton text="CANCEL" variant="contained" color="error" size="medium" onClick={() => onCloseModalWithoutData()} />
        <ActionButton text="SAVE" variant="contained" color="success" size="medium" onClick={() => onSaveParticipantData()} />
      </DialogActions>
    </Dialog>


    // <div className="additionalParticipantInfoContainer">
    //   <ToastContainer autoClose={1000} theme="colored" hideProgressBar={true} />

    //   <div className="additionalParticipantInfo">
    //     <div className="additionalParticipantInfoCard">
    //       <Heading heading={"General information:"} />

    //       <InputTextField
    //         title="First Name"
    //         value={participantCopy.first_name}
    //         placeholder={"Name of participant"}
    //         onChange={(newFirstName) => {
    //           handleChange("first_name", newFirstName);
    //         }}
    //         required={true}
    //       />
    //       <InputTextField
    //         title="Last Name"
    //         value={participantCopy.last_name}
    //         placeholder={"Name of participant"}
    //         onChange={(newLastName) => {
    //           handleChange("last_name", newLastName);
    //         }}
    //         required={true}
    //       />
    //       <InputTextField
    //         title="Link"
    //         value={
    //           !(participantCopy.id.length === 0 || sessionId.length === 0)
    //             ? `${PARTICIPANT_HOST}?participantId=${participantCopy.id}&sessionId=${sessionId}`
    //             : "Save session to generate link."
    //         }
    //         readonly={true}
    //         required={false}
    //       />

    //       <Box sx={{ display: "flex", justifyContent: "flex-start", flexWrap: "wrap" }}>
    //         <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
    //           <InputLabel htmlFor="grouped-select">Direction</InputLabel>
    //           <Select defaultValue="" id="grouped-select" label="Direction">
    //             <MenuItem value={1}>clockwise</MenuItem>
    //             <MenuItem value={2}>anti-clockwise</MenuItem>
    //           </Select>
    //         </FormControl>
    //         <TextField label="Frame Rate" id="" defaultValue="" type="number"
    //           InputProps={{
    //             endAdornment: <InputAdornment position="end">fps</InputAdornment>,
    //           }} size="small" sx={{ m: 1, width: '10vw', minWidth: 140 }} />
    //         <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
    //           <InputLabel htmlFor="grouped-select">Direction</InputLabel>
    //           <Select defaultValue="" id="grouped-select" label="Direction">
    //             <MenuItem value={1}>clockwise</MenuItem>
    //             <MenuItem value={2}>anti-clockwise</MenuItem>
    //           </Select>
    //         </FormControl>
    //         <TextField label="Frame Rate" id="" defaultValue="" type="number"
    //           InputProps={{
    //             endAdornment: <InputAdornment position="end">fps</InputAdornment>,
    //           }} size="small" sx={{ m: 1, width: '10vw', minWidth: 140 }} />
    //       </Box>
    //       <Box sx={{ display: "flex", alignItems: "flex-start" }}>
    //         <IconButton variant="outlined" color="success" sx={{ my: 1, mr: 1, }}>
    //           <AddIcon />
    //         </IconButton>
    //         <IconButton color="error" sx={{ my: 1, mr: 1 }}>
    //           <DeleteOutlineIcon />
    //         </IconButton>
    //       </Box>

    //       <div className="participantMuteCheckbox">
    //         <Checkbox
    //           title="Mute Audio"
    //           value={participantCopy.muted_audio}
    //           checked={participantCopy.muted_audio}
    //           onChange={() =>
    //             handleChange("muted_audio", !participantCopy.muted_audio)
    //           }
    //           required={false}
    //         />
    //         <Checkbox
    //           title="Mute Video"
    //           value={participantCopy.muted_video}
    //           checked={participantCopy.muted_video}
    //           onChange={() =>
    //             handleChange("muted_video", !participantCopy.muted_video)
    //           }
    //           required={false}
    //         />
    //       </div>
    //       <Heading heading={"Current video position and size:"} />
    //       <div className="participantVideoSize">
    //         <div className="participantPosition">
    //           <Label title={"x: "} /> {participantCopy.position.x}
    //         </div>
    //         <div className="participantPosition">
    //           <Label title={"y: "} /> {participantCopy.position.y}
    //         </div>
    //         <div className="participantPosition">
    //           <Label title={"Width: "} /> {participantCopy.size.width}
    //         </div>
    //         <div className="participantPosition">
    //           <Label title={"Height: "} /> {participantCopy.size.height}
    //         </div>
    //       </div>
    //       <ActionButton text="Save Participant" variant="contained" color="primary" size="large" onClick={() => onSaveParticipantData()} />
    //       <ActionButton
    //         text="BACK"
    //         variant="contained"
    //         color="primary"
    //         size="large"
    //         onClick={() => {
    //           onCloseModalWithoutData();
    //         }}
    //       />
    //     </div>
    //   </div>
    // </div>
  );
}

export default ParticipantDataModal;
