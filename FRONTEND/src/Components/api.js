const Base = import.meta.env.VITE_API_URL;

async function req(path, opts) {
  const res = await fetch(Base + path, opts);

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}

export const getGuide = () => req("/api/guide");

export const getThemes = () => req("/api/themes");

export const askQuestion = (question) =>
  req("/api/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });