document.addEventListener("DOMContentLoaded", function () {
  const chatIcon = document.getElementById("chat-icon");
  const chatBox = document.getElementById("chat-box");
  const chatLog = document.getElementById("chat-log");
  const chatInput = document.getElementById("chat-input");

  chatIcon.addEventListener("click", () => {
    chatBox.style.display = chatBox.style.display === "none" ? "block" : "none";
  });

  chatInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      const question = chatInput.value.toLowerCase();
      let response = "Sorry, I don't have an answer for that.";

      if (question.includes("muster")) {
        response = "Muster areas are covered in section 9.6. <a href='/checklist/9.6'>Go to 9.6</a>";
      } else if (question.includes("evacuation")) {
        response = "Evacuation types are explained in section 9.7. <a href='/checklist/9.7'>Go to 9.7</a>";
      } else if (question.includes("escape")) {
        response = "Escape routes are detailed in section 9.5. <a href='/checklist/9.5'>Go to 9.5</a>";
      } else if (question.includes("alarm")) {
        response = "Alarms and communication are covered in section 9.3. <a href='/checklist/9.3'>Go to 9.3</a>";
      }

      chatLog.innerHTML += `<div><strong>You:</strong> ${chatInput.value}</div>`;
      chatLog.innerHTML += `<div><strong>Bot:</strong> ${response}</div>`;
      chatInput.value = "";
      chatLog.scrollTop = chatLog.scrollHeight;
    }
  });
});