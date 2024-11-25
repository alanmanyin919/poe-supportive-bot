// 🛠️ Configuration settings
const promptText = "continue";
const intervalTime = 2500; // ⏱️ 2.5 seconds
const clickDelay = 1500; // ⏳ 1.5 seconds delay before clicking
const totalIterations = 150; // Total iterations: 150 * 500 = 75,000 iterations

// 🗄️ Variables to manage automation state
let intervalId = null;
let isTypingPhase = true; // 🔀 Toggle between typing and clicking phases
let iterationCount = 0; // Counter for total iterations

// 🔄 Check and click the "Regenerate" button if it is present; skip iteration if clicked
function checkAndClickRegenerate() {
    const regenerateButton = document.querySelector("button[data-testid='regenerate-thread-error-button']");
    if (regenerateButton) {
        console.log("🔄 Regenerate button detected: Clicking to regenerate response.");
        regenerateButton.click();
        return true; // 🔄 Indicates that the regenerate button was clicked
    } else {
        console.log("🔍 Regenerate button not found: Skipping regenerate step.");
    }
    return false; // 🔍 Indicates that the regenerate button was not found
}

function checkAndClickCursorButton() {
    try {
        // Using escaped `/` in the selector
        const cursorButton = document.querySelector(
            "button.cursor-pointer.absolute.z-10.rounded-full.bg-clip-padding.border.text-token-text-secondary.border-token-border-light.right-1\\/2.translate-x-1\\/2.bg-token-main-surface-primary.w-8.h-8.flex.items-center.justify-center.bottom-5"
        );

        if (cursorButton) {
            console.log("🖱️ Cursor button detected. Attempting to click...");
            cursorButton.focus(); // Focus on the button
            cursorButton.dispatchEvent(new MouseEvent("mousedown", { bubbles: true, cancelable: true }));
            cursorButton.dispatchEvent(new MouseEvent("mouseup", { bubbles: true, cancelable: true }));
            cursorButton.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }));
            console.log("✅ Cursor button clicked successfully.");
            return true; // Indicate the button was found and clicked
        } else {
            console.log("🔍 Cursor button not found. Skipping this step.");
        }
    } catch (error) {
        console.error("⚠️ Error while checking or clicking the cursor button:", error);
    }
    return false; // Indicate the button was not found or clicked
}


// 🖱️ Fully simulate a button click with focus, mousedown, mouseup, and click events
function simulateButtonClick(button) {
    button.focus();
    button.dispatchEvent(new MouseEvent("mousedown", { bubbles: true, cancelable: true }));
    button.dispatchEvent(new MouseEvent("mouseup", { bubbles: true, cancelable: true }));
    button.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }));
    console.log("🖱️ Full button click simulation triggered.");
}

// 💬 Insert text into the contenteditable input field and ensure updates are registered
function insertPromptText(inputField, text) {
    inputField.innerHTML = `<p>${text}</p>`;
    inputField.dispatchEvent(new Event("input", { bubbles: true }));
    inputField.focus();
    setTimeout(() => inputField.blur(), 100); // 🔄 Short delay to register input
    console.log(`💬 Prompt text "${text}" inserted and registered in the input field.`);
}

// 🔍 Check if a response is actively streaming based on the presence of the "Stop streaming" button
function isStreaming() {
    const streamingButton = document.querySelector("button[aria-label='Stop streaming'], button[data-testid='stop-button']");
    if (streamingButton) {
        console.log("📡 Streaming detected: Waiting for response to finish.");
        return true;
    } else {
        console.log("✅ No streaming detected: Ready to send next prompt.");
        return false;
    }
}

// 🔄 Main function to handle the automation process
function processAutomation() {
    try {
        console.log("🚀 Starting automation process...");

        // 🔍 Skip if streaming is active
        if (isStreaming()) {
            console.log("⏸️ Skipping automation process due to active streaming.");
            return;
        }

        // 🔄 Check and click the "Regenerate" button if present
        if (checkAndClickRegenerate()) {
            console.log("⏩ Skipping current iteration after clicking regenerate.");
            return;
        }

        // 🔀 Toggle between typing and clicking phases
        if (isTypingPhase) {
            // ✍️ Typing Phase: Insert prompt text into input field
            const inputField = document.querySelector("#prompt-textarea");
            if (inputField) {
                checkAndClickCursorButton();
                insertPromptText(inputField, promptText);
                console.log("✍️ Typing phase completed. Switching to clicking phase.");
                isTypingPhase = false; // Move to the clicking phase
            } else {
                console.error("❌ Input field not found. Unable to complete typing phase.");
            }
        } else {
            // 🖱️ Clicking Phase: Attempt to submit the prompt
            const submitButton = document.querySelector("button[aria-label='Send prompt'], button[data-testid='send-button']");
            if (submitButton) {
                setTimeout(() => {
                    console.log("⏳ Attempting full button click simulation after delay.");
                    simulateButtonClick(submitButton);
                    isTypingPhase = true; // 🔄 Move back to typing phase for next iteration
                }, clickDelay); // Delay set to 1.5 seconds (adjustable)
            } else {
                console.error("❌ Submit button not found. Unable to complete clicking phase.");
            }
        }

        // Increment the iteration count and check if we've reached the total iteration limit
        iterationCount++;
        if (iterationCount >= totalIterations) {
            console.log(`🚫 Reached the total iteration limit of ${totalIterations}. Stopping automation.`);
            stopAutomation();
        }

    } catch (error) {
        console.error("⚠️ An error occurred during the automation process:", error);
    }
}

// 🛑 Stop the automated prompt submission and reset state variables
function stopAutomation() {
    if (intervalId !== null) {
        clearInterval(intervalId);
        intervalId = null;
        isTypingPhase = true; // 🔄 Reset to typing phase
        console.log("🛑 Automated prompt submission stopped and state reset.");
    } else {
        console.log("🚫 Automation is not running.");
    }
}

// 🏁 Start the automation by setting up the interval directly
function startAutomation() {
    intervalId = setInterval(processAutomation, intervalTime);
    console.log(`🚀 Automated prompt submission started with interval of ${intervalTime / 1000} seconds, running until ${totalIterations} iterations.`);
}

// To start, run `startAutomation();` in the console
// To manually stop, use `stopAutomation();` in the console
