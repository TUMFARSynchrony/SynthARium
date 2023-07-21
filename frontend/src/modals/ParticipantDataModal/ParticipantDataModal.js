import { useState } from "react";
import { ActionButton } from "../../components/atoms/Button";
import Box from "@mui/material/Box";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import FormControlLabel from "@mui/material/FormControlLabel";
import TextField from "@mui/material/TextField";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import ListSubheader from "@mui/material/ListSubheader";
import Chip from "@mui/material/Chip";
import Typography from "@mui/material/Typography";
import Checkbox from "@mui/material/Checkbox";
import { getParticipantInviteLink } from "../../utils/utils";
import CustomSnackbar from "../../components/atoms/CustomSnackbar/CustomSnackbar";
import { initialSnackbar } from "../../utils/constants";
// TO REMOVE: Mocking filters data until filter API call is established, remove once done
// This is new filters, with dynamic config parameters.
//import filtersData from '../../filters_new.json'

// This is the current filters that is working integrated with the backend.
import filtersData from "../../filters.json";

// Loading filters data before the component renders, because the Select component needs value.
const testData = filtersData.filters;

// We set the 'selectedFilter' to a default filter type, because the MUI Select component requires a default value when the page loads.
// For current filters, set default filter = "test", and for new filters set default filter = "none"
const defaultFilterId = "test";

const getIndividualFilters = () => {
  return testData.filter((filter) => filter.groupFilter !== true);
};

const getGroupFilters = () => {
  return testData.filter((filter) => filter.groupFilter === true);
};

function ParticipantDataModal({
  originalParticipant,
  sessionId,
  index,
  showParticipantInput,
  setShowParticipantInput,
  handleParticipantChange,
  onDeleteParticipant,
  setSnackbarResponse
}) {
  const [participantCopy, setParticipantCopy] = useState(originalParticipant);
  const [selectedFilter, setSelectedFilter] = useState(
    testData.find((filter) => filter.id === defaultFilterId)
  );
  const individualFilters = getIndividualFilters();
  const groupFilters = getGroupFilters();
  const [snackbar, setSnackbar] = useState(initialSnackbar);

  // Setting these snackbar response values to display the notification in Session Form Page.
  // These notifications cannot be displayed in this file, since on closing the Participant Modal,
  // this component and the immediate parent are deleted -> hence sending the snackbar responses
  // up to the grandparent.
  const snackbarResponse = {
    newParticipantInputEmpty: false,
    requiredInformationMissing: false,
    participantOriginalEmpty: false,
    newInputEqualsOld: false
  };

  const handleChange = (objKey, objValue) => {
    const newParticipantData = { ...participantCopy };
    newParticipantData[objKey] = objValue;
    setParticipantCopy(newParticipantData);
  };

  // On closing the edit participant dialog, the entered data is checked (if data is not saved,
  // if required data is missing) to display appropriate notification.
  const onCloseModalWithoutData = () => {
    setShowParticipantInput(!showParticipantInput);

    let newParticipantInputEmpty =
      participantCopy.first_name === "" && participantCopy.last_name === "";
    if (newParticipantInputEmpty) {
      setSnackbarResponse({
        ...snackbarResponse,
        newParticipantInputEmpty: newParticipantInputEmpty
      });
      onDeleteParticipant(index);
      return;
    }

    let requiredInformationMissing =
      participantCopy.first_name === "" || participantCopy.last_name === "";
    if (requiredInformationMissing) {
      setSnackbarResponse({
        ...snackbarResponse,
        requiredInformationMissing: requiredInformationMissing
      });
      onDeleteParticipant(index);
      return;
    }

    let participantOriginalEmpty =
      originalParticipant.first_name.length === 0 &&
      originalParticipant.last_name.length === 0;
    let newInputEqualsOld =
      JSON.stringify(participantCopy) === JSON.stringify(originalParticipant);

    if (participantOriginalEmpty && !newInputEqualsOld) {
      setSnackbarResponse({
        ...snackbarResponse,
        participantOriginalEmpty: participantOriginalEmpty,
        newInputEqualsOld: newInputEqualsOld
      });
      onDeleteParticipant(index);
      return;
    }

    if (!newInputEqualsOld) {
      setSnackbar({
        open: true,
        text: "You need to save the information first!",
        severity: "warning"
      });
      setParticipantCopy(originalParticipant);
      return;
    }
  };

  const onSaveParticipantData = () => {
    if (participantCopy.first_name === "" || participantCopy.last_name === "") {
      setSnackbar({
        open: true,
        text: "Failed to save participant since required fields are missing!",
        severity: "error"
      });
      return;
    }

    setSnackbar({
      open: true,
      text: `Saved participant: ${participantCopy.first_name} ${participantCopy.last_name}`,
      severity: "success"
    });
    setShowParticipantInput(!showParticipantInput);
    handleParticipantChange(index, participantCopy);
  };

  const handleFilterSelect = (filter) => {
    setSelectedFilter(filter);

    // Use this line for current filters.
    if (
      ["test", "edge", "rotation", "delay-v", "display-speaking-time"].includes(
        filter.id
      )
    ) {
      // Uncomment to use for new filters.
      // if (testData.map((f) => f.type === "video" || f.type === "both" ? f.id : "").includes(filter.id)) {
      setParticipantCopy((oldParticipant) => ({
        ...oldParticipant,
        video_filters: [...oldParticipant.video_filters, filter]
      }));
    }
    // Use this line for current filters.
    else if (
      ["delay-a", "delay-a-test", "audio-speaking-time"].includes(filter.id)
    ) {
      // Uncomment to use for new filters.
      // if (testData.map((f) => f.type === "audio" || f.type === "both" ? f.id : "").includes(filter.id)) {
      setParticipantCopy((oldParticipant) => ({
        ...oldParticipant,
        audio_filters: [...oldParticipant.audio_filters, filter]
      }));
    }
  };

  const handleDeleteVideoFilter = (filterCopyIndex) => {
    setParticipantCopy((oldParticipant) => ({
      ...oldParticipant,
      video_filters: oldParticipant.video_filters.filter(
        (filter, index) => index !== filterCopyIndex
      )
    }));
  };

  const handleDeleteAudioFilter = (filterCopyIndex) => {
    setParticipantCopy((oldParticipant) => ({
      ...oldParticipant,
      audio_filters: oldParticipant.audio_filters.filter(
        (filter, index) => index !== filterCopyIndex
      )
    }));
  };

  return (
    <>
      <CustomSnackbar
        open={snackbar.open}
        text={snackbar.text}
        severity={snackbar.severity}
        handleClose={() => setSnackbar(initialSnackbar)}
      />
      <Dialog
        open={showParticipantInput}
        onClose={() => onCloseModalWithoutData()}
      >
        <DialogTitle sx={{ textAlign: "center", fontWeight: "bold" }}>
          Participant Details
        </DialogTitle>
        <DialogContent>
          <Box>
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                gap: 5,
                my: 3
              }}
            >
              <TextField
                label="First Name"
                value={participantCopy.first_name}
                size="small"
                fullWidth
                required
                onChange={(event) => {
                  handleChange("first_name", event.target.value);
                }}
              />
              <TextField
                label="Last Name"
                value={participantCopy.last_name}
                size="small"
                fullWidth
                required
                onChange={(event) => {
                  handleChange("last_name", event.target.value);
                }}
              />
            </Box>
            <Box>
              <TextField
                label="Invite Link"
                size="small"
                fullWidth
                disabled
                value={
                  !(participantCopy.id.length === 0 || sessionId.length === 0)
                    ? getParticipantInviteLink(participantCopy.id, sessionId)
                    : "Save session to generate link."
                }
              />
            </Box>
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                gap: 4,
                my: 3
              }}
            >
              <TextField
                label="Width"
                size="small"
                value={participantCopy.size.width}
                disabled
              />
              <TextField
                label="Height"
                size="small"
                value={participantCopy.size.height}
                disabled
              />
              <TextField
                label="x coordinate"
                size="small"
                value={participantCopy.position.x}
                disabled
              />
              <TextField
                label="y coordinate"
                size="small"
                value={participantCopy.position.y}
                disabled
              />
            </Box>
            <Box
              sx={{ display: "flex", justifyContent: "center", gap: 2, my: 3 }}
            >
              <FormControlLabel
                control={<Checkbox />}
                label="Mute Audio"
                checked={participantCopy.muted_audio}
                onChange={() => {
                  handleChange("muted_audio", !participantCopy.muted_audio);
                }}
              />
              <FormControlLabel
                control={<Checkbox />}
                label="Mute Video"
                checked={participantCopy.muted_video}
                onChange={() => {
                  handleChange("muted_video", !participantCopy.muted_video);
                }}
              />
            </Box>

            {/* Displays the list of filters available in the backend in a dropdown */}
            <Box sx={{ display: "flex", justifyContent: "flex-start" }}>
              <FormControl sx={{ m: 1, minWidth: 180 }} size="small">
                <InputLabel id="filters-select">Filters</InputLabel>
                {
                  <Select
                    value={selectedFilter}
                    default=""
                    id="filters-select"
                    label="Filters"
                  >
                    <ListSubheader sx={{ fontWeight: "bold", color: "black" }}>
                      Individual Filters
                    </ListSubheader>
                    {/* Uncomment the below block to use new filters. */}
                    {/* {
                      individualFilters.map((individualFilter) => {
                        if (individualFilter.id == defaultFilterId) {
                          return <MenuItem key={individualFilter.id} value={individualFilter} disabled><em>{individualFilter.id}</em></MenuItem>
                        }
                        else {
                          return <MenuItem key={individualFilter.id} value={individualFilter} onClick={() => handleFilterSelect(individualFilter)}>{individualFilter.id}</MenuItem>
                        }
                      })
                    }
                    <ListSubheader sx={{ fontWeight: "bold", color: "black" }}>Group Filters</ListSubheader>
                    {
                      groupFilters.map((groupFilter) => {
                        return <MenuItem key={groupFilter.id} value={groupFilter} onClick={() => handleFilterSelect(groupFilter)}>{groupFilter.id}</MenuItem>
                      })
                    } */}
                    {/* Use the below block for current filters. */}
                    {testData.map((filter, filterIndex) => {
                      if (filter.id === defaultFilterId) {
                        return (
                          <MenuItem key={filterIndex} value={filter} disabled>
                            <em>{filter.id}</em>
                          </MenuItem>
                        );
                      } else {
                        return (
                          <MenuItem
                            key={filterIndex}
                            value={filter}
                            onClick={() => handleFilterSelect(filter)}
                          >
                            {filter.id}
                          </MenuItem>
                        );
                      }
                    })}
                  </Select>
                }
              </FormControl>
              <Typography variant="caption" sx={{ mt: 4 }}>
                (NOTE: You can select each filter multiple times)
              </Typography>
            </Box>

            {/* Displays applied audio filters */}
            <Box>
              <Typography variant="overline" display="block">
                Audio Filters
              </Typography>
              {participantCopy.audio_filters.map(
                (audioFilter, audioFilterIndex) => {
                  return (
                    <Box
                      key={audioFilterIndex}
                      sx={{ display: "flex", justifyContent: "flex-start" }}
                    >
                      <Box sx={{ minWidth: 140 }}>
                        <Chip
                          key={audioFilterIndex}
                          label={audioFilter.id}
                          variant="outlined"
                          size="medium"
                          color="secondary"
                          onDelete={() => {
                            handleDeleteAudioFilter(audioFilterIndex);
                          }}
                        />
                      </Box>

                      {/* Uncomment the below block while using new filters (audio). */}
                      {/* If the config attribute is an array, renders a dropdown. If it is a number, renders an input for number */}
                      {/* <Box sx={{ display: "flex", justifyContent: "flex-start", flexWrap: "wrap" }}>
                        {
                          Object.keys(audioFilter.config).map((configType, configIndex) => {
                            if (Array.isArray(audioFilter["config"][configType]["value"])) {
                              return (
                                <FormControl key={configIndex} sx={{ m: 1, width: '10vw', minWidth: 130 }} size="small">
                                  <InputLabel htmlFor="audio-filters-config">{configType.charAt(0).toUpperCase() + configType.slice(1)}</InputLabel>
                                  <Select key={configIndex} defaultValue="" id="audio-filters-config" label="Direction">
                                    {
                                      audioFilter["config"][configType]["value"].map((value) => {
                                        return <MenuItem key={value} value={value}>{value}</MenuItem>
                                      })
                                    }
                                  </Select>
                                </FormControl>
                              )
                            } else if (typeof audioFilter["config"][configType]["value"] == "number") {
                              return (
                                <TextField key={configIndex} label={configType.charAt(0).toUpperCase() + configType.slice(1)} id="" defaultValue="" type="number" size="small"
                                  sx={{ m: 1, width: '10vw', minWidth: 130 }} />
                              )
                            }
                          })
                        }
                      </Box> */}
                    </Box>
                  );
                }
              )}

              {/* Displays applied video filters */}
              <Typography variant="overline" display="block">
                Video Filters
              </Typography>
              {participantCopy.video_filters.map(
                (videoFilter, videoFilterIndex) => {
                  return (
                    <Box
                      key={videoFilterIndex}
                      sx={{ display: "flex", justifyContent: "flex-start" }}
                    >
                      <Box sx={{ minWidth: 140 }}>
                        <Chip
                          key={videoFilterIndex}
                          label={videoFilter.id}
                          variant="outlined"
                          size="medium"
                          color="secondary"
                          onDelete={() => {
                            handleDeleteVideoFilter(videoFilterIndex);
                          }}
                        />
                      </Box>

                      {/* Uncomment the below block while using new filters (video). */}
                      {/* If the config attribute is an array, renders a dropdown. Incase of a number, renders an input for number */}
                      {/* <Box sx={{ display: "flex", justifyContent: "flex-start", flexWrap: "wrap" }}>
                        {
                          Object.keys(videoFilter.config).map((configType, configIndex) => {
                            if (Array.isArray(videoFilter["config"][configType]["value"])) {
                              return (
                                <FormControl key={configIndex} sx={{ m: 1, width: '10vw', minWidth: 130 }} size="small">
                                  <InputLabel htmlFor="grouped-select">{configType.charAt(0).toUpperCase() + configType.slice(1)}</InputLabel>
                                  <Select key={configIndex} defaultValue="" id="grouped-select">
                                    {
                                      videoFilter["config"][configType]["value"].map((value) => {
                                        return <MenuItem key={value} value={value}>{value}</MenuItem>
                                      })
                                    }
                                  </Select>
                                </FormControl>
                              )
                            } else if (typeof videoFilter["config"][configType]["value"] == "number") {
                              return (
                                <TextField key={configIndex} label={configType.charAt(0).toUpperCase() + configType.slice(1)} id="" defaultValue="" type="number" size="small"
                                  sx={{ m: 1, width: '10vw', minWidth: 130 }} />
                              )
                            }
                          })
                        }
                      </Box> */}
                    </Box>
                  );
                }
              )}
            </Box>
          </Box>
        </DialogContent>
        <DialogActions sx={{ alignSelf: "center" }}>
          <ActionButton
            text="CANCEL"
            variant="contained"
            color="error"
            size="medium"
            onClick={() => onCloseModalWithoutData()}
          />
          <ActionButton
            text="SAVE"
            variant="contained"
            color="success"
            size="medium"
            onClick={() => onSaveParticipantData()}
          />
        </DialogActions>
      </Dialog>
    </>
  );
}

export default ParticipantDataModal;
