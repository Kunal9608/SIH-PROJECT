const url = window.location.href;

// Delay to allow page load
setTimeout(() => {
    chrome.runtime.sendMessage(
        { type: "CHECK_URL", url },
        response => {
            if (!response) return;

            let result = response.final.final;
            if (result === "SAFE") {
                showToast("🟢 SAFE WEBSITE VERIFIED", "green");
            } else {
                showToast("🔴 PHISHING SITE BLOCKED", "red");
            }
        }
    );
}, 1200);