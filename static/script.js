document.addEventListener("DOMContentLoaded", () => {
  const chatMessages = document.getElementById("chat-messages");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");
  const themeToggle = document.getElementById("theme-toggle");

  let conversationHistory = [];
  let botResponseElement = null; // Store the bot response element

  function appendMessage(content, isUser) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(isUser ? "user-message" : "bot-message");
    messageDiv.textContent = content;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return messageDiv;
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
      appendMessage(message, true);
      userInput.value = "";
      adjustTextareaHeight();

      try {
        const response = await fetch("/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: message,
            conversation_history: conversationHistory,
          }),
        });

        console.log("Request sent to /chat, waiting for response..."); // Debugging line

        if (response.ok) {
          const reader = response.body.getReader();
          const decoder = new TextDecoder();
          let accumulatedResponse = ""; // Initialize empty accumulated response

          // Create an initial message element for the bot
          botResponseElement = appendMessage("", false);

          while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            console.log("Received chunk:", chunk); // Debugging line

            // Append only the new content
            accumulatedResponse += chunk;
            botResponseElement.textContent = accumulatedResponse; // Update only the content, not creating new elements
          }

          conversationHistory.push({ role: "user", content: message });
          conversationHistory.push({
            role: "assistant",
            content: accumulatedResponse,
          });
        } else {
          console.error(
            "Failed to get response from server:",
            response.statusText
          );
          appendMessage(
            "Failed to get response from server. Please try again.",
            false
          );
        }
      } catch (error) {
        console.error("Network error:", error);
        appendMessage("A network error occurred. Please try again.", false);
      }
    }
  }

  function adjustTextareaHeight() {
    userInput.style.height = "auto";
    userInput.style.height = userInput.scrollHeight + "px";
  }

  sendButton.addEventListener("click", sendMessage);

  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  userInput.addEventListener("input", adjustTextareaHeight);

  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
  });

  console.log("Chat interface initialized."); // Debugging line
});
