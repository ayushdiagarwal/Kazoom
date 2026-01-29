const bars = document.querySelectorAll(".wave span");
const listen = document.querySelector(".circle-container");
const subtext = document.querySelector(".subtext");
const wave = document.querySelector(".wave");
const micBtn = document.querySelector(".mic svg");
const stopBtn = document.querySelector(".stop");
const confidence = document.querySelector(".confidence");

let timerId = null;

for (let i = 0; i < bars.length; i++) {
  const delay = Math.random() * 0.6;
  const duration = 0.4 + Math.random() * 0.4;

  bars[i].style.animationDelay = delay + "s";
  bars[i].style.animationDuration = duration + "s";
}

listen.addEventListener("click", async () => {
  if (timerId) return;

  let timeLeft = 7;
  subtext.innerHTML = `Listening ... ${timeLeft}s`;
  wave.classList.add("listening");
  micBtn.style.visibility = "hidden";
  stopBtn.style.visibility = "visible";

  timerId = setInterval(() => {
    timeLeft--;
    subtext.innerHTML = `Listening ... ${timeLeft}s`;

    if (timeLeft <= 0) {
      clearInterval(timerId);
      timerId = null;

      subtext.innerHTML = "Analyzing ...";
      wave.classList.remove("listening");
      micBtn.style.visibility = "visible";
      stopBtn.style.visibility = "hidden";
    }
  }, 1000);

  try {
    // request mic
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    const mediaRecorder = new MediaRecorder(stream);
    const audioChunks = [];

    mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, {
        type: "audio/webm",
      });

      const url = URL.createObjectURL(audioBlob);

      // send the recorded audio to flask backend
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      try {
        const response = await fetch("http://localhost:5000/upload", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const text = await response.text();
          console.error("Server returned error: ", response.status, text);
          return;
        }

        const result = await response.json();
        console.log("Server response: ", result);
        console.log(
          `Song name: ${result.song_name}, Artist: ${result.song_artist}, Album: ${result.song_album}`,
        );

        const albums = document.querySelectorAll(".album");

        console.log(albums);

        albums.forEach((album) => {
          const nameDiv = album.querySelector(".name");
          const tickDiv = album.querySelector(".tick");
          const album_img = album.querySelector("img");

          console.log(nameDiv);

          if (
            nameDiv &&
            tickDiv &&
            nameDiv.textContent.trim() === result.song_album
          ) {
            album_img.classList.add("selected-album");
            tickDiv.style.visibility = "visible";
            tickDiv.classList.add("selected");
          }
        });
        updateSongResponse(result.song_name, result.song_artist);
        updateConfidence(result.confidence);
      } catch (err) {
        console.error("Error sending audio: ", err);
      }
    };

    mediaRecorder.start();

    setTimeout(() => {
      mediaRecorder.stop();
      console.log("Recording stopped.");
    }, 7000);
  } catch (err) {
    console.error("Microphone access denied: ", err);
  }
});

// update both of these
function updateSongResponse(song, artist) {
  subtext.innerHTML = `${song} by ${artist}`;
  subtext.classList.add("song-result");
}

function updateConfidence(newVal) {
  confidence.textContent = "Confidence: " + newVal.toFixed(2);
  confidence.style.visibility = "visible";
}
