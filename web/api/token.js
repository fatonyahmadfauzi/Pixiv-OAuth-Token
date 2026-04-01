const { forwardTokenRequest } = require("./_oauthProxy");
const { checkSecurity } = require("./_security");

module.exports = async (req, res) => {
  if (req.method !== "POST")
    return res.status(405).json({ error: "Method Not Allowed" });

  const sec = checkSecurity(req);
  if (!sec.ok) {
    return res.status(sec.status).json({ error: sec.error });
  }

  const { status, data } = await forwardTokenRequest(req.body || {});
  return res.status(status).json(data);
};
