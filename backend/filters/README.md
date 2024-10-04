The current list of filters currently offered within the main project are:
| Filter Name | Description | Filter Type | Filter Link| Developer|
| ------------| ----------------------------| -------| ---------| ---------|
| edge detection| applies Canny edge detection and visualizes edges of video feed.| manipulation| included | Alexander Liebald |
|rotation | continuously rotates video feed.| manipulation| included | Alexander Liebald |
|v delay | delays the video feed by X seconds. | manipulation| included | Alexander Liebald|
|a delay| delays the audio feed by X seconds. | manipulation | included |Alexander Liebald|
| openfaceAU12 | reads and displays AU12 to video stream | analysis | included | Julian Geheeb |
| ping | Calculates ping between participant and backend. This is done by initiating a pinging process through the FilterAPI which periodicaly sends messages to estimate currrent ping. | analysis | included | Jonas Goos

**Filter Name** is the name of the filter as you will find in the front end drop down selection.

**Description** is the expected behavior of the filter when applied to a video stream.

**Filter Type** is a label to determine if the filter is for real time _analysis_ of the video stream or if it _manipulates_ the visual output of the stream, or if it does _both_ (e.g. could be a filter that makes someone look more sweaty if their visually detected heart rate goes up.)

**Filter Link** is the link to filters made by external collaborators and contributors. If it is included in the project main by _default_ it is also indicated as such.

**Developer** is the name of the person who created the filter and who deserves the credit for it.

# Have an idea for a filter?!

Or have you already implemented one and would like to see how it can be integrated to our experimental hub? Check out our [Filters & Group Filters](https://github.com/TUMFARSynchrony/experimental-hub/wiki/Filters-&-Group-Filters) wiki page and consider linking your external repo in the table above or even contributing it to be a core hub filter!
