// // content.js
// chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
//     console.log("API called");
//     if (message.greeting === "activateFeedback") {
//         // Your content script logic here
//     }
// });

// content.js
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.greeting === "activateFeedback") {

        // Access the prediction value from the message
        const prediction = message.prediction;

        const watermarkDiv = document.createElement("div");
        watermarkDiv.textContent = prediction === 0 ? "Legitimate" : "Malicious"; // Customize the watermark text as needed
        watermarkDiv.style.position = "fixed";
        watermarkDiv.style.top = "0";
        watermarkDiv.style.left = "0";
        watermarkDiv.style.width = "100%";
        watermarkDiv.style.backgroundColor = prediction === 0 ? 'green' : 'red'; // Background color for the watermark
        watermarkDiv.style.color = "white"; // Text color for the watermark
        watermarkDiv.style.textAlign = "center";
        watermarkDiv.style.padding = "5px";
        watermarkDiv.style.zIndex = "9999";

        // Add the banner to the document's body
        document.body.appendChild(watermarkDiv);
    }
});
