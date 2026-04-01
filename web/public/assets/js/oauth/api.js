import { t } from "../core/i18n.js";

/**
 * Fetch wrapper hitting the backend serverless endpoint
 * @param {object} payload
 */
export async function callApi(payload) {
  const res = await fetch("/api/token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),
    raw = await res.text();
  let data;
  try {
    data = JSON.parse(raw);
  } catch {
    if (404 === res.status) throw new Error(t("errApiNotFound"));
    if (
      (raw && raw.toLowerCase().includes("<html")) ||
      raw.startsWith("The page")
    )
      throw new Error(t("errApiHtml"));
    throw new Error(raw || "Unknown API response");
  }
  if (!res.ok) throw new Error(data.error || JSON.stringify(data));
  return data;
}
