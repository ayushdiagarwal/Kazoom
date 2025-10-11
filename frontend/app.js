const squares = document.querySelectorAll(".square");
const songRes = document.querySelectorAll(".res");
const songStats = document.querySelectorAll(".stats");
const songName = null;

squares.forEach((square) => {
  square.addEventListener("click", async () => {
    try {
      // Request microphone
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];

      mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        const url = URL.createObjectURL(audioBlob);

        // Send to flask backend
        const formData = new FormData();
        formData.append("audio", audioBlob, "recording.webm");

        try {
          const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData,
          });

          if (!response.ok) {
            const text = await response.text();
            console.error("Server returned error:", response.status, text);
            return;
          }

          const result = await response.json();
          console.log("Server response:", result);
          console.log("Song name:", result.song_name);
          updateSongResponse(result.song_name);
          updateConfidence(result.confidence);
        } catch (err) {
          console.error("Error sending audio:", err);
        }
      };

      mediaRecorder.start();
      console.log("Recording started...");

      setTimeout(() => {
        mediaRecorder.stop();
        console.log("Recording stopped.");
      }, 7000);
    } catch (err) {
      console.error("Microphone access denied:", err);
    }
  });
});

function updateSongResponse(newText) {
  songRes.forEach((el) => {
    el.textContent = "Now Playing: " + newText;
    el.style.visibility = "visible";
  });
}

function updateConfidence(newVal) {
  songStats.forEach((s) => {
    s.textContent = "Confidence: " + newVal;
    s.style.visibility = "visible";
  });
}
