(async () => {
  const response = await fetch("http://localhost:4242/ingest/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url: window.location.href,
      title: document.title,
    }),
  });
  const data = await response.json();
})();
