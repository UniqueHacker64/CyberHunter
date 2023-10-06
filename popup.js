// var currentDomain = null;

// chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
//     if (changeInfo.status === "complete") {
//         var tabDomain = extractMainDomain(tab.url);
//         if (tabDomain !== currentDomain) {
//             currentDomain = tabDomain;
//             console.log(currentDomain);
//             document.getElementById('domain').textContent = "Main Domain: " + currentDomain;
//         }
//     }
// });

// document.addEventListener('DOMContentLoaded', function () {
//     chrome.tabs.query({
//         active: true,
//         lastFocusedWindow: true
//     }, function (tabs) {
//         var tab = tabs[0];
//         var tabDomain = extractMainDomain(tab.url);
//         currentDomain = tabDomain;
//         console.log(currentDomain);
//         document.getElementById('domain').textContent = "Main Domain: " + currentDomain;
//         document.getElementById('current-url').textContent = "Current URL: " + tab.url;
//     });
// });

// function extractMainDomain(url) {
//     var matches = url.match(/^(https?:\/\/[^/]+)/i);
//     if (matches !== null && matches.length > 1) {
//         return matches[1];
//     }
//     return null;
// }
let currentDomain = null;
let predictedValue = null;
console.log("page called");

chrome.tabs.query({ active: true, lastFocusedWindow: true }, async function (tabs) {
    console.log("API called");
    const tab = tabs[0];
    const tabDomain = extractMainDomain(tab.url);
    currentDomain = tabDomain;
    alert("call api")
    // alert(currentDomain);
    // console.log("API called");
    if (currentDomain != null){
        predictedValue = await fetchData(currentDomain);
        updatePopup(currentDomain, predictedValue);
    }

    chrome.tabs.sendMessage(tab.id, { greeting: "activateFeedback", prediction: predictedValue });
    // predictedValue = await fetchData(currentDomain);
    // updatePopup(currentDomain, predictedValue);
});

// chrome.webNavigation.onCompleted.addListener(async function (details) {
//     alert("listner activated")
//     const tabDomain = extractMainDomain(details.url);
//     alert(tabDomain)
//     if (tabDomain !== currentDomain) {
//         await fetchData(currentDomain);
//         updatePopup(currentDomain);
//         // Log a message when a new page is loaded
//         alert("New page loaded with domain: " + currentDomain)
//         console.log("API called" + currentDomain);
//     }
// });

async function fetchData(currentDomain) {
    try {
        if (currentDomain != null){
            const dataToSend = {
                text: currentDomain
            };

            const response = await fetch('http://127.0.0.1:8000/cyberHunter/post', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataToSend)
            });

            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            
            const data = await response.json();
            predictedValue = data.predictions;
            return predictedValue;
        }

        } catch (error) {
            console.error(error);
            alert('An error occurred while fetching data');
        }
        
}

function updatePopup(domain, predictedValue ) {
    document.getElementById('domain').textContent = "Main Domain: " + domain;
    website = predictedValue === 0 ? "Legitimate website" : 'Malicious website'
    document.body.style.backgroundColor = "green";
    document.getElementById('current-url').textContent = "Predictions Output: " + website;
}

function extractMainDomain(url) {
    console.log("API called");
    const matches = url.match(/^(https?:\/\/[^/]+)/i);
    if (matches !== null && matches.length > 1) {
        return matches[1];
    }
    return null;
}




