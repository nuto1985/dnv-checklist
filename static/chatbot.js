document.addEventListener("DOMContentLoaded", function () {
  const chatIcon = document.getElementById("chat-icon");
  const chatBox = document.getElementById("chat-box");
  const chatLog = document.getElementById("chat-log");
  const chatInput = document.getElementById("chat-input");

  const keywordMap = {
    "escape": "Escape routes are described in section 9.5...",
    "muster": "Muster areas are covered in section 9.6...",
    "evacuation": "Section 9.7 covers evacuation means...",
    "alarm": "Alarm systems must reach 80 dB(A)...",
    "shutdown": "Shutdown actions are defined in section 9.4..."
  };

  chatIcon.addEventListener("click", () => {
    chatBox.style.display = chatBox.style.display === "none" ? "block" : "none";
    if (!chatLog.innerHTML.includes("💡")) {
      chatLog.innerHTML = '<div style="font-size: 0.9em; color: #555;">💡 Tip: Type keywords like "escape", "alarm", or "muster" for help.</div><hr>';
    }
  });

  chatInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      const question = chatInput.value.toLowerCase();
      let response = "Sorry, I don't have an answer for that.";
      for (const key in keywordMap) {
        if (question.includes(key)) {
          response = keywordMap[key];
          break;
        }
      }
      chatLog.innerHTML += `<div><strong>You:</strong> ${chatInput.value}</div>`;
      chatLog.innerHTML += `<div><strong>Bot:</strong> ${response}</div>`;
      chatInput.value = "";
      chatLog.scrollTop = chatLog.scrollHeight;
    }
  });
});