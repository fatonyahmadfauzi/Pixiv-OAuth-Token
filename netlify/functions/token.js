const { forwardTokenRequest } = require("../../api/_oauthProxy");

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: JSON.stringify({ error: "Method Not Allowed" }) };
  }

  let payload = {};
  try { payload = JSON.parse(event.body || "{}"); } catch {}

  const { status, data } = await forwardTokenRequest(payload);
  return {
    statusCode: status,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  };
};
