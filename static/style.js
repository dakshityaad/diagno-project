document.addEventListener("DOMContentLoaded", () => {
  const chatContainer = document.getElementById("chat-container");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const fileUpload = document.getElementById("file-upload");
  const micBtn = document.getElementById("mic-btn");

  // Add message to chat window
  function addMessage(text, sender = "user") {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    msgDiv.textContent = text;
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  // Send text message to backend
  async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, "user");
    userInput.value = "";

    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await response.json();
    addMessage(data.reply, "bot");
  }

  // Handle send button click
  sendBtn.addEventListener("click", sendMessage);

  // Handle Enter key
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  // Handle file upload
  fileUpload.addEventListener("change", async () => {
    const file = fileUpload.files[0];
    if (!file) return;

    addMessage(`📎 Uploaded: ${file.name}`, "user");

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/upload", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    addMessage(data.reply, "bot");
  });

  // 🎤 Handle mic with Web Speech API
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US"; // change to "hi-IN" for Hindi etc.
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    micBtn.addEventListener("click", () => {
      recognition.start();
      micBtn.textContent = "🎤 Listening...";
    });

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      console.log("You said:", transcript);

      // show transcript in input
      userInput.value = transcript;

      // auto-send to backend
      sendMessage();

      micBtn.textContent = "🎤";
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      addMessage("⚠️ Speech recognition error: " + event.error, "bot");
      micBtn.textContent = "🎤";
    };

    recognition.onend = () => {
      micBtn.textContent = "🎤"; // reset when finished
    };
  } else {
    micBtn.addEventListener("click", () => {
      addMessage("⚠️ Speech-to-Text not supported in this browser.", "bot");
    });
  }
});
