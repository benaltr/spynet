// Send URLs to the Python server
function sendUrls(urls) {
    fetch('http://localhost:5000/urls', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ urls })
    }).then(response => {
      console.log('URLs sent successfully');
    }).catch(error => {
      console.error('Error sending URLs:', error);
    });
  }
  
  // Event listener for URL changes
  chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (changeInfo.url) {
      sendUrls([changeInfo.url]);
    }
  });
  