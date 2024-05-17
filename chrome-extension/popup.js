document.addEventListener("DOMContentLoaded", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  let url = tab.url;
  if (url.includes("&")) {
    url = url.split("&")[0];
  }
  let title = tab.title;
  if (title.includes(" - YouTube")) {
    title = title.replace(" - YouTube", "");
  }

  document.getElementById("url").value = url;
  document.getElementById("title").value = title;

  document
    .getElementById("data-form")
    .addEventListener("submit", async (event) => {
      event.preventDefault();

      const url = document.getElementById("url").value;
      const title = document.getElementById("title").value;
      const authors = document.getElementById("authors").value;

      const response = await fetch("http://localhost:4242/ingest/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url,
          title: title,
          authors: authors,
        }),
      });

      const data = await response.json();

      // if data contains {'status': 'success'}, then show success message:
      if (data.status === "success") {
        document.getElementById("data-form").style.display = "none";
        document.getElementById("success").style.display = "block";
      }
    });
});
