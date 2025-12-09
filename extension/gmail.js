console.log("PhishGuard Gmail Scanner Loaded");

// Hash generator to avoid duplicate scans
function generateHash(str) {
    return [...str].reduce((acc, c) => acc + c.charCodeAt(0), 0);
}

function scanEmail() {
    try {
        const sender = document.querySelector("span.gD")?.getAttribute("email");
        const subject = document.querySelector("h2.hP")?.innerText;
        const body = document.querySelector(".a3s.aiL")?.innerText;

        if (!sender || !subject || !body) return;

        const emailData = `
        Sender: ${sender}
        Subject: ${subject}
        Content: ${body}
        `;

        const emailHash = generateHash(emailData);

        chrome.runtime.sendMessage(
            { type: "CHECK_EMAIL", emailData, emailHash },
            response => {
                if (!response) return;

                if (response.final === "phishing") {
                    showToast("🔴 PHISHING EMAIL DETECTED!", "red");
                } else {
                    showToast("🟢 Safe Email", "green");
                }
            }
        );

    } catch (e) {
        console.log("Email scan error:", e);
    }
}

// Detect new email opened (DOM observer)
const observer = new MutationObserver(() => {
    const emailOpened = document.querySelector(".ha");
    if (emailOpened) {
        scanEmail();
    }
});

observer.observe(document.body, { childList: true, subtree: true });