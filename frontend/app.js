const dom = {
  bars: document.querySelectorAll(".wave span"),
  circle: document.querySelector(".circle-container"),
  subtext: document.querySelector(".subtext"),
  wave: document.querySelector(".wave"),
  micIcon: document.querySelector(".mic svg"),
  stopBtn: document.querySelector(".stop"),
  confidence: document.querySelector(".confidence"),
  albums: document.querySelectorAll(".album"),
};

const LISTEN_DURATION = 7000;
let isListening = false;
let mediaRecorder = null;

dom.bars.forEach((bar) => {
  bar.style.animationDelay = `${Math.random() * 0.6}s`;
  bar.style.animationDuration = `${0.4 + Math.random() * 0.4}s`;
});

dom.bars.forEach((bar) => {
  bar.style.animationDelay = `${Math.random() * 0.6}s`;
  bar.style.animationDuration = `${0.4 + Math.random() * 0.4}s`;
});

dom.circle.addEventListener("click", async () => {
  if (isListening) return;
  isListening = true;

  resetPreviousResult();

  startCountdown(7, setAnalyzingUI);

  try {
    const audioBlob = await recordAudio(LISTEN_DURATION);
    const result = await uploadAudio(audioBlob);

    highlightAlbum(result.song_album);
    setResultUI(result.song_name, result.song_artist);
    updateConfidence(result.confidence);
  } catch (err) {
    console.error(err);
  } finally {
    isListening = false;
  }
});

async function recordAudio(durationMs) {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const recorder = new MediaRecorder(stream);
  const chunks = [];

  recorder.ondataavailable = (e) => chunks.push(e.data);

  recorder.start();

  return new Promise((resolve) => {
    setTimeout(() => {
      recorder.stop();
      recorder.onstop = () => {
        resolve(new Blob(chunks, { type: "audio/webm" }));
      };
    }, durationMs);
  });
}

async function uploadAudio(blob) {
  const formData = new FormData();
  formData.append("audio", blob, "recording.webm");

  const res = await fetch("http://localhost:8000/upload", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error(`Upload failed: ${res.status}`);
  }

  return res.json();
}

function startCountdown(seconds, onDone) {
  let remaining = seconds;
  setListeningUI(remaining);

  const id = setInterval(() => {
    remaining--;
    setListeningUI(remaining);

    if (remaining <= 0) {
      clearInterval(id);
      onDone();
    }
  }, 1000);
}

function highlightAlbum(albumName) {
  dom.albums.forEach((album) => {
    const name = album.querySelector(".name")?.textContent.trim();
    if (name === albumName) {
      album.querySelector("img")?.classList.add("selected-album");
      const tick = album.querySelector(".tick");
      tick.style.visibility = "visible";
      tick.classList.add("selected");
    }
  });
}

function setListeningUI(secondsLeft) {
  dom.subtext.textContent = `Listening ... ${secondsLeft}s`;
  dom.wave.classList.add("listening");
  dom.micIcon.style.visibility = "hidden";
  dom.stopBtn.style.visibility = "visible";
}

function setAnalyzingUI() {
  dom.subtext.textContent = "Analyzing ...";
  dom.wave.classList.remove("listening");
  dom.micIcon.style.visibility = "visible";
  dom.stopBtn.style.visibility = "hidden";
}

function setResultUI(song, artist) {
  dom.subtext.textContent = `${song} by ${artist}`;
  dom.subtext.classList.add("song-result");
}

function updateConfidence(val) {
  dom.confidence.textContent = `Confidence: ${val.toFixed(2)}`;
  dom.confidence.style.visibility = "visible";
}

function resetPreviousResult() {
  dom.albums.forEach((album) => {
    album.querySelector("img")?.classList.remove("selected-album");

    const tick = album.querySelector(".tick");
    if (tick) {
      tick.classList.remove("selected");
      tick.style.visibility = "hidden";
    }
  });

  dom.confidence.textContent = "";
  dom.confidence.style.visibility = "hidden";

  dom.subtext.classList.remove("song-result");
}
