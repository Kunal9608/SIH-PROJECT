console.log("PhishGuard BG Loaded");

const URL_API = "http://127.0.0.1:8000/check";
const EMAIL_API = "http://127.0.0.1:8001/check_text";

let scannedUrls = new Set();
let scannedEmails = new Set();

// Handle URL scanning
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {

    // ---------------- URL CHECK ----------------
    if (msg.type === "CHECK_URL") {

        if (scannedUrls.has(msg.url)) {
            return; // do not scan again
        }
        scannedUrls.add(msg.url);

        fetch(URL_API, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ url: msg.url })
        })
        .then(r => r.json())
        .then(data => {
            sendResponse(data);

            const verdict = data.final.final;

            if (verdict !== "SAFE") {
                chrome.tabs.update(sender.tab.id, { url: chrome.runtime.getURL("block.html") });
            }
        });

        return true;
    }

    // ---------------- EMAIL CHECK ----------------
    if (msg.type === "CHECK_EMAIL") {

        const hash = msg.emailHash;
        if (scannedEmails.has(hash)) {
            return; // do not rescan same email
        }
        scannedEmails.add(hash);

        fetch(EMAIL_API, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ text: msg.emailData })
        })
        .then(r => r.json())
        .then(data => {
            sendResponse(data);

            if (data.final === "phishing") {
                chrome.notifications.create({
                    type: "basic",
                    title: "Phishing Email Detected",
                    message: "A dangerous email was detected and flagged.",
                    iconUrl: "icons/icon128.png"
                });
            }
        });

        return true;
    }
});