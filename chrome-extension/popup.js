document.addEventListener("DOMContentLoaded", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  document.getElementById("url").value = tab.url;
  document.getElementById("title").value = tab.title;

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
      console.log(data);
    });
});
