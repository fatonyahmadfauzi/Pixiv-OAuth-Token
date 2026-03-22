const { forwardTokenRequest } = require("./_oauthProxy");

module.exports = async (req, res) => {
  if (req.method !== "POST") return res.status(405).json({ error: "Method Not Allowed" });
  const { status, data } = await forwardTokenRequest(req.body || {});
  return res.status(status).json(data);
};
