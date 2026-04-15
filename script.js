function loadTruckingCompanies() {
  const jsonUrl = document.getElementById("jsonUrl").value.trim();
  const errorMessage = document.getElementById("errorMessage");

  errorMessage.innerHTML = "";

  if (!jsonUrl) {
    errorMessage.innerHTML = "Please enter a valid JSON file name.";
    return;
  }

  fetch(`/cgi-bin/server.py?file=${encodeURIComponent(jsonUrl)}`)
    .then(response => response.text())
    .then(data => {
      if (data.startsWith("Error:")) {
        errorMessage.innerHTML = data;
        return;
      }

      const tableWindow = window.open("", "", "width=1200,height=800,scrollbars=yes");

      if (!tableWindow) {
        errorMessage.innerHTML = "Popup blocked. Allow popups.";
        return;
      }

      tableWindow.document.open();
      tableWindow.document.write(data);
      tableWindow.document.close();
    })
    .catch(error => {
      errorMessage.innerHTML = `Error: ${error.message}`;
    });
}
